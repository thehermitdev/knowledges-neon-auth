---
name: translate-tech-docs-th
description: Translate authorized English technology documentation in Markdown or MDX into natural Thai for beginner-to-intermediate full-stack developers while preserving document structure, code, identifiers, links, and MDX syntax. Use when Codex is asked to translate one or more .md/.mdx technical documents, documentation folders, tutorials, conceptual guides, or API references into a mirrored th/ output tree and optionally produce separate Thai learning notes without inserting explanations into the translated document.
---

# Translate Technology Documentation to Thai

Translate technical prose faithfully while protecting every machine-sensitive part of Markdown and MDX. Keep explanations outside the translated document so the primary output remains structurally aligned with its source.

## Read the Required Guidance

Before planning or translating, read:

- `references/thai-style-guide.md` for terminology, tone, and semantic fidelity.
- `references/markdown-mdx-preservation.md` for protected syntax and content.

Before final delivery, read `references/quality-checklist.md` and apply every relevant check.

## Follow the Workflow

### 1. Establish scope and authority

- Accept only `.md` and `.mdx` sources.
- Translate only user-authored, user-provided, openly licensed, or otherwise authorized material. Ask for confirmation when authorization is unclear.
- Read the nearest applicable project instructions such as `AGENTS.md` before inspecting source files.
- Identify the source root, target root, requested files, and exclusions. Exclude existing translation targets, generated output, dependency folders, and build artifacts.
- Use English-to-Thai as the default direction. Ask before handling another source language.

### 2. Read before translating

- Read each complete source file before editing any translation.
- For a large file set, inventory all files first and propose safe batches.
- Identify document purpose, intended reader, recurring terminology, cross-file links, hard concepts, and MDX components.

### 3. Present a plan and pause

Present a short plan containing:

- Source files and exact output paths.
- Terminology or product names that require consistent treatment.
- Complex concepts that merit separate learning notes.
- Validation steps and any known limitations.

Wait for explicit user confirmation. Do not create translated files before confirmation.

### 4. Map outputs deterministically

- Honor a user-specified target root.
- Otherwise use `th/` as the target root.
- Preserve every source-relative directory and filename under the target root.
- Map `docs/guide/setup.mdx` to `th/docs/guide/setup.mdx` when the source root is the current project root.
- Store optional explanations at `th/_notes/<relative-parent>/<stem>.notes.md`.
- Do not place learning notes inside the translated file.

### 5. Translate the primary document

- Translate all human-readable prose without omitting, summarizing, or inventing content.
- Preserve block order and Markdown/MDX structure.
- Preserve code, commands, identifiers, paths, URLs, product names, API names, and syntax exactly unless the user explicitly authorizes a narrow exception.
- Preserve requirement strength, conditions, warnings, negation, version constraints, and causal relationships.
- Apply one consistent Thai term for each source concept across the file set.
- Keep comments inside code unchanged by default. Translate only comments when explicitly requested, and change nothing else in the code block.

### 6. Create separate learning notes

- Create a notes file only when the document contains terminology or concepts that benefit from explanation.
- Explain concepts for beginner-to-intermediate full-stack developers without duplicating the full source.
- Include a compact glossary and practical context when useful.
- Label interpretations or additional examples clearly; never present them as source content.
- Omit the notes file when the user requests translation only.

### 7. Validate and review

Run the bundled validator for every source/output pair:

```bash
python3 <skill-dir>/scripts/validate_translation.py SOURCE.md th/SOURCE.md
```

If the user explicitly requested translated comments inside fenced code, run:

```bash
python3 <skill-dir>/scripts/validate_translation.py \
  SOURCE.md th/SOURCE.md --allow-code-changes
```

- Treat validator failures as blockers. Inspect and fix the output, then rerun it.
- Use `references/quality-checklist.md` for semantic checks the script cannot perform.
- Re-read the full translated file once after validation.

### 8. Report completion

- List translated files and any companion notes.
- Report validation results and any intentionally preserved English terms.
- Mention unresolved ambiguities instead of silently choosing a meaning.
- Link user-facing output files when the environment supports file links.

## Handle Conflicts

Apply this priority order:

1. User instructions for the current task.
2. Applicable repository instructions such as `AGENTS.md`.
3. This skill's defaults.

Never relax syntax protection merely to make Thai prose read more smoothly. Ask when a requested translation would make executable or machine-readable content ambiguous.
