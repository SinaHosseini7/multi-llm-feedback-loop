# Repository Structure Guide

**Purpose:** This document defines where every piece of content from `CONTENT_WRITING_GUIDE.md` physically lives in the repository. It implements the hybrid model: **one comprehensive file** that contains condensed explanations of everything, plus **specialized deep-dive files** for readers who want full depth on a specific topic.

> **Revision note (this pass).** This file was reconciled with `CONTENT_WRITING_GUIDE.md`; several inconsistencies between the two are now fixed. The folder tree, mapping table, and build order below are the single source of truth. Substantive changes are logged in **Appendix A: Changelog**. Short version: the phantom `docs/06-case-study.md` is gone (the case study lives in `case-study/`), the duplicative `docs/glossary.md` is removed (the cheat sheet is README-only), the critique-request template now has a reserved file, and the diagram is inline Mermaid rather than a required PNG.

## Design Rationale

- **`README.md` as the comprehensive file:** GitHub renders `README.md` automatically on the repo's landing page, so it's the natural home for the "read top to bottom and understand everything" experience. It should be complete on its own — a reader who never clicks into `docs/` or `case-study/` should still walk away understanding every technique and the full tutorial.
- **`docs/` for prose deep dives:** Keeping specialized files in a `docs/` folder is standard GitHub convention, keeps the repo root uncluttered, and — as a side benefit — is exactly the folder GitHub Pages expects if you ever want to publish this as a browsable site later. You don't need to set up Pages now; this just means you won't have to restructure anything if you do it in six months.
- **Numbered filenames:** Prefixing deep-dive files with numbers (`02-`, `03-`…) that match the ToC section numbers keeps sidebar/file-explorer ordering aligned with reading order — GitHub's file browser sorts alphabetically, so this is the only way to control order without a Pages nav config. Note that `docs/` intentionally has no `01`, `06`, `08`, or `09`: Section 1 (Intro), 8 (Cheat Sheet), and 9 (References) have no deep dive, and Section 6 (Case Study) lives in its own top-level folder (below), not in `docs/`.
- **`case-study/` as its own top-level folder, not under `docs/`:** The Flappy Bird experiment produces actual runnable code (four versions of it) alongside its write-up — that's a different kind of artifact than a prose deep-dive, so it gets its own space. **`case-study/README.md` *is* the full Section 6 deep-dive.** (There is deliberately no `docs/06-case-study.md`; the content guide agrees.)
- **`assets/` for anything visual:** Screenshots from the Flappy Bird case study live outside the markdown files so they can be reused without duplication. **Diagrams are inline Mermaid by default** (rendered natively by GitHub, version-controlled as text), so `assets/diagrams/` is now an *optional* slot reserved only for a future polished/exported PNG — not required for v1.

## Folder Tree

```
multi-llm-feedback-loop/
│
├── README.md                          ← THE comprehensive file (Sections 1–9, condensed)
├── LICENSE
├── CONTRIBUTING.md                     ← optional, only if you want external contributions
│
├── docs/                               ← specialized prose deep-dive files (full depth)
│   ├── 02-foundations.md               ← Section 2 in full: shot-types + efficiency tradeoff
│   ├── 03-toolkit.md                   ← Section 3 in full: all toolkit techniques, per-technique detail
│   ├── 04-feedback-loop.md             ← Section 4 in full: the core technique, extended examples
│   ├── 05-master-tutorial.md           ← Section 5 in full: the 5-part framework, worked walkthrough
│   └── 07-pitfalls.md                  ← Section 7 in full: extended pitfall examples (optional)
│
├── case-study/                         ← Section 6: Flappy Bird Experiment (full deep-dive + artifacts)
│   ├── README.md                       ← full Section 6 write-up (the case-study deep-dive itself)  [DONE]
│   ├── 01-zero-shot/
│   │   ├── prompt.md                   ← the exact zero-shot prompt  [DONE]
│   │   ├── flappy_bird.py              ← generated code (verbatim)  [DONE]
│   │   └── evaluation.md               ← functional-review notes    [DONE — gpt-oss score pending]
│   ├── 02-standard/
│   │   ├── prompt.md                   ← the exact standard prompt   [DONE]
│   │   ├── flappy_bird.py              ← generated code (verbatim)  [DONE]
│   │   └── evaluation.md               ← functional-review notes    [DONE — gpt-oss score pending]
│   ├── 03-advanced-feedback-loop/
│   │   ├── 00-critique-request-template.md  ← reusable template pasted to each Critic  [READY NOW]
│   │   ├── 01-architect-draft.md       ← Architect's Draft v1 prompt [READY NOW — see prompt pack]
│   │   ├── 02-critic-feedback/          ← one file per Critic model  [STUBS — paste transcripts]
│   │   │   ├── critic-gpt-oss.md        ← gpt-oss:20b critique
│   │   │   ├── critic-qwen.md           ← qwen3.6:27b critique
│   │   │   ├── critic-gemma.md          ← gemma4:26b critique
│   │   │   └── critic-phi4.md           ← phi4-reasoning:14b critique
│   │   ├── 03-final-prompt.md           ← synthesized final prompt   [DONE]
│   │   ├── flappy_bird.py               ← generated code (verbatim)  [DONE]
│   │   └── evaluation.md                ← functional-review notes    [DONE — gpt-oss score pending]
│   └── benchmark-results.md             ← comparison table across all 3 stages  [DONE — gpt-oss score pending]
│
├── assets/
│   ├── diagrams/                        ← OPTIONAL — only for a future exported PNG; v1 uses inline Mermaid
│   └── screenshots/
│       └── (Flappy Bird gameplay screenshots, if desired)
│
└── planning/                           ← your own working files, not meant for readers
    ├── CONTENT_WRITING_GUIDE.md         ← the content briefing doc
    └── REPOSITORY_STRUCTURE_GUIDE.md    ← this file
```

**Three model roles in `case-study/` (added this revision).** The case-study folder involves three distinct model roles that must not be conflated; the folder layout reflects them:

- **Architect & Critic models** produce *prompts* and appear only under `03-advanced-feedback-loop/`. **Roster as run:** Architect draft = Claude Opus 4.8; Critics = `gpt-oss:20b`, `qwen3.6:27b`, `gemma4:26b`, `phi4-reasoning:14b`; synthesis = Claude Sonnet 5.
- **The code-generation model** *executes* each stage's final prompt and produces every `flappy_bird.py`. **Held constant** = `gpt-oss:20b`, so the prompting technique is the only variable. Named at the top of `case-study/README.md`.
- **The evaluator** grades each `flappy_bird.py` and produces every `evaluation.md` and `benchmark-results.md`. Intended: `gpt-oss:20b` + fixed rubric; Run 1's committed scores are an independent functional review (⚠️ `gpt-oss:20b` was also generator + a critic → self-preference risk; use a distinct grader in v2). It never writes or runs prompts.

## Content-to-File Mapping

| Section | Condensed version lives in | Full version lives in |
|---|---|---|
| 1. Introduction | `README.md` | — (short by design, no deep dive needed) |
| 2. Foundations | `README.md` | `docs/02-foundations.md` |
| 3. Toolkit | `README.md` | `docs/03-toolkit.md` |
| 4. Feedback Loop | `README.md` (full — this is your core content, don't over-condense it) | `docs/04-feedback-loop.md` (extended examples only) |
| 5. Master Tutorial | `README.md` | `docs/05-master-tutorial.md` |
| 6. Case Study | `README.md` (results table + interpretive paragraph) | `case-study/README.md` + per-stage folders |
| 7. Best Practices | `README.md` | `docs/07-pitfalls.md` (optional, only if you want extended examples) |
| 8. Cheat Sheet | `README.md` **only** | **not duplicated** — its value is being in one bookmarkable place (no `docs/glossary.md`) |
| 9. References | `README.md` | — |

## Linking Convention

At the start of every condensed section in `README.md`, add a one-line pointer to its deep-dive counterpart, e.g.:

```markdown
## 3. The Prompt Engineering Toolkit
*For full definitions, examples, and tradeoffs per technique, see [docs/03-toolkit.md](docs/03-toolkit.md).*
```

For Section 6, the pointer targets the case-study folder instead of `docs/`:

```markdown
## 6. Case Study: The Flappy Bird Experiment
*For the full prompts, generated code, per-critic feedback, and scoring, see [case-study/README.md](case-study/README.md).*
```

This keeps `README.md` skimmable while making the deeper content discoverable without forcing every reader into it.

## Naming Conventions

- All markdown filenames: lowercase, hyphen-separated (`feedback-loop.md`, not `FeedbackLoop.md` or `feedback_loop.md`) — matches GitHub/Pages convention and avoids case-sensitivity issues across OSes.
- Deep-dive files in `docs/` are prefixed with their `README.md` section number so file order in GitHub's UI matches reading order.
- Files inside `case-study/03-advanced-feedback-loop/` are prefixed by *step* order (`00-` template, `01-` draft, `02-` critiques, `03-` final) so the folder reads as the procedure it documents.
- Per-critic files are named by vendor (`critic-gpt.md`, `critic-gemini.md`, `critic-deepseek.md`) rather than `critic-a/b/c`, so it's obvious which lineage produced which critique.
- Code files use standard language conventions (`flappy_bird.py`, snake_case) regardless of the markdown convention above.
- Diagrams are authored inline as Mermaid code blocks; if you later export a polished image, name it `feedback-loop-flow.png` under `assets/diagrams/`.

## Build Order & Status

The experiment has been run once, so the case-study branch is largely populated. Remaining work is the prose deep-dives, the top-level README, and two small pieces of pasted-in data.

1. **Case-study prompt pack — ✅ DONE.** `00-critique-request-template.md`, `01-zero-shot/prompt.md`, `02-standard/prompt.md`, `03-advanced-feedback-loop/01-architect-draft.md`.
2. **Experiment run — ✅ DONE.** Draft → 4 critics → Sonnet 5 synthesis → `gpt-oss:20b` generated all three `flappy_bird.py` files.
3. **Case-study result files — ✅ MOSTLY DONE.** `03-final-prompt.md` (verbatim), all three `flappy_bird.py` (verbatim), all three `evaluation.md`, `benchmark-results.md`, and `case-study/README.md` are written from the real Run 1 data. **Two pending inputs:** paste the four raw critic transcripts into `02-critic-feedback/*` (currently stubs), and, if you ran the grading step, paste `gpt-oss:20b`'s rubric scores into the "pending" rows.
4. **Prose deep-dives — ⬜ TODO (no experiment needed):** `docs/02-foundations.md` → `docs/03-toolkit.md` → `docs/04-feedback-loop.md` → `docs/05-master-tutorial.md`.
5. **`docs/07-pitfalls.md`** — ⬜ optional.
6. **`README.md` last — ⬜ TODO** — condense each finished deep-dive into its summary section, embed the benchmark table and the Mermaid diagram, and write Section 1 (Introduction), Section 8 (Cheat Sheet), and Section 9 (References) fresh. A working draft is provided at the repo root (`README.md`) for the assembling model to refine; §6 there must preserve the honest, non-monotonic Run 1 finding.

## Appendix A: Changelog (what changed this revision and why)

- **Removed `docs/06-case-study.md` as a concept.** The content guide previously pointed there; the case study lives in `case-study/README.md`. *Why:* the two files disagreed, and the runnable-code artifact belongs in its own top-level folder — which this guide's own mapping table already implied.
- **Removed `docs/glossary.md`.** *Why:* it duplicated the Section 8 cheat sheet, contradicting the content guide *and* this file's own mapping-table row ("not duplicated"). The tree was the outlier; it now matches.
- **Added `case-study/03-advanced-feedback-loop/00-critique-request-template.md`.** *Why:* the content guide (5.3) and the prompt pack both require a standardized critique template, but the tree had no reserved file for it.
- **Renamed `critic-a/b/c.md` → `critic-gpt/gemini/deepseek.md`.** *Why:* ties each critique to a named lineage from the locked roster, so the diversity-of-critics premise is legible from the file names.
- **Diagram is inline Mermaid; `assets/diagrams/` demoted to optional.** *Why:* GitHub renders Mermaid natively and it version-controls as text — better than a required binary PNG for a v1 that will change.
- **Build order now flags the experiment dependency and the "ready now vs. after you run it" split.** *Why:* prevents you from trying to draft result files before the data exists, and makes the handoff explicit.
- **Added the three-role note to the case-study section.** *Why:* mirrors the content guide so the folder layout can't be misread.

## Appendix B: Post-Run-1 updates

- **Critic filenames now match the models actually used:** `critic-gpt-oss.md`, `critic-qwen.md`, `critic-gemma.md`, `critic-phi4.md` (was the hypothetical gpt/gemini/deepseek set). *Why:* the run used four local open-weight critics, not frontier API models.
- **Roster in the three-role note updated to the real run**, including the Opus-draft / Sonnet-synthesis split and the `gpt-oss:20b` generator = grader = critic self-preference caveat.
- **Status markers added throughout the tree** (`[DONE]` / stubs / pending) so the assembling model knows exactly what exists and what still needs pasted-in data.
- **A top-level `README.md` draft was added** to the deliverables so the repo can be assembled turnkey; it is a draft for refinement, not a frozen file.
