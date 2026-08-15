#!/usr/bin/env python3
"""Validate protected Markdown/MDX structures after English-to-Thai translation."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


FENCE_OPEN_RE = re.compile(r"^(?P<indent>[ \t]{0,3})(?P<marker>`{3,}|~{3,})(?P<info>[^\r\n]*)$")
FRONTMATTER_KEY_RE = re.compile(r"^(?P<indent>[ \t]*)(?P<key>[A-Za-z0-9_.-]+)[ \t]*:")
INLINE_CODE_RE = re.compile(r"(?<!`)(`+)([^\r\n]*?)\1(?!`)")
IMPORT_EXPORT_RE = re.compile(r"^[ \t]*(?:import|export)\b.*$", re.MULTILINE)
HTML_COMMENT_RE = re.compile(r"<!--[\s\S]*?-->")
TAG_RE = re.compile(r"</?[A-Za-z][^<>]*?>", re.DOTALL)
INLINE_LINK_RE = re.compile(r"!?\[[^\]\r\n]*\]\(\s*([^\r\n)]*?)\s*\)")
REFERENCE_DEF_RE = re.compile(
    r"^[ \t]*\[([^\]\r\n]+)\]:[ \t]*(\S+)(?:[ \t]+.*)?$", re.MULTILINE
)
REFERENCE_USE_RE = re.compile(r"\[[^\]\r\n]*\]\[([^\]\r\n]*)\]")


@dataclass(frozen=True)
class FencedDocument:
    masked_text: str
    blocks: tuple[str, ...]
    signatures: tuple[tuple[str, int, str], ...]
    errors: tuple[str, ...]


def read_utf8(path: Path) -> str:
    try:
        return path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    except FileNotFoundError as exc:
        raise ValueError(f"file not found: {path}") from exc
    except UnicodeDecodeError as exc:
        raise ValueError(f"file is not valid UTF-8: {path}") from exc


def blank_like(line: str) -> str:
    return "\n" if line.endswith("\n") else ""


def extract_fenced_document(text: str) -> FencedDocument:
    lines = text.splitlines(keepends=True)
    masked: list[str] = []
    blocks: list[str] = []
    signatures: list[tuple[str, int, str]] = []
    errors: list[str] = []
    current: list[str] = []
    marker_char = ""
    marker_length = 0
    start_line = 0

    for line_number, line in enumerate(lines, start=1):
        bare = line[:-1] if line.endswith("\n") else line
        if not current:
            opening = FENCE_OPEN_RE.match(bare)
            if opening:
                marker = opening.group("marker")
                marker_char = marker[0]
                marker_length = len(marker)
                start_line = line_number
                current = [line]
                signatures.append((marker_char, marker_length, opening.group("info").strip()))
                masked.append(blank_like(line))
            else:
                masked.append(line)
            continue

        current.append(line)
        masked.append(blank_like(line))
        closing_re = re.compile(
            rf"^[ \t]{{0,3}}{re.escape(marker_char)}{{{marker_length},}}[ \t]*$"
        )
        if closing_re.match(bare):
            blocks.append("".join(current))
            current = []
            marker_char = ""
            marker_length = 0

    if current:
        errors.append(f"unclosed fenced code block beginning at line {start_line}")
        blocks.append("".join(current))

    return FencedDocument(
        masked_text="".join(masked),
        blocks=tuple(blocks),
        signatures=tuple(signatures),
        errors=tuple(errors),
    )


def extract_frontmatter_keys(text: str) -> tuple[str, ...]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return ()

    keys: list[str] = []
    for line in lines[1:]:
        if line.strip() in {"---", "..."}:
            return tuple(keys)
        match = FRONTMATTER_KEY_RE.match(line)
        if match:
            keys.append(f"{len(match.group('indent'))}:{match.group('key')}")
    return tuple(keys)


def mask_inline_code(text: str) -> tuple[str, tuple[str, ...]]:
    tokens: list[str] = []

    def replace(match: re.Match[str]) -> str:
        tokens.append(match.group(0))
        return " " * len(match.group(0))

    return INLINE_CODE_RE.sub(replace, text), tuple(tokens)


def pipe_count(line: str) -> int:
    count = 0
    escaped = False
    for character in line:
        if escaped:
            escaped = False
        elif character == "\\":
            escaped = True
        elif character == "|":
            count += 1
    return count


def structural_tokens(text: str) -> tuple[str, ...]:
    tokens: list[str] = []
    for line in text.splitlines():
        heading = re.match(r"^[ \t]{0,3}(#{1,6})(?:[ \t]+|$)", line)
        if heading:
            tokens.append(f"heading:{len(heading.group(1))}")

        list_item = re.match(r"^(?P<indent>[ \t]*)(?P<marker>[-+*]|\d+[.)])[ \t]+", line)
        if list_item:
            marker = list_item.group("marker")
            kind = "unordered" if marker in {"-", "+", "*"} else f"ordered:{marker[-1]}"
            task = re.match(r"^[ \t]*[-+*][ \t]+\[([ xX])\]", line)
            task_state = f":task:{task.group(1).lower()}" if task else ""
            tokens.append(f"list:{len(list_item.group('indent'))}:{kind}{task_state}")

        quote = re.match(r"^[ \t]*(?P<marks>(?:>[ \t]*)+)", line)
        if quote:
            tokens.append(f"blockquote:{quote.group('marks').count('>')}")

        if re.match(r"^[ \t]{0,3}(?:\*[ \t]*){3,}$", line):
            tokens.append("thematic:*")
        elif re.match(r"^[ \t]{0,3}(?:_[ \t]*){3,}$", line):
            tokens.append("thematic:_")
        elif re.match(r"^[ \t]{0,3}(?:-[ \t]*){3,}$", line):
            tokens.append("thematic:-")

        directive = re.match(r"^[ \t]*(?P<marks>:{3,})(?P<name>[A-Za-z0-9_-]*)", line)
        if directive:
            tokens.append(
                f"directive:{len(directive.group('marks'))}:{directive.group('name')}"
            )

        footnote = re.match(r"^[ \t]*\[\^(?P<label>[^\]]+)\]:", line)
        if footnote:
            tokens.append(f"footnote:{footnote.group('label')}")

        pipes = pipe_count(line)
        if pipes:
            tokens.append(f"pipe-row:{pipes}")

    return tuple(tokens)


def tag_tokens(text: str) -> tuple[str, ...]:
    without_comments = HTML_COMMENT_RE.sub("", text)
    return tuple(match.group(0) for match in TAG_RE.finditer(without_comments))


def link_destinations(text: str) -> tuple[str, ...]:
    return tuple(match.group(1).strip() for match in INLINE_LINK_RE.finditer(text))


def compare_sequence(
    label: str,
    source: Iterable[object],
    translated: Iterable[object],
    issues: list[str],
) -> None:
    source_items = tuple(source)
    translated_items = tuple(translated)
    if source_items == translated_items:
        return

    if len(source_items) != len(translated_items):
        issues.append(
            f"{label}: item count differs ({len(source_items)} source, "
            f"{len(translated_items)} translated)"
        )
        return

    differing = [
        str(index)
        for index, (left, right) in enumerate(zip(source_items, translated_items), start=1)
        if left != right
    ]
    preview = ", ".join(differing[:8])
    suffix = "..." if len(differing) > 8 else ""
    issues.append(f"{label}: changed item(s) {preview}{suffix}")


def validate(source_text: str, translated_text: str, allow_code_changes: bool) -> list[str]:
    issues: list[str] = []
    source_fenced = extract_fenced_document(source_text)
    translated_fenced = extract_fenced_document(translated_text)

    issues.extend(f"source: {error}" for error in source_fenced.errors)
    issues.extend(f"translated: {error}" for error in translated_fenced.errors)
    compare_sequence(
        "fenced code signatures",
        source_fenced.signatures,
        translated_fenced.signatures,
        issues,
    )
    if not allow_code_changes:
        compare_sequence("fenced code blocks", source_fenced.blocks, translated_fenced.blocks, issues)

    source_plain, source_inline = mask_inline_code(source_fenced.masked_text)
    translated_plain, translated_inline = mask_inline_code(translated_fenced.masked_text)

    compare_sequence("inline code", source_inline, translated_inline, issues)
    compare_sequence(
        "frontmatter keys",
        extract_frontmatter_keys(source_text),
        extract_frontmatter_keys(translated_text),
        issues,
    )
    compare_sequence(
        "Markdown structure",
        structural_tokens(source_plain),
        structural_tokens(translated_plain),
        issues,
    )
    compare_sequence(
        "link destinations",
        link_destinations(source_plain),
        link_destinations(translated_plain),
        issues,
    )
    compare_sequence(
        "reference definitions",
        REFERENCE_DEF_RE.findall(source_plain),
        REFERENCE_DEF_RE.findall(translated_plain),
        issues,
    )
    compare_sequence(
        "reference-use labels",
        REFERENCE_USE_RE.findall(source_plain),
        REFERENCE_USE_RE.findall(translated_plain),
        issues,
    )
    compare_sequence(
        "HTML comments",
        HTML_COMMENT_RE.findall(source_plain),
        HTML_COMMENT_RE.findall(translated_plain),
        issues,
    )
    compare_sequence("MDX/HTML tags", tag_tokens(source_plain), tag_tokens(translated_plain), issues)
    compare_sequence(
        "import/export statements",
        IMPORT_EXPORT_RE.findall(source_plain),
        IMPORT_EXPORT_RE.findall(translated_plain),
        issues,
    )
    return issues


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check that protected Markdown/MDX structures survived translation."
    )
    parser.add_argument("source", type=Path, help="English source .md or .mdx file")
    parser.add_argument("translated", type=Path, help="Thai translated .md or .mdx file")
    parser.add_argument(
        "--allow-code-changes",
        action="store_true",
        help="Allow fenced code contents to differ; use only for approved comment translation.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    for path in (args.source, args.translated):
        if path.suffix.lower() not in {".md", ".mdx"}:
            print(f"ERROR: unsupported file type: {path}", file=sys.stderr)
            return 2

    try:
        source_text = read_utf8(args.source)
        translated_text = read_utf8(args.translated)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    issues = validate(source_text, translated_text, args.allow_code_changes)
    if issues:
        print("FAIL: protected Markdown/MDX content differs:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("PASS: protected Markdown/MDX structures match.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
