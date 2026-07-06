# Benchmark Results

**Task (held constant):** a runnable Flappy Bird clone in Python + `pygame-ce`.
**Code-generation model (held constant, role 2):** `gpt-oss:20b` — the *only* variable across stages is the prompt.
**Evaluator (role 3):** intended per methodology to be `gpt-oss:20b` with a fixed rubric. The scores in this file are an **independent functional review** (each program run headlessly under `pygame-ce` 2.5.7 + code inspection, this session). Where you have `gpt-oss:20b`'s own rubric numbers, they slot into the same columns — see "Data still needed."

---

## Read this first: what the technique actually claims

The Multi-LLM Feedback Loop is a method for producing a **better prompt.** Its deliverable is a prompt, not a program. So the primary result is the *prompt-quality progression*; the *generated-code quality* is a downstream, single-run proxy limited by a small local generator. Both are reported below, honestly, and they do **not** tell an identical story.

## 1. Prompt-quality progression (the technique's actual output)

| Stage | Prompt | Explicit requirements | Specifies units? | Names edge cases / failure modes? |
|---|---|---|---|---|
| Zero-shot | one line | ~1 | no | no |
| Standard | short spec | ~7 | no | partially |
| Advanced (draft v1) | Architect draft | ~9 | some | some |
| Advanced (final) | 4-critic synthesis | **~15** | **yes** (px/s, px/s²) | **yes** (tunneling, held-key repeat, restart flap, unbounded pipes, off-edge gaps) |

This progression is large, objective, and monotonic. On the axis the technique is meant to move, it worked: four independent open-weight critics surfaced concrete gaps in the draft, and the synthesis folded them into a markedly more rigorous prompt. **This is the headline result.**

## 2. Generated-code quality (downstream proxy — single run, small local model)

Verified feature matrix (✅ present & working / ⚠️ present but weak / ❌ missing), from functional testing:

| Requirement | Zero-shot | Standard | Advanced |
|---|:--:|:--:|:--:|
| Launches without error | ✅ | ✅ | ✅ |
| Frame-rate-independent (`dt`) physics | ✅ | ⚠️ per-frame | ✅ |
| Edge-triggered flap (no held-key repeat) | ✅ | ✅ | ✅ |
| Pipe spawn / scroll / pass-through | ✅ | ✅ | ✅ |
| Off-screen pipe cleanup | ✅ | ✅ | ✅ |
| Gap constrained to playfield | ✅ | ✅ | ✅ (cleanest) |
| **Ground/ceiling collision ends game** | ✅ | ✅ | ❌ **missing** |
| Score increments + displays | ✅ | ✅ | ✅ |
| Game-over screen + restart | ✅ | ✅ | ✅ |
| Full state reset on restart | ✅ | ✅ | ✅ |
| Restart debounce (no accidental flap) | ✅ | ✅ | ✅ explicit |
| Max-fall-speed clamp (anti-tunnel) | ❌ | ❌ | ✅ only stage |
| Start screen | ✅ | ❌ | ❌ |
| High score tracked | ✅ | ❌ | ❌ |

Independent functional-review scores (1–10, Claude — see each stage's `evaluation.md`):

| Stage | Correctness | Completeness | Code quality | Constraint adherence | **Overall** |
|---|:--:|:--:|:--:|:--:|:--:|
| Zero-shot | 8 | 9 | 7 | 9* | **8.0** |
| Standard | 7 | 7 | 8 | 8 | **7.5** |
| Advanced | 5 | 7 | 9 | 7 | **7.0** |

\* Adherence for zero-shot is high only because its prompt imposes almost nothing to violate; compare each stage against its own prompt.

## Interpretation

The code-quality scores are **not** monotonic, and that's the interesting part. The advanced stage produced the **best-architected** program (only one with dt-physics *and* an anti-tunneling clamp, cleanest constants and comments, explicit restart debounce) yet scored lowest overall because a single run of `gpt-oss:20b` **dropped one explicitly-required feature — ground/ceiling collision — that the two simpler prompts got right.** Meanwhile the zero-shot output was unexpectedly strong (start screen, high score, dt-physics), and the standard output *regressed* to per-frame physics.

The clean way to state the finding: **the Feedback Loop reliably improved the prompt; the small single-run generator did not reliably honor the improved prompt.** That is precisely the small-/local-model behavior discussed in Content Guide §2.2, and precisely what the §5.4 validation step exists to catch — a secondary model checking the advanced output against its own success criteria would have flagged the missing collision in one pass. The result argues *for* the full 5-part framework (draft → critique → synthesize → **validate** → finalize), not against the technique.

## Methodology & honest caveats

- **Single generation run per stage.** No averaging. The advanced ground-collision miss is a textbook example of single-run variance; averaging over 3–5 runs (or adding the §5.4 validation pass) would reduce it. Disclosed, not hidden.
- **Generator = evaluator = one of the critics.** `gpt-oss:20b` served as the code generator, the intended rubric grader, *and* one of the four critics. A model grading its own output risks **self-preference bias**; a distinct grader is recommended for a v2. (The scores in this file avoid that particular issue by being an independent review, but the intended methodology should still switch graders.)
- **Architect role spanned two models.** Draft v1 was written by Claude Opus 4.8; the synthesis was done by Claude Sonnet 5. Minor, but recorded for reproducibility.
- **Verbatim artifacts.** All three `flappy_bird.py` files are committed exactly as generated. Bugs are documented, not fixed.

## Data still needed to finalize

1. `gpt-oss:20b`'s own **rubric scores**, if you ran the grading step, to populate the "pending" rows in each `evaluation.md` alongside the functional-review numbers.
2. The exact **Stage-2 (standard) prompt text**, verbatim → `02-standard/prompt.md` (currently a clearly marked stub).

*(The four raw **critic transcripts** — `gpt-oss:20b`, `qwen3.6:27b`, `gemma4:26b`, `phi4-reasoning:14b` — are now committed verbatim in `03-advanced-feedback-loop/02-critic-feedback/`.)*
