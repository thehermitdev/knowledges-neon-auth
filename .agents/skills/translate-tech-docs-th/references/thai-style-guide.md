# Thai Style Guide

## Audience and voice

- Write for beginner-to-intermediate full-stack developers.
- Use clear, natural Thai that sounds like an experienced developer explaining the subject to a junior.
- Prefer concise sentences and explicit subjects when the English source relies on ambiguous pronouns.
- Use `ครับ` sparingly in conversational tutorials. Do not add it to headings, API references, terse warnings, or every sentence.
- Avoid stiff academic language, slang, and unnecessary encouragement not present in the source.

## Terminology order

Choose terms in this order:

1. Keep official product, library, framework, protocol, API, class, function, and configuration names exactly.
2. Use a Thai term already common among Thai developers when it is precise.
3. Use a natural Thai transliteration for a widely borrowed technical term.
4. Retain the English term in parentheses only when it disambiguates the concept; put the explanation in the companion notes.

Examples:

| English | Preferred Thai treatment |
| --- | --- |
| cache | แคช |
| dependency | dependency or การพึ่งพา ตามบริบท; explain in notes |
| request | request or คำขอ ตามบริบท |
| render | เรนเดอร์ |
| middleware | middleware; explain in notes |
| PostgreSQL | `PostgreSQL` |
| `useQuery` | `useQuery` |

Do not force one Thai word across different meanings. For example, translate `state` according to whether it means UI state, application state, or a geographic state.

## Semantic fidelity

- Preserve all facts, steps, examples, constraints, prerequisites, and outcomes.
- Preserve modality precisely: distinguish must, should, may, can, and cannot.
- Preserve negative statements and exception boundaries.
- Preserve singular/plural distinctions when they affect behavior.
- Preserve version numbers, defaults, units, limits, and comparison direction.
- Preserve uncertainty. Do not strengthen `may` into a guarantee.
- Do not add advice, claims, or implementation details to the primary translation.

## Companion notes

Use this shape when notes are useful:

```markdown
# คำอธิบายประกอบ: <ชื่อเอกสาร>

## ศัพท์สำคัญ

| คำศัพท์ | ใช้ในฉบับแปล | ความหมายในบริบทนี้ |
| --- | --- | --- |

## แนวคิดที่ควรรู้

<Short explanations or analogies>

## จุดที่มักเข้าใจผิด

<Only when useful>
```

- Keep notes shorter than the translated document.
- Explain only concepts that materially help the target reader.
- Mark an analogy as an analogy and state where it stops matching reality.
- Do not copy long passages from the source into notes.
