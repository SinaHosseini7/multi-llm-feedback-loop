# 7. Best Practices & Common Pitfalls

*This is the full version of [README §7](../README.md#7-best-practices--common-pitfalls). Each pitfall gets a one-line description, a one-line fix, and just enough example to make it recognizable in your own work. Where a real example exists in the Run 1 record, it's cited — several of these were live in the case study.*

### 1. Over-prompting until the core instruction is lost

**What it looks like:** the prompt grows constraint by constraint until the one sentence defining success is buried in the middle of forty others — and the model starts honoring the trivia while missing the point.
**Fix:** rank your requirements, cut what doesn't change the output, and restate the core ask at the end of the prompt as well as the start.
Models attend best to the beginning and end of a long context and worst to the middle ([§2.2](02-foundations.md#22-the-efficiency-tradeoff)) — the middle is where an unpruned prompt puts your priorities. If everything is emphasized, nothing is.

### 2. Shot-count bloat

**What it looks like:** adding a fifth, sixth, seventh example on the theory that more demonstrations must mean better output — while a small model's adherence quietly gets worse.
**Fix:** test 1-shot and 3-shot before assuming more, and treat "more examples" as a hypothesis to benchmark, not a default ([§2.2](02-foundations.md#22-the-efficiency-tradeoff)).
This is pitfall #1 wearing examples instead of constraints: shots dilute the instruction, and small models overfit to their surface patterns.

### 3. Contradictory instructions across a long prompt

**What it looks like:** line 8 and line 31 give the model two different answers to the same question, and it silently picks one — a different one per run.
**Fix:** give every parameter exactly one home in the prompt, then do a final read checking *only* for cross-section conflicts before shipping the draft.
Run 1 contains a live (mild) specimen: `qwen3.6:27b` flagged that the draft asked for window constants *"at the top of the file"* while separately asking for all tunables to be *"grouped together"* — not strictly contradictory, but two rules competing to place the same values ([transcript](../case-study/03-advanced-feedback-loop/02-critic-feedback/critic-qwen.md)). A diverse critic panel is good at catching these, because each critic resolves the ambiguity differently and *someone* trips on it.

### 4. Treating critic feedback as universally correct

**What it looks like:** the synthesis step becomes "apply all suggestions," and the prompt inherits every critic's pet concern, scope creep, and occasional bad call.
**Fix:** reconcile, don't concatenate — weigh consensus and severity, judge unique catches on merit, and arbitrate conflicts against the goal card ([§4.3](04-feedback-loop.md#43-synthesis-is-reconciliation-not-concatenation)).
Run 1 required exactly this: `phi4-reasoning:14b` wanted the draft's self-verification step de-emphasized as a distraction, while `qwen3.6:27b` wanted it *broadened*. The Architect sided with qwen and strengthened the step — one critic was simply overruled, and the final prompt is better for it. Critics are diagnostic instruments, not oracles.

### 5. Letting a critic rewrite instead of diagnose

**What it looks like:** a "critique" that comes back as a full corrected prompt — now you have N competing drafts, no comparable findings, and a review-the-reviewers problem.
**Fix:** enforce the template's rules — *list issues only; do not rewrite; do not provide a corrected version* — and re-request any critique that breaks them ([§5.3](05-master-tutorial.md#53-the-execution)).
Diagnoses compose; rewrites compete. The no-rewrite rule is also what keeps the final prompt in a single voice — the Architect's — instead of a patchwork of four styles.

### 6. Skipping Goal Definition and iterating blind

**What it looks like:** drafting first and discovering the requirements by watching the prompt fail — every vague expectation becomes a wasted critique round or a failed generation.
**Fix:** write the goal card before the prompt: output format, audience, measurable success criteria, hard constraints, explicit out-of-scope list ([§5.1](05-master-tutorial.md#51-goal-definition)).
The out-of-scope list earns its keep fast: Run 1 kept it implicit, and when a critic proposed difficulty progression the Architect had to infer it was out of scope rather than point to a line saying so.

### 7. Conflating the model roles

**What it looks like:** reading the case study as "Claude scored 7/10 at Flappy Bird," or letting one model quietly wear several hats in your own pipeline.
**Fix:** keep the mnemonic straight — **the Architect and Critics build the prompt; the generator runs it; the evaluator grades it** — and staff each role deliberately ([§6](../case-study/README.md)).
The roles answer different questions (was the *prompt* improved? did the *output* meet spec? judged by *whom*?), and merging them corrupts the answers. Run 1 logs its own violation honestly: `gpt-oss:20b` served as critic, generator, *and* intended grader, a self-preference risk disclosed in the [benchmark caveats](../case-study/benchmark-results.md).

### 8. Forgetting to version-control final prompts

**What it looks like:** the "final" prompt lives in a chat scrollback; three weeks later nobody knows which version produced the good run, or why a clause exists.
**Fix:** save every final prompt as a file with a version, a provenance header, and a critique→edit changelog ([§5.5](05-master-tutorial.md#55-finalization)).
Prompts are engineering artifacts with the same lifecycle as code — the case study's [final prompt](../case-study/03-advanced-feedback-loop/03-final-prompt.md) shows the pattern: one file from which a stranger can reconstruct the whole pipeline.

### 9. *(Bonus, earned by Run 1)* Skipping output validation

**What it looks like:** treating a well-engineered prompt as a guarantee — shipping the first generation unchecked because the *instructions* were airtight.
**Fix:** always run [§5.4](05-master-tutorial.md#54-validation): a non-generator model checks the output against the success criteria, PASS/FAIL per item with evidence, and code additionally gets executed.
This is the case study's central lesson. The final prompt explicitly required ground/ceiling collisions to end the game; a single run of the small generator implemented everything else and dropped exactly that. One validation pass catches it; skipping the pass is how the best prompt in the experiment shipped the run's only game-breaking bug ([Stage 3 evaluation](../case-study/03-advanced-feedback-loop/evaluation.md)).

---

*The pitfalls are the framework in negative: 1–3 are [§2](02-foundations.md) ignored, 4–5 are [§4](04-feedback-loop.md) ignored, 6–9 are [§5](05-master-tutorial.md) ignored. If one is biting you, the fix links to the section that prevents it.*
