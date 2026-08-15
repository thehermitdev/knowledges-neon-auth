# Markdown and MDX Preservation Rules

## Preserve the document skeleton

- Keep frontmatter delimiters, key order, nesting, and non-prose values.
- Translate only clearly human-facing frontmatter values such as `title`, `description`, or `summary`.
- Keep heading levels, section order, list nesting, numbering style, task states, blockquotes, admonitions, table shape, footnotes, and thematic breaks.
- Keep reference identifiers stable even when visible link text is translated.
- Keep HTML comments unchanged.

## Protect code and machine-readable text

Keep these exact by default:

- Fenced and indented code.
- Fence characters, length, language labels, and metadata.
- Inline code.
- Terminal commands and command output.
- File paths, package names, environment variables, identifiers, flags, and literal values.
- Regular expressions, query strings, JSON keys, YAML keys, and configuration keys.

Translate comments inside code only when the user explicitly requests it. Preserve whitespace, executable tokens, and all non-comment text when doing so.

## Preserve links and media

- Translate visible link labels and image alt text when appropriate.
- Keep URL destinations, anchors, reference destinations, and optional link titles unchanged.
- Do not repair or normalize a source URL unless the user separately requests it.
- Check relative links after mirroring files under the target root; report broken paths instead of silently rewriting architecture.

## Preserve MDX

Keep these exact:

- `import` and `export` statements.
- Component and element names.
- JSX/HTML tags, attributes, prop names, and expression braces.
- JavaScript or TypeScript expressions.
- ESM blocks, comments, and directives.

Translate only prose text nodes and Markdown prose outside protected expressions. If prose exists inside a JSX string prop, leave it unchanged unless the project instructions explicitly identify that prop as translatable.

## Preserve tables and special blocks

- Keep the same table columns and alignment markers.
- Translate prose inside cells without moving data between columns.
- Preserve directive and admonition names, markers, attributes, and nesting.
- Translate their visible titles and bodies only when those parts are ordinary prose.
- Preserve escaped characters and entity syntax when changing them could alter rendering.

## Avoid structural drift

- Do not add explanations, summaries, examples, or new headings to the translated document.
- Do not merge or split sections.
- Do not remove repeated text merely because it appears redundant.
- Avoid reflowing paragraphs unless necessary for correct Thai rendering.
- Put all educational additions in the companion notes file.
