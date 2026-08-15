# Translation Quality Checklist

## Scope and files

- [ ] Every approved `.md` or `.mdx` source has exactly one translated counterpart.
- [ ] Output paths mirror the agreed relative paths under `th/` or the user-specified target.
- [ ] No source, dependency, generated, or unrelated file was modified.
- [ ] Companion notes, when present, live under `_notes/` and not inside primary translations.

## Completeness and meaning

- [ ] Every heading, paragraph, list item, callout, table cell, caption, and visible label is accounted for.
- [ ] The translation does not summarize, omit, duplicate, or invent source content.
- [ ] Requirements, prohibitions, warnings, conditions, and exceptions retain their strength.
- [ ] Numbers, versions, units, limits, defaults, and comparison directions match the source.
- [ ] Pronouns and technical subjects resolve to the correct entity.
- [ ] Repeated terminology is consistent across all translated files.

## Technical integrity

- [ ] Fenced code and inline code remain exact unless a narrow exception was approved.
- [ ] Commands, identifiers, paths, product names, API names, and literals remain exact.
- [ ] Markdown hierarchy, list nesting, tables, links, and reference identifiers remain valid.
- [ ] MDX imports, exports, components, props, expressions, and tags remain valid.
- [ ] Relative links and anchors still resolve in the mirrored output structure.

## Thai readability

- [ ] Thai sentences are natural for beginner-to-intermediate full-stack developers.
- [ ] English technical terms are retained only where they improve precision.
- [ ] Transliteration and capitalization are consistent.
- [ ] No explanation or analogy has leaked into the primary translation.
- [ ] Companion notes are useful, concise, and clearly separate source meaning from added teaching context.

## Final verification

- [ ] `validate_translation.py` passes for every source/output pair.
- [ ] Each complete translated file has been re-read after automated validation.
- [ ] Any ambiguity or intentional exception is reported to the user.
