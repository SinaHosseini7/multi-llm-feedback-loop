# 5. The Master Tutorial: A 5-Part Framework

*This is the full version of [README §5](../README.md#5-the-master-tutorial-5-part-framework). Sections [2](02-foundations.md)–[4](04-feedback-loop.md) were the **what**; this section is the **how**, in order. Follow it top to bottom and you'll have run the Multi-LLM Feedback Loop end to end, with artifacts to show for it. The [case study](../case-study/README.md) is this framework executed for real — each part below points at the actual files it produced.*

The framework has five parts, and the ordering is the point:

**Goal Definition → Resource Gathering → Execution → Validation → Finalization**

The Feedback Loop of Section 4 is part 3. The parts around it are what make it pay off: the loop can only sharpen a prompt against a goal that exists (§5.1), and a sharpened prompt still doesn't guarantee a correct output (§5.4).

## 5.1 Goal Definition

Before writing a single line of prompt, write the **goal card** — four short answers:

1. **Exact output format.** What artifact comes back? A single code file, a JSON object with named fields, a 120-word paragraph? If you can't name the format, you can't validate against it later.
2. **Audience / consumer.** Who or what consumes the output — a human reader at what expertise level, or a downstream program with what expectations?
3. **Measurable success criteria.** A checklist of *verifiable* statements. "The code is robust" is not verifiable; "collisions end the game" is. Every adjective in your head must be converted into a check, because §5.4 will test exactly these and nothing else.
4. **Hard constraints and out-of-scope.** What must never happen, which tools/formats are mandatory, and — just as important — what you are deliberately *not* asking for. An explicit out-of-scope list is what lets you decline a critic's pet feature later without relitigating the goal.

**The mistake this step prevents** is the most common intermediate-level failure in this repo's [pitfall list](07-pitfalls.md): starting to draft the prompt first and discovering the requirements *by watching it fail*. That discovery process is expensive precisely where this guide's techniques are expensive — every vague requirement becomes a critique round or a failed run instead of one line on a card.

**The goal card behind the case study** (each row traces directly to the committed [Draft v1](../case-study/03-advanced-feedback-loop/01-architect-draft.md)):

| Field | Value |
|---|---|
| Output format | One complete, runnable Python file (`flappy_bird.py`), returned as a single code block plus a short paragraph of stated assumptions |
| Audience / consumer | A person who runs `python flappy_bird.py` as-is after `pip install pygame-ce` |
| Success criteria | Launches without errors; bird responds to input; pipes spawn, scroll, and can be passed; collisions end the game; score increments and displays; restart works after game over |
| Hard constraints | Single file; pygame drawing primitives and default font only — no image/font/sound asset files; tunables as named constants; clean quit handling |
| Out of scope *(implicit in Run 1)* | Sound, menus beyond a restart prompt, difficulty progression |

One honest note on that last row: Run 1's out-of-scope list was implicit rather than written down, and it cost a little — a critic later proposed difficulty progression, and the Architect had to infer it was out of scope rather than point at a line saying so ([§4.3](04-feedback-loop.md#43-synthesis-is-reconciliation-not-concatenation)). Write the list down.

## 5.2 Resource Gathering

The Architect drafts from what you give it, so **your draft's quality is bounded by your resources' quality.** Gather, before drafting:

- **Reference documentation** for any API, library, or domain the prompt touches — the authoritative version, not your memory of it.
- **Examples of good and bad output**, if they exist. Even one of each sharpens both the draft and, later, the validation checklist.
- **Domain constraints** — style guides, compliance rules, naming conventions — anything the model can't guess.
- **Prior prompt attempts** and how they failed, if this isn't your first pass.

**The tool worth knowing here: Jina Reader.** Prepending `https://r.jina.ai/` to any URL returns that page as clean, LLM-ready text — markup, navigation, and ads stripped:

```text
https://r.jina.ai/https://example.com/docs
```

Paste the result into the Architect's context as grounding material. At the time of writing, unauthenticated use is rate-limited to roughly 20 requests per minute, and a free API key raises that limit — fine for gathering a handful of reference pages per prompt, which is the typical need. (This is why `r.jina.ai` lives here and not in the [Section 3 toolkit](03-toolkit.md): it's a resource-gathering tool, not a prompting technique.)

Two habits close this step. First, **version the resources next to the prompt** — a prompt grounded on v2 docs will quietly rot when v3 ships, and you'll want to know what it was built against. Second, calibrate effort to the task: the case study needed almost no gathering because a Flappy Bird clone is deeply in-distribution for any code model; the step matters most for exactly the opposite case — internal APIs, house styles, and domain rules the model has never seen.

## 5.3 The Execution

This is the Feedback Loop of [Section 4](04-feedback-loop.md), run as an operational sequence:

**Step 1 — The Architect drafts.** Give the Architect the goal card and resources, and have it produce Prompt v1. A structure that has held up well (and is the structure of the case study's draft): a `<role>`, the `<task>`, one tagged section per requirement area, explicit `<success_criteria>`, and a `<final_step>` self-check — XML-tagged throughout ([§3.3](03-toolkit.md#33-practical-enhancers)). Save the draft as a file (`01-architect-draft.md` in the case study's naming). It is now **frozen**: every critic must review the identical artifact, or their critiques stop being comparable.

**Step 2 — Send the draft, unmodified, to each critic.** Wrap it in a standardized critique request. Here is the actual template used in Run 1, reproduced verbatim so this section is self-contained (canonical copy: [`00-critique-request-template.md`](../case-study/03-advanced-feedback-loop/00-critique-request-template.md)):

```text
You are acting as an expert prompt reviewer. I will give you a PROMPT that was
written to instruct a separate code-generation model to build a Flappy Bird clone
in Python with pygame. Your job is to review the PROMPT itself — not to complete
the task, not to write any code, and not to rewrite the prompt.

Review the PROMPT for:
1. Ambiguity — anything a code model could reasonably interpret more than one way.
2. Missing requirements or edge cases — behavior that isn't specified but should be
   (e.g., frame-rate independence, restart handling, boundary conditions,
   difficulty over time, determinism, window/asset assumptions).
3. Failure modes — ways the resulting program could crash, hang, or behave wrongly.
4. Structural weaknesses — ordering, contradictions, or unclear success criteria that
   make the prompt harder for the model to follow reliably.

Rules for your response:
- DO NOT rewrite or rephrase the prompt. DO NOT provide a corrected version.
- DO NOT write any Python or pygame code.
- List issues only. For each issue, give: (a) a short label, (b) a severity of
  High / Medium / Low, (c) the specific part of the prompt it refers to (quote a few
  words), and (d) one sentence on why it matters for the generated code.
- If you find no issue in a category, say so rather than inventing one.
- End with a single line: the one change you'd prioritize if only one could be made.

Here is the PROMPT to review:

---
{{DRAFT_PROMPT}}
---
```

(To reuse it for your own task, adapt the first paragraph's task description and the category examples; the rules travel unchanged.)

Every rule in that template exists for a reason worth knowing:

- **"Review the PROMPT itself"** stops critics from helpfully solving the task instead of reviewing the instructions.
- **The four categories** force coverage — a critic who only free-associates will cluster on whatever it notices first.
- **"DO NOT rewrite… DO NOT provide a corrected version"** is the load-bearing rule. A rewrite collapses N independent critiques into N *competing drafts*, and now someone has to review the reviewers. Diagnoses compose — five lists of issues merge into one; five rewritten prompts don't. It also keeps the final prompt in a single voice: the Architect's.
- **Label + severity + quoted span + one-line rationale** makes every issue triageable and traceable back to the exact words that caused it.
- **"If you find no issue in a category, say so"** gives critics permission not to invent problems — in Run 1, two critics used it, and their silence was signal.
- **The single prioritized change** forces each critic to rank its own findings, which turned out to be one of the most informative lines in each Run 1 transcript (all four converged on delta-time physics).

**Step 3 — Collect.** One transcript per critic, saved verbatim as its own file (`02-critic-feedback/critic-<model>.md` in the case study). The mechanics that protect independence: a **fresh session per critic**, no shared context, no critic sees another's review, and the exact **model name and version recorded** in each file's header. Three to five critics from different training lineages is the sweet spot ([§4.4](04-feedback-loop.md#44-choosing-the-critic-roster)).

Then the Architect synthesizes — consensus adopted and made precise, unique catches judged on merit, conflicts arbitrated against the goal card, scope creep declined. That discipline is covered in depth, with the real Run 1 arbitrations, in [§4.3](04-feedback-loop.md#43-synthesis-is-reconciliation-not-concatenation).

## 5.4 Validation

Keep two different reviews straight, because conflating them is how bugs ship:

- **§5.3 critiques the *prompt*, before it runs.** Its question: *will these instructions be interpreted the way I intend?*
- **§5.4 validates the *output*, after it runs.** Its question: *did the thing that came back actually meet the success criteria?*

The Feedback Loop makes the prompt better; it does **not** make any single generation obey it. The case study proved this the honest way: the final prompt *explicitly required* that collisions with the ground and ceiling end the game, and the generator's single run implemented every other new requirement cleanly while **omitting exactly that check** — a no-flap bird sinks through the floor and the game never ends ([Stage 3 evaluation](../case-study/03-advanced-feedback-loop/evaluation.md)).

Walk what validation would have done with it. A validator handed the final prompt's own `<success_criteria>` reaches the item *"collisions (pipe, ground, ceiling) end the game reliably even at high fall speed"*, searches the code for a ground/ceiling collision test, finds pipe collisions only, and returns: **FAIL — no ground or ceiling collision check present; bird falls out of the playfield with no game-over.** One checklist pass, one caught bug — the cheapest call in the whole pipeline is the one Run 1 skipped.

**How to run validation well:**

1. **Use a validator that is not the generator.** A model checking its own output brings the same blind spots to the review that produced the miss — the same self-preference argument as [§4.1](04-feedback-loop.md#41-core-concept--why-it-works), now applied downstream. (Run 1's design had `gpt-oss:20b` as generator *and* intended grader; the [benchmark](../case-study/benchmark-results.md) logs that as a caveat rather than pretending otherwise.)
2. **Validate against the §5.1 criteria — verbatim.** The checklist you wrote at the start is the contract; don't let the validator improvise a different one.
3. **Demand PASS/FAIL per item, with evidence.** Quoted lines or "no implementation found." No partial credit — partial credit is where misses hide.
4. **For code, also run it.** A static read plus an actual execution (headless smoke test if there's a display, as the case-study evaluations did) catches different failure classes.
5. **Ask for a simple rubric score.** Not because the number is deep, but because a *repeatable* scoring rule makes runs and prompt versions comparable — this is exactly the role the functional-review scores play in the [benchmark table](../case-study/benchmark-results.md).

A generic validation-request template you can copy (this one is illustrative — written for this guide, not a Run 1 artifact):

```text
You are acting as an independent validator. Below are (1) the SUCCESS CRITERIA an
output was required to meet, and (2) the OUTPUT produced by a separate generation
model. Check the OUTPUT against the CRITERIA — do not fix it, do not praise it.

Rules:
- Evaluate every criterion, one per row: criterion | PASS or FAIL | evidence
  (quote the relevant line(s), or write "no implementation found").
- No partial credit: if a criterion is only partly met, mark FAIL and state what
  is missing.
- Separately flag anything present that was never asked for and could cause
  problems (invented features, unsafe defaults, contradictions with the criteria).
- End with the PASS/FAIL counts and one overall score out of 10, applying a rule
  you state explicitly before scoring.

SUCCESS CRITERIA:
{{CRITERIA}}

OUTPUT:
{{OUTPUT}}
```

**When validation fails, triage before iterating.** If the output missed a requirement the prompt stated clearly (Run 1's case), the prompt isn't the problem — regenerate, or fix the artifact directly, and remember [§2.2's](02-foundations.md#22-the-efficiency-tradeoff) lesson about single-run variance on small models. If the miss traces to a genuine ambiguity, patch the prompt and note it for §5.5. Either way, **bound the iteration** — one or two loops, each recorded — or "validate" quietly becomes "fiddle forever."

## 5.5 Finalization

The deliverable of this whole framework is not a chat transcript — it's a **versioned prompt artifact**. Finalize by:

1. **Reconciling validation feedback** into the prompt where (and only where) triage said the prompt was at fault.
2. **Saving the final prompt as its own file**, named and versioned (`03-final-prompt.md`, v1.0), with a **provenance header**: what produced it, from what draft, reviewed by which critic models, synthesized by whom, on what date. The case study's [final prompt](../case-study/03-advanced-feedback-loop/03-final-prompt.md) is the live pattern — its header lets a stranger reconstruct the entire pipeline from one file.
3. **Keeping a changelog that maps critique → edit.** One line per accepted change, naming the critic finding and the prompt line it produced. The case study's [draft→final diff table](../case-study/README.md) is the worked example: every new requirement in the final prompt is traceable to a transcript. This is what makes the prompt *maintainable* — six months later, "why is this clause here?" has an answer.
4. **Knowing when to re-run the loop.** A versioned prompt is stable, not sacred. Re-run when the generator model changes (prompt quality is model-relative — [§2.2](02-foundations.md#a-2026-caveat-native-reasoning-models-change-where-scaffolds-pay-off)), when the task drifts, or when production surfaces a new failure class the criteria never covered. Version the result; keep the old one.

## The whole framework on one card

```text
[ ]  1. Goal card written: output format, audience, measurable success criteria,
        hard constraints, explicit out-of-scope list.            (§5.1)
[ ]  2. Resources gathered and versioned; web docs pulled clean via
        https://r.jina.ai/<url>.                                 (§5.2)
[ ]  3. Architect drafts Prompt v1 from goal card + resources; draft frozen
        and saved as a file.                                     (§5.3)
[ ]  4. Draft sent UNMODIFIED to 3–5 critics from different training
        lineages — fresh sessions, standard critique template.   (§5.3)
[ ]  5. One verbatim transcript saved per critic, model + version recorded.
[ ]  6. Architect synthesizes: consensus adopted, unique catches judged,
        conflicts arbitrated against the goal card, scope creep
        declined and logged.                                     (§4.3)
[ ]  7. Final prompt run on the target generator.
[ ]  8. Output validated by a NON-generator model against the §5.1
        criteria: PASS/FAIL per item with evidence; code also executed.  (§5.4)
[ ]  9. Failures triaged — regenerate vs. patch prompt — with bounded
        iteration (1–2 loops, recorded).                         (§5.4)
[ ] 10. Final prompt saved as a versioned artifact with provenance header
        and critique→edit changelog.                             (§5.5)
```

---

*To see every artifact this procedure produces — goal-shaped draft, four verbatim critiques, synthesized final prompt, generated code, and the validation-shaped evaluations — walk the [case study](../case-study/README.md). For what goes wrong when steps get skipped: [Section 7 — Pitfalls](07-pitfalls.md).*
