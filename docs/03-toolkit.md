# 3. The Prompt Engineering Toolkit

*This is the full version of [README §3](../README.md#3-the-prompt-engineering-toolkit): every named technique, with a plain-language definition, a minimal illustrative example, and the tradeoff it introduces.*

This toolkit is organized into **three functional categories, not a flat alphabetical list**, because each category answers a different question. [3.1](#31-reasoning--structure-frameworks) answers *how does the model reason* — techniques that shape the path from question to answer. [3.2](#32-meta-prompting) answers *how does the model improve its own instructions* — techniques where the prompt itself is the thing being engineered. [3.3](#33-practical-enhancers) answers *how do you shape the model's behavior through format and framing* — lightweight levers that change how a prompt lands without changing what it asks. Read the toolkit through those three questions and it stops being a grab-bag; each technique has a job, and the jobs compose.

One framing note carried over from [§2.2](02-foundations.md#22-the-efficiency-tradeoff): several techniques in 3.1 externalize reasoning that native reasoning models now do internally by default. Their marginal payoff is therefore largest on the small and local models this repository emphasizes — keep that in mind as you read the tradeoffs.

## 3.1 Reasoning & Structure Frameworks

### Chain-of-Thought (CoT)

**What it is:** prompting the model to externalize intermediate reasoning steps before producing a final answer, which measurably improves performance on multi-step logical, arithmetic, and planning tasks (Wei et al., 2022). It comes in two flavors: *few-shot CoT*, where your examples include worked reasoning, and *zero-shot CoT*, where a single instruction elicits it (the famous "Let's think step by step"; Kojima et al., 2022).

**Minimal example:**

```text
Work through the problem step by step first, then give the final answer on its own last line.
```

**Tradeoff:** longer outputs, higher token cost and latency — and on native reasoning models this is now often automatic, so the instruction can be redundant (see the [§2.2 currency note](02-foundations.md#a-2026-caveat-native-reasoning-models-change-where-scaffolds-pay-off)). One honest caution: a fluent chain of reasoning is not proof of a correct answer; models can rationalize a wrong conclusion convincingly, so verify the answer, not the eloquence.

### Tree-of-Thoughts (ToT)

**What it is:** an extension of CoT where the model explores multiple reasoning branches in parallel, evaluates them, and prunes weaker paths before converging (Yao et al., 2023a) — useful for problems with multiple viable solution paths, like puzzles, planning, and design-space exploration. Full ToT is usually an orchestrated search loop in code; the prompt-only approximation below captures the spirit.

**Minimal example:**

```text
Propose three genuinely different approaches, score each against the constraints, discard the weakest two, and carry the strongest to a complete answer.
```

**Tradeoff:** significantly higher compute and latency — you're paying for branches you'll throw away — so reserve it for complex planning or search-like tasks where single-path CoT demonstrably dead-ends.

### ReAct (Reason + Act)

**What it is:** a pattern where the model interleaves reasoning steps with *actions* — tool calls, searches, code execution — and the resulting *observations*, looping until it reaches a final answer (Yao et al., 2023b). Grounding reasoning in real observations is why it reduces hallucination, and it is the foundation of most modern agentic systems.

**Minimal example** (the format, more than a single sentence):

```text
Thought: I need the current exchange rate before I can convert.
Action: search("USD to JPY exchange rate")
Observation: <result>
Thought: Now I can compute the converted amount...
```

**Tradeoff:** this is less a single prompt than a prompting *pattern* for multi-turn, tool-using systems — it needs tool infrastructure, stop conditions, and error handling, so it belongs in agent design more than in one-off prompting.

### The self-correction family: Self-Consistency, Reflexion, Self-Refine

These three are variations on one core idea — **the model checking or improving its own output** — but the mechanisms differ, and the differences matter.

**Self-Consistency** attacks variance: sample multiple *independent* reasoning paths for the same problem (temperature above zero), then take the majority or most consistent final answer (Wang et al., 2022). Example instruction to yourself, not the model: *run the same CoT prompt five times and vote.* It needs a discrete, comparable answer to vote on, and it multiplies cost by the sample count.

**Reflexion** attacks repeated failure: the model critiques its own prior attempt in natural language — often informed by an external signal like a failing test — and uses that verbal feedback as memory for an improved attempt, across multiple episodes (Shinn et al., 2023). Example: *"Here is your previous attempt and the test that failed. Explain what went wrong, then produce a corrected attempt."* It shines on tasks with a checkable outcome; without one, the model grades its own homework.

**Self-Refine** is the tightest and most widely cited version of the loop today: **generate → self-critique → revise**, repeated until quality plateaus, all within one model and often one conversation (Madaan et al., 2023). Example: *"Draft the email. Then list three specific weaknesses in your draft. Then rewrite it addressing all three."* Cost is modest (a few extra turns); the ceiling is the model's own judgment.

**Why Self-Refine earns its spot in this list:** it is the direct single-model ancestor of this repository's core technique. In one sentence, the Multi-LLM Feedback Loop of [Section 4](04-feedback-loop.md) is *Self-Refine, but with the critique step delegated to several independent models instead of the same one.* Which exposes the family's shared limitation and the reason Section 4 exists: a model critiquing its own output brings the same blind spots to the review that it brought to the draft. The critique is correlated with the mistake.

## 3.2 Meta-Prompting

The techniques above improve an *answer*. This subsection's techniques improve the *prompt* — they treat the prompt itself as the object being engineered.

### Automatic Prompt Engineering (APE)

**What it is:** using an LLM to generate, evaluate, and select candidate prompts for a task automatically — typically by generating many instruction variants and scoring them against a metric or a held-out set of examples, keeping the winner (Zhou et al., 2022).

**Minimal example:**

```text
Here are 10 input→output pairs. Propose 8 candidate instructions that would make a model produce these outputs from these inputs.
```

…followed by scoring each candidate on held-out pairs.

**Tradeoff:** APE needs what many real tasks lack — an automatic metric and a labeled evaluation set — and it optimizes for the metric, not for requirements you forgot to encode in it. **Currency note:** APE's ideas have since matured into named, tooling-backed *automated prompt optimization* frameworks — most prominently **DSPy** — that treat prompts as compiled, optimizable modules rather than hand-written strings. Those frameworks are deliberately out of scope here (see [Further Reading](../README.md#9-references)), but you should know APE isn't just a 2022 research curiosity; it's now infrastructure.

### Conversational Prompt Engineering (CPE)

**What it is:** an interactive process where a human and an LLM iteratively refine a prompt together through dialogue — the human states a goal, the LLM proposes a prompt (often after interviewing the human about preferences and edge cases), the human gives feedback, and the LLM revises (Ein-Dor et al., 2024).

**Minimal example:**

```text
Interview me with up to five questions about my task, audience, and constraints. Then draft the prompt you'd use, and revise it after my feedback.
```

**Tradeoff:** it's bounded by one human's attention and one model's perspective — excellent for *articulating* requirements you couldn't state cold (which makes it a natural companion to [§5.1 Goal Definition](05-master-tutorial.md#51-goal-definition)), weaker at *catching* the requirements neither of you thought of.

### The bridge to Section 4

Notice what APE, CPE, and Self-Refine jointly establish: **prompts are not written once — they are objects to be engineered, tested, and revised.** APE revises against a metric; CPE revises against one human's feedback; Self-Refine revises against one model's self-critique. Each has a single point of judgment, and that single point is each one's ceiling. The [Multi-LLM Feedback Loop](04-feedback-loop.md) extends the same idea across *multiple independent models acting as critics* — not one model, not one human–model pair, not one automated metric — so the judgment itself is diversified. That is the whole trick, and Section 4 explains why it works.

## 3.3 Practical Enhancers

Two lightweight levers that change how a prompt lands rather than what it asks. Cheap to apply, worth knowing precisely.

### XML tags

**What it is:** using structural tags — `<context>`, `<instructions>`, `<example>`, `<success_criteria>` — to delimit the distinct parts of a prompt. Making the structure unambiguous measurably improves instruction-following in many models (several vendors, notably Anthropic, explicitly recommend it in their prompting documentation): the model can no longer confuse your reference material with your instructions, or your example with your input.

**Short example:**

```text
<instructions>
Summarize the report below for an executive audience in under 120 words.
</instructions>

<report>
{{report_text}}
</report>
```

**Tradeoff:** essentially none beyond a few tokens, which is why both of the case study's advanced-stage prompts use tags throughout — see the [Architect's draft](../case-study/03-advanced-feedback-loop/01-architect-draft.md) and the [final synthesized prompt](../case-study/03-advanced-feedback-loop/03-final-prompt.md). One habit worth keeping: use tag *names* that mean something (`<mechanics>`, not `<section2>`), because the names themselves carry instruction.

### Emotional prompting

**What it is:** adding stakes, urgency, or emotional framing to a prompt — *"this is critical for my job"*, *"take a deep breath and work carefully"* — which some research (e.g., the EmotionPrompt line of work; Li et al., 2023) and practitioner testing has shown can nudge output quality or apparent effort in certain models.

**Short example:**

```text
This analysis will be presented to the board unedited — accuracy matters more than speed.
```

**Tradeoff, stated evenhandedly:** results are **model-dependent and inconsistent** — some models show measurable gains, others none, and effects can shift between model versions. Treat it as *a lever worth A/B testing on your model*, never a guaranteed win, and never a substitute for an actual requirement: "this is very important" is not a spec.

> **Scope note:** `r.jina.ai` is deliberately *not* listed here. It's a resource-gathering **tool**, not a prompting technique, so it lives in [§5.2 of the Master Tutorial](05-master-tutorial.md#52-resource-gathering).

## Choosing from the toolkit

A closing decision aid — symptom on the left, first technique to reach for on the right:

| You're seeing… | Reach for… |
|---|---|
| Wrong answers on multi-step logic/math (small model) | CoT; add Self-Consistency if answers are checkable |
| Several plausible solution paths, model commits too early | Tree-of-Thoughts |
| Task needs live information or tools | ReAct (as a system pattern) |
| Output quality plateaus after one attempt | Self-Refine; Reflexion if you have a failure signal |
| Output format keeps drifting | One-shot example + XML tags |
| You can score outputs automatically | APE / automated prompt optimization |
| You can't articulate your own requirements yet | CPE, then §5.1 Goal Definition |
| The prompt is high-stakes or will be reused many times | The [Multi-LLM Feedback Loop](04-feedback-loop.md), run inside the [Section 5 framework](05-master-tutorial.md) |

---

*Next: [Section 4 — Introducing the Multi-LLM Feedback Loop](04-feedback-loop.md). Paper sources for every technique above are grouped under [References](../README.md#9-references) in the main README.*
