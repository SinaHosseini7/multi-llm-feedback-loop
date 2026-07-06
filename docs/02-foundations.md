# 2. Foundations of Prompting

*This is the full version of [README §2](../README.md#2-foundations-of-prompting). It defines the four basic prompting modes, then spends real time on the tradeoff that the rest of this repository keeps returning to: more specification is not free, and on small models, more examples can actively hurt.*

Every prompting technique in this repository — up to and including the Multi-LLM Feedback Loop — is a way of moving along one axis: **how much of the task you specify versus how much you leave to the model's pretrained defaults.** The four modes below are the rungs of that ladder. Getting them straight matters because the case study in [Section 6](../case-study/README.md) is literally a controlled walk up this ladder, and its results only make sense if you know what each rung does and doesn't buy you.

To keep the four modes comparable, we'll reuse one analogy throughout: you're handing a broken laptop to a **repair specialist**. The specialist is competent — the question is only how much you tell them.

## 2.1 Zero-Shot, Standard, One-Shot, and Few-Shot Prompting

### Zero-shot

**Definition:** instructing the model to perform a task with no examples of the desired output, relying entirely on its pretrained knowledge of what the task usually looks like.

**Analogy:** you hand the specialist the laptop and say *"fix it."* No symptoms, no constraints, no example of what "fixed" means to you. Whatever they do next is drawn entirely from what laptops usually need.

**Syntax shape:**

```text
Summarize the following support ticket in one sentence.

<ticket text>
```

**Reach for it when** the task is common enough that the model's default interpretation is probably your interpretation — summarization, translation, boilerplate code, well-trodden formats. It's the cheapest possible prompt, and on tasks that saturate a model's training distribution it can be startlingly good. The case study's [zero-shot stage](../case-study/01-zero-shot/prompt.md) is one line long and still produced a start screen, a high score, and frame-rate-independent physics that nobody asked for — a useful reminder that the baseline you're trying to beat is not a straw man.

### Standard prompting

**Definition:** adding explicit task instructions, constraints, or context — requirements in prose — without providing any worked examples of the output.

**Analogy:** you add a written description: *"the laptop won't turn on, the battery reads 40%, and there's no charging light."* The specialist now knows *your* situation, but has still never seen how you want the repair documented.

**Syntax shape:**

```text
Summarize the following support ticket in one sentence.
Audience: engineering triage. Include the product area and a severity guess.
Do not speculate about root cause.

<ticket text>
```

**Reach for it when** the model's defaults are close but not right — you need *your* constraints (format, audience, exclusions, scope) rather than the statistical average of everyone's. This is the workhorse mode of day-to-day prompting, and it's the case study's [Stage 2](../case-study/02-standard/prompt.md): a careful spec of mechanics, controls, scoring, and restart behavior, with no examples.

### One-shot

**Definition:** supplying exactly one example of the input→output pattern you want replicated, alongside the instruction.

**Analogy:** you show the specialist one completed repair ticket from a previous job — *"here's how I documented the last similar repair"* — and ask them to follow the template.

**Syntax shape:**

```text
Summarize support tickets in the format shown.

Ticket: "App crashes when exporting a PDF on Android 14, started after v3.2."
Summary: [Mobile/Export] SEV-2 — PDF export crash on Android 14 since v3.2.

Ticket: <new ticket>
Summary:
```

**Reach for it when** the hard part of your task is the *shape* of the output rather than the reasoning — a precise format, a naming convention, a tone — because one concrete example disambiguates format far more cheaply than three paragraphs of description.

### Few-shot

**Definition:** supplying multiple examples (typically two to eight) so the model can infer a pattern, format, or reasoning style and apply it to a novel input — the mechanism the literature calls in-context learning (Brown et al., 2020).

**Analogy:** you hand over three or four completed repair tickets covering *different fault types* — a dead battery, a cracked screen, a liquid spill — so the specialist can infer the general documentation pattern and apply it to a fault they haven't seen documented.

**Syntax shape:** the one-shot layout, repeated — three or four `input → output` pairs, deliberately varied in surface content but identical in structure, followed by the new input.

**Reach for it when** the pattern is genuinely hard to verbalize: classification with fuzzy boundaries, a house style, edge-case handling that's easier to show than to state. Pick examples that differ as much as possible in *content* while agreeing exactly on *pattern* — if all your examples share an accidental quirk, the model may learn the quirk.

**One rule of thumb ties the four together:** put *behavior* in instructions and *format* in examples. Examples are a poor substitute for stating a requirement — a model shown three correct outputs may still not infer the constraint that made them correct — and instructions are a poor substitute for showing a format. The failure mode of skipping this rule is Section 7's first pitfall.

## 2.2 The Efficiency Tradeoff

Here is the nuance this repository is built around, so it gets real space rather than a footnote: **increasing the number of shots does not scale performance linearly, and on smaller or lower-parameter models, additional examples can *degrade* output quality rather than improve it.**

That claim surprises people whose intuition was formed on frontier models, so it's worth being precise about the mechanisms. Three of them are well-supported and easy for an intermediate practitioner to sanity-check on their own hardware:

1. **Context dilution and weak long-range attention.** Smaller models have both shorter effective context and weaker attention over long ranges. As examples stack up, the tokens of your actual instruction become a smaller and smaller fraction of the prompt, and later examples can dilute or even override earlier instructions. Research on long-context behavior has found that models attend best to the beginning and end of a prompt and worst to the middle (the "lost in the middle" effect; Liu et al., 2023) — and the middle is exactly where a long example block puts your constraints.

2. **Overfitting to surface patterns.** Smaller models are more prone to copying the *surface* of examples — formatting quirks, phrasings, even topical content — rather than the underlying task logic. Work on what demonstrations actually teach a model (Min et al., 2022) suggests much of few-shot's benefit comes from conveying format and label space rather than deep task understanding, which is precisely why a small model given four examples about laptops may start hallucinating laptop details into your unrelated fifth input.

3. **The core instruction gets lost.** Every added token increases the chance that the one sentence that actually defines success stops being the thing the model optimizes for. This is the same failure as over-prompting ([Section 7](07-pitfalls.md), pitfall #1) — shot bloat is just over-prompting with examples instead of constraints.

**The practical rule of thumb:** for smaller and local models, test **1-shot and 3-shot before assuming more is better**, and treat "more examples" as a *hypothesis to benchmark*, not a default best practice. Concretely: fix a small set of representative inputs, run each shot-count variant against them, and score per-requirement adherence rather than overall vibes. If 3-shot doesn't beat 1-shot on your task and your model, more shots almost certainly won't either.

There is a second, related property of small models that the tradeoff implies and the case study demonstrates: **single-run variance.** A small model doesn't just respond differently to different prompt sizes — it responds differently to the *same* prompt across runs, sometimes dropping a requirement it honored the run before. In [Section 6](../case-study/README.md) this shows up twice: the standard-stage output *regressed* to frame-locked physics that the zero-shot output had gotten right, and the advanced-stage output dropped an explicitly-required collision check while implementing every other new requirement cleanly. Prompt quality raises the ceiling; a small model in a single run doesn't always reach it. That's why the framework in [Section 5](05-master-tutorial.md) doesn't end at "write a better prompt" — it ends at *validate the output* (§5.4).

### A 2026 caveat: native reasoning models change where scaffolds pay off

Since these techniques were first cataloged, native **reasoning models** — OpenAI's o-series and GPT-5.x, Anthropic's reasoning-enabled Claude models, Google's Gemini, DeepSeek-R1, and open-weight reasoners like GPT-OSS — now perform chain-of-thought internally by default, before you ask.

The practical consequence is blunt: **explicit CoT/ToT scaffolding yields the largest marginal benefit on smaller and local models that don't reason natively, and the smallest on frontier reasoners that already do.** Telling a frontier reasoner to "think step by step" is mostly redundant; telling a small non-reasoning local model to do so can be the difference between a right and wrong answer on multi-step tasks.

This is not a digression from the efficiency tradeoff — it's the same thesis from another angle. Both say: *prompting techniques are model-relative; their payoff concentrates at the small end of the model spectrum.* It's also why the case study's fixed generator and intended grader, GPT-OSS-20B — itself a small open-weight reasoning model — is a fair, representative test bed for the kind of model this guide's techniques help most, rather than an arbitrary pick.

**So what do you do differently now?** Before choosing a technique from [Section 3](03-toolkit.md), identify which class of model you're prompting. If it's a frontier reasoner, invest in constraints, context, and validation rather than reasoning scaffolds. If it's a small or local model — this repository's emphasis — invest in explicit structure, keep shot counts low until benchmarks say otherwise, and never trust a single run.

---

*Next: [Section 3 — The Prompt Engineering Toolkit](03-toolkit.md), which organizes the named techniques by the question each one answers. Sources for the papers mentioned here are grouped under [References](../README.md#9-references) in the main README.*
