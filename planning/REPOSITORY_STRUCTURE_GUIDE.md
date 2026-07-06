# Repository Structure Guide

**Purpose:** This document defines where every piece of content from `CONTENT_WRITING_GUIDE.md` physically lives in the repository. It implements the hybrid model: **one comprehensive file** that contains condensed explanations of everything, plus **specialized deep-dive files** for readers who want full depth on a specific topic.

> **Revision note (this pass).** This revision updates the folder tree and status markers to match the real, current state of the repository: all four critic transcripts under `02-critic-feedback/` are finalized and committed (no longer stubs), and `LICENSE`, `CONTRIBUTING.md`, and `.gitignore` are confirmed present at the repo root. Two items remain genuinely open and are flagged everywhere they're relevant rather than buried in one table: the grading-model decision (and the re-scoring it requires), and gameplay screenshots. The diagram approach (inline Mermaid) is confirmed final — no PNG export is planned. Full change log in **Appendix A**.

## Design Rationale

- **`README.md` as the comprehensive file:** GitHub renders `README.md` automatically on the repo's landing page, so it's the natural home for the "read top to bottom and understand everything" experience. It should be complete on its own — a reader who never clicks into `docs/` or `case-study/` should still walk away understanding every technique and the full tutorial. **A working full draft exists at the repo root now** — it has been reviewed and is structurally sound; no reorganization is needed. Treat further edits to it as a *content refinement* pass (matching the eventual `docs/` deep-dives once they're written), not a restructuring task.
- **`docs/` for prose deep dives:** Keeping specialized files in a `docs/` folder is standard GitHub convention, keeps the repo root uncluttered, and — as a side benefit — is exactly the folder GitHub Pages expects if you ever want to publish this as a browsable site later. You don't need to set up Pages now; this just means you won't have to restructure anything if you do it in six months.
- **Numbered filenames:** Prefixing deep-dive files with numbers (`02-`, `03-`…) that match the ToC section numbers keeps sidebar/file-explorer ordering aligned with reading order — GitHub's file browser sorts alphabetically, so this is the only way to control order without a Pages nav config. Note that `docs/` intentionally has no `01`, `06`, `08`, or `09`: Section 1 (Intro), 8 (Cheat Sheet), and 9 (References) have no deep dive, and Section 6 (Case Study) lives in its own top-level folder (below), not in `docs/`.
- **`case-study/` as its own top-level folder, not under `docs/`:** The Flappy Bird experiment produces actual runnable code (three versions of it) alongside its write-up — that's a different kind of artifact than a prose deep-dive, so it gets its own space. **`case-study/README.md` *is* the full Section 6 deep-dive**, and it's written and current with Run 1 data.
- **`assets/` for anything visual:** Screenshots from the Flappy Bird case study are the one visual asset still queued — see Build Order below. **Diagrams are inline Mermaid by default** (rendered natively by GitHub, version-controlled as text) — this has been reviewed and confirmed as the permanent v1 (and likely permanent, period) approach. `assets/diagrams/` remains reserved but unused; there is no plan to populate it.

## Folder Tree

```
multi-llm-feedback-loop/
│
├── README.md                          ← THE comprehensive file (Sections 1–9, condensed)  [DRAFT WRITTEN — reviewed, structurally final]
├── LICENSE                             [PRESENT]
├── CONTRIBUTING.md                     [PRESENT]
├── .gitignore                          [PRESENT]
│
├── docs/                               ← specialized prose deep-dive files (full depth)
│   ├── 02-foundations.md               ← Section 2 in full: shot-types + efficiency tradeoff        [TODO — next writing task]
│   ├── 03-toolkit.md                   ← Section 3 in full: all toolkit techniques, per-technique detail [TODO]
│   ├── 04-feedback-loop.md             ← Section 4 in full: core technique, extended examples       [TODO — now unblocked to use real critic transcripts as worked examples]
│   ├── 05-master-tutorial.md           ← Section 5 in full: the 5-part framework, worked walkthrough [TODO]
│   └── 07-pitfalls.md                  ← Section 7 in full: extended pitfall examples (optional)     [OPTIONAL / LOWEST PRIORITY]
│
├── case-study/                         ← Section 6: Flappy Bird Experiment (full deep-dive + artifacts)
│   ├── README.md                       ← full Section 6 write-up  [DONE]
│   ├── 01-zero-shot/
│   │   ├── prompt.md                   ← the exact zero-shot prompt                    [DONE]
│   │   ├── flappy_bird.py              ← generated code (verbatim)                    [DONE]
│   │   └── evaluation.md               ← functional-review notes                      [DONE — grading-model score still pending, see below]
│   ├── 02-standard/
│   │   ├── prompt.md                   ← the exact standard prompt                     [DONE]
│   │   ├── flappy_bird.py              ← generated code (verbatim)                    [DONE]
│   │   └── evaluation.md               ← functional-review notes                      [DONE — grading-model score still pending]
│   ├── 03-advanced-feedback-loop/
│   │   ├── 00-critique-request-template.md  ← reusable template pasted to each Critic  [DONE]
│   │   ├── 01-architect-draft.md       ← Architect's Draft v1 prompt                   [DONE]
│   │   ├── 02-critic-feedback/          ← one file per Critic model                    [ALL FOUR DONE]
│   │   │   ├── critic-gpt-oss.md        ← gpt-oss:20b critique                          [DONE]
│   │   │   ├── critic-qwen.md           ← qwen3.6:27b critique                          [DONE — verified identical to raw model output]
│   │   │   ├── critic-gemma.md          ← gemma4:26b critique                           [DONE]
│   │   │   └── critic-phi4.md           ← phi4-reasoning:14b critique                   [DONE]
│   │   ├── 03-final-prompt.md           ← synthesized final prompt                     [DONE]
│   │   ├── flappy_bird.py               ← generated code (verbatim)                    [DONE]
│   │   └── evaluation.md                ← functional-review notes                      [DONE — grading-model score still pending]
│   └── benchmark-results.md             ← comparison table across all 3 stages          [DONE — grading-model scores still pending]
│
├── assets/
│   ├── diagrams/                        ← RESERVED, UNUSED — inline Mermaid is the confirmed permanent approach; no PNG planned
│   └── screenshots/
│       └── (Flappy Bird gameplay screenshots — QUEUED, not yet added: one per stage, 01/02/03)
│
└── planning/                           ← your own working files, not meant for readers
    ├── CONTENT_WRITING_GUIDE.md         ← the content briefing doc
    └── REPOSITORY_STRUCTURE_GUIDE.md    ← this file
```

**Three model roles in `case-study/` — status update.** The case-study folder involves three distinct model roles that must not be conflated; the folder layout reflects them:

- **Architect & Critic models** produce *prompts* and appear only under `03-advanced-feedback-loop/`. **Roster as run, final:** Architect draft = Claude Opus 4.8; Critics = `gpt-oss:20b`, `qwen3.6:27b`, `gemma4:26b`, `phi4-reasoning:14b` — **all four transcripts are committed, nothing outstanding here.** Synthesis = Claude Sonnet 5.
- **The code-generation model** *executes* each stage's final prompt and produces every `flappy_bird.py`. **Held constant** = `gpt-oss:20b`, so the prompting technique is the only variable. This is done and unaffected by any remaining open task. Named at the top of `case-study/README.md`.
- **The evaluator** grades each `flappy_bird.py` and produces every `evaluation.md` and `benchmark-results.md`. **This is the one role not yet finalized.** Run 1's committed scores are an independent functional review, not output from a dedicated grading model — because the originally intended grader (`gpt-oss:20b`) was also the generator and one of the four critics, which risks self-preference bias. **Next-update task:** choose a grader from a different lineage than the generator, fix its reasoning-effort setting, score each program 3× and average, then update `evaluation.md` (×3) and `benchmark-results.md` with the results.

## Content-to-File Mapping

| Section | Condensed version lives in | Full version lives in | Status |
|---|---|---|---|
| 1. Introduction | `README.md` | — (no deep dive needed) | Done |
| 2. Foundations | `README.md` | `docs/02-foundations.md` | README done; deep dive TODO |
| 3. Toolkit | `README.md` | `docs/03-toolkit.md` | README done; deep dive TODO |
| 4. Feedback Loop | `README.md` (full) | `docs/04-feedback-loop.md` (extended examples only) | README done; deep dive TODO (use real critic transcripts) |
| 5. Master Tutorial | `README.md` | `docs/05-master-tutorial.md` | README done; deep dive TODO |
| 6. Case Study | `README.md` (results table + interpretive paragraph) | `case-study/README.md` + per-stage folders | Content done; grading scores pending; screenshots pending |
| 7. Best Practices | `README.md` | `docs/07-pitfalls.md` (optional) | README done; deep dive optional |
| 8. Cheat Sheet | `README.md` **only** | **not duplicated** | Done |
| 9. References | `README.md` | — | Done |

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

This keeps `README.md` skimmable while making the deeper content discoverable without forcing every reader into it. **This convention is already followed correctly in the current `README.md` draft — no changes needed here.**

## Naming Conventions

- All markdown filenames: lowercase, hyphen-separated (`feedback-loop.md`, not `FeedbackLoop.md` or `feedback_loop.md`) — matches GitHub/Pages convention and avoids case-sensitivity issues across OSes.
- Deep-dive files in `docs/` are prefixed with their `README.md` section number so file order in GitHub's UI matches reading order.
- Files inside `case-study/03-advanced-feedback-loop/` are prefixed by *step* order (`00-` template, `01-` draft, `02-` critiques, `03-` final) so the folder reads as the procedure it documents.
- Per-critic files are named by vendor (`critic-gpt-oss.md`, `critic-qwen.md`, `critic-gemma.md`, `critic-phi4.md`) rather than `critic-a/b/c`, so it's obvious which lineage produced which critique. **This naming is already correctly applied and all four files exist — confirmed this pass.**
- Code files use standard language conventions (`flappy_bird.py`, snake_case) regardless of the markdown convention above.
- Diagrams are authored inline as Mermaid code blocks. **No exported-image naming convention is needed going forward** — the earlier placeholder convention (`feedback-loop-flow.png` under `assets/diagrams/`) is retained here only for reference in case you ever change your mind, but there is currently no plan to use it.
- **When you eventually add screenshots**, use a simple stage-matched convention to keep them self-explanatory: `assets/screenshots/01-zero-shot.png`, `02-standard.png`, `03-advanced.png` (add `-2`, `-3` suffixes if you want more than one per stage).

## Build Order & Status

The experiment has been run once, all four critic transcripts are now in, and the housekeeping files are confirmed present. Remaining work is narrower than before: two data/scoring tasks, then the four prose deep-dives, then a final consistency pass on `README.md`.

1. **Case-study prompt pack — ✅ DONE.** `00-critique-request-template.md`, `01-zero-shot/prompt.md`, `02-standard/prompt.md`, `03-advanced-feedback-loop/01-architect-draft.md`.
2. **Experiment run — ✅ DONE.** Draft → 4 critics → Sonnet 5 synthesis → `gpt-oss:20b` generated all three `flappy_bird.py` files.
3. **Case-study result files — ✅ DONE except grading.** `03-final-prompt.md` (verbatim), all three `flappy_bird.py` (verbatim), all three `evaluation.md`, `benchmark-results.md`, and `case-study/README.md` are written from the real Run 1 data. **All four raw critic transcripts are now in** (`02-critic-feedback/*` — no longer stubs). **The one remaining input:** choose a grading model distinct from the generator/critics, run it (3× per program, averaged, fixed reasoning-effort), and paste the real scores into the "pending" rows of the three `evaluation.md` files and `benchmark-results.md`.
4. **Screenshots — ⬜ TODO.** One gameplay screenshot per stage into `assets/screenshots/`, referenced from `case-study/README.md`.
5. **Prose deep-dives — ⬜ TODO (no experiment needed):** `docs/02-foundations.md` → `docs/03-toolkit.md` → `docs/04-feedback-loop.md` → `docs/05-master-tutorial.md`. Note: 04 and 05 can now draw on the real, finalized critic transcripts for their worked examples, which wasn't possible before this update.
6. **`docs/07-pitfalls.md`** — ⬜ optional.
7. **`README.md` — ⬜ final consistency pass (not a rewrite).** The current draft has already been reviewed and is structurally sound. Once the `docs/` deep-dives exist, do a pass to make sure the condensed sections still match them in tone and emphasis, and update Section 6's language if the grading-model re-scoring changes the story materially (see the Content Writing Guide's note on not smoothing over the non-monotonic result).

## Appendix A: Changelog (what changed this revision and why)

- **All four critic files marked DONE.** `critic-gpt-oss.md`, `critic-gemma.md`, and `critic-phi4.md` were previously stubs; `critic-qwen.md` has been checked against the raw model output and confirmed identical. The folder tree, mapping table, and build order no longer describe `02-critic-feedback/` as partially populated. *Why:* this was directly confirmed as complete.
- **LICENSE, CONTRIBUTING.md, and .gitignore marked PRESENT at the repo root.** *Why:* directly confirmed; previously `CONTRIBUTING.md` was listed as optional/uncertain in the tree with no confirmation either way.
- **Diagram status changed from "locked decision" to "confirmed final, reviewed."** No PNG export is planned; `assets/diagrams/` stays reserved but explicitly unused going forward. *Why:* the inline Mermaid diagram has now been reviewed by you directly and approved as-is, which is a stronger status than merely "decided in planning."
- **Grading-model decision separated out as the single flagged open task**, called out in the folder tree, the model-roles note, the build order, and its own line — rather than living only inside a "Locked Decisions" appendix where it could be missed. *Why:* it's the most consequential remaining task (it changes real benchmark numbers), so it needed to be visible everywhere relevant, not just once.
- **Screenshots added to the folder tree and build order as an explicit queued task**, with a suggested naming convention (`01-zero-shot.png`, etc.) since none previously existed. *Why:* newly confirmed as planned but not yet done, and the guide had no naming convention ready for when you do add them.
- **`README.md` status changed from "TODO, draft provided" to "draft written and reviewed, structurally final."** Remaining work on it is now scoped explicitly as a *consistency pass* against the eventual deep-dives, not a restructuring or first-draft task. *Why:* you've now reviewed the draft and confirmed it's in good shape; the guide should reflect that it's past the "build it" stage.
- **Build order renumbered and tightened** to reflect that only two data-dependent tasks remain (grading, screenshots) before the four deep-dive docs, rather than describing the case study as having multiple pending pieces.

## Appendix B: Reference — what "Run 1" actually produced (for continuity across future sessions)

Keeping this here so a future update doesn't have to reconstruct it from scratch:

- **Roster as run:** Architect draft = Claude Opus 4.8; four open-weight critics = `gpt-oss:20b`, `qwen3.6:27b`, `gemma4:26b`, `phi4-reasoning:14b` (all four transcripts finalized); synthesis = Claude Sonnet 5; generator = `gpt-oss:20b` (held constant across all three stages).
- **Result shape:** prompt quality improved sharply and monotonically across the three stages; generated-code quality (current functional-review scores) did **not** — zero-shot 8.0, standard 7.5, advanced 7.0 — because the single advanced-stage generation run dropped a required feature (ground/ceiling collision). This is the intended, honestly-reported finding and should not be quietly revised away once real grading scores come in, unless the new scores genuinely tell a different story.
- **Known caveat on file:** the intended grader (`gpt-oss:20b`) was also generator and a critic in Run 1 — flagged as a self-preference risk, not yet corrected. Correcting it is the top open task in this repository.
