# Content Writing Guide: The Multi-LLM Feedback Loop Repository

**Purpose of this document:** This is your internal planning and briefing file — not repository content itself. Each section below tells you exactly what to write, why it belongs where it does, and what it needs to accomplish before you move to the next one. Treat each entry as a brief you'd hand to a ghostwriter: read it, then draft the actual section content into its corresponding file (see `REPOSITORY_STRUCTURE_GUIDE.md` for where each piece lives).

**Audience reminder:** Intermediate users. Don't re-explain what an LLM is. Do explain *why* a technique works, not just *that* it exists. Every section should answer "so what do I do differently now?"

> **Revision note (this pass).** This revision reconciles the guide with the actual state of the repository as it stands today: all four critic transcripts are now finalized and committed (the qwen transcript was checked against the repo copy and confirmed byte-for-byte identical — no drift between what the critic produced and what's on GitHub). Two items remain genuinely open and are called out explicitly wherever they matter, rather than being marked "pending" quietly in a table: **(1)** deciding on and running a grading model distinct from the generator, and **(2)** adding gameplay screenshots. Everything else — folder layout, roster, diagram format, LICENSE/CONTRIBUTING/.gitignore presence — is now confirmed and locked. Full change log in **Appendix A**.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Foundations of Prompting](#2-foundations-of-prompting)
   - 2.1 [Zero-Shot, Standard, One-Shot, and Few-Shot Prompting](#21-zero-shot-standard-one-shot-and-few-shot-prompting)
   - 2.2 [The Efficiency Tradeoff](#22-the-efficiency-tradeoff)
3. [The Prompt Engineering Toolkit](#3-the-prompt-engineering-toolkit)
   - 3.1 [Reasoning & Structure Frameworks](#31-reasoning--structure-frameworks)
   - 3.2 [Meta-Prompting](#32-meta-prompting)
   - 3.3 [Practical Enhancers](#33-practical-enhancers)
4. [Introducing the Multi-LLM Feedback Loop](#4-introducing-the-multi-llm-feedback-loop)
   - 4.1 [Core Concept & Why It Works](#41-core-concept--why-it-works)
   - 4.2 [When to Use It (and When Not To)](#42-when-to-use-it-and-when-not-to)
5. [The Master Tutorial (5-Part Framework)](#5-the-master-tutorial-5-part-framework)
   - 5.1 [Goal Definition](#51-goal-definition)
   - 5.2 [Resource Gathering](#52-resource-gathering)
   - 5.3 [The Execution](#53-the-execution)
   - 5.4 [Validation](#54-validation)
   - 5.5 [Finalization](#55-finalization)
6. [Case Study: The Flappy Bird Experiment](#6-case-study-the-flappy-bird-experiment)
   - 6.1 [Zero-Shot Baseline](#61-zero-shot-baseline)
   - 6.2 [Standard Prompt](#62-standard-prompt)
   - 6.3 [Advanced Technique-Enhanced Prompt](#63-advanced-technique-enhanced-prompt)
   - 6.4 [Benchmark Results](#64-benchmark-results)
7. [Best Practices & Common Pitfalls](#7-best-practices--common-pitfalls)
8. [Quick-Reference Cheat Sheet](#8-quick-reference-cheat-sheet)
9. [References](#9-references)

---

## 1. Introduction

**Where it lives:** Top of the comprehensive file (`README.md`). **Status: written** — the current README draft's Section 1 satisfies this brief; no further action needed unless you materially change the repo's scope.

**What to write:** A short abstract, 150–250 words, styled like the abstract of a scientific paper — problem, gap, contribution, promise of payoff, in that order. Open with the problem: most prompting guides teach isolated techniques (few-shot, CoT, ToT) but stop short of showing how to *systematically iterate* a prompt toward a high-performance final version. State the gap: prompt refinement is usually a solo, single-model loop — you write, you test, you tweak, using your own judgment as the only critic. Introduce your contribution: the **Multi-LLM Feedback Loop**, a technique where one LLM drafts, several independent LLMs critique, and the original LLM synthesizes the critiques into a refined final prompt — treating prompt engineering as a peer-review process rather than a solitary one. Close with the payoff: readers will leave with both the underlying theory (Sections 2–4) and a proven, benchmarked example of the technique outperforming simpler prompting strategies (Section 6). Do not explain the technique in detail here — that's Section 4's job. This section's only goal is to hook the reader and set expectations for the rest of the repo.

**Tone note:** Confident and precise, not salesy. Avoid superlatives like "revolutionary" — let the benchmark data in Section 6 do that work later.

---

## 2. Foundations of Prompting

**Where it lives:** Comprehensive file (condensed) + `docs/02-foundations.md` (full depth). **Status: README condensed version written; `docs/02-foundations.md` is your next writing task.**

### 2.1 Zero-Shot, Standard, One-Shot, and Few-Shot Prompting

**What to write:** Define each of the four prompting modes in turn, and for each, apply your **Laptop Repair Specialist analogy** consistently so the reader can track progression across all four:

- **Zero-Shot:** You hand the specialist a broken laptop and say "fix it" — no context, no example of what "fixed" looks like, no constraints. Define zero-shot prompting as instructing the model to perform a task with no examples of the desired output, relying entirely on its pretrained knowledge.
- **Standard Prompting:** You add a written description — "the laptop won't turn on, battery is at 40%, no charging light" — more detail, but still no example of a completed repair. Define this as adding explicit task instructions, constraints, or context without providing worked examples.
- **One-Shot:** You show the specialist one completed repair ticket as a template — "here's how I documented the last similar job." Define one-shot as supplying exactly one example of the input-output pattern you want replicated.
- **Few-Shot:** You hand over three or four completed repair tickets covering different fault types, so the specialist can infer the general documentation pattern and apply it to a novel case. Define few-shot as supplying multiple examples to help the model infer a pattern, format, or reasoning style.

For each mode, include: (a) the one-line definition, (b) the analogy beat, (c) a short generic prompt-syntax example (2–3 lines, not full code), (d) one sentence on when an intermediate practitioner would reach for it.

### 2.2 The Efficiency Tradeoff

**What to write:** This is your key nuance and should not be treated as a footnote — give it real space. Explain that increasing the number of shots does not scale performance linearly, and in smaller/lower-parameter models specifically, additional examples can *degrade* output quality rather than improve it. Cover the likely mechanisms an intermediate reader will find credible: (1) smaller context windows and weaker long-range attention mean later examples can dilute or override earlier instructions; (2) smaller models are more prone to overfitting to surface patterns in the examples (e.g., copying formatting quirks rather than the underlying task logic) instead of generalizing; (3) added token length increases the chance of the core instruction getting "lost" relative to the examples. Give a practical rule of thumb: for smaller/local models, test 1-shot and 3-shot before assuming more is better, and treat "more examples" as a hypothesis to benchmark, not a default best practice. Tie this section forward to Section 6, where the reader will see this principle demonstrated empirically.

**Currency note to weave in:** Since these techniques were first cataloged, native *reasoning models* (OpenAI's o-series and GPT-5.x, Anthropic's reasoning-enabled Claude, Google's Gemini, DeepSeek-R1, and open-weight reasoners like GPT-OSS) now perform chain-of-thought internally by default. State the practical consequence plainly: explicit CoT/ToT scaffolding yields the *largest marginal benefit on smaller and local models* that don't reason natively, and the *smallest* on frontier reasoners that already do. This directly reinforces this section's small-model thesis and explains why the case study's evaluator (once decided — see Section 6 and Locked Decisions) is a fair, representative test bed rather than an arbitrary pick.

**New evidence to fold in when you write this section (Run 1 result):** the case study didn't just demonstrate shot-count degradation in theory — it produced a second, closely related small-model finding worth citing here: *single-run variance*. The same well-engineered prompt, generated once by a small local model, dropped an explicitly required feature (ground/ceiling collision — see Section 6.4) that a simpler prompt handled correctly. This isn't a shot-count effect, but it belongs in the same "small models don't reliably reach the ceiling a good prompt sets" family of cautions, and 2.2 is the natural place to plant that seed before Section 6 pays it off in full.

---

## 3. The Prompt Engineering Toolkit

**Where it lives:** Comprehensive file (condensed definitions) + `docs/03-toolkit.md` (full depth per technique). **Status: README condensed version written; `docs/03-toolkit.md` is your next writing task after 2.**

**Framing note for this whole section:** Open with a short paragraph explaining that this toolkit is organized into three functional categories — not a flat alphabetical list — because each category answers a different question: *how does the model reason* (3.1), *how does the model improve its own instructions* (3.2), and *how do you shape the model's behavior through format and framing* (3.3). This framing paragraph is what prevents the section from reading as a grab-bag, so don't skip it.

### 3.1 Reasoning & Structure Frameworks

**What to write:** Cover the techniques below, each with: a plain-language definition, a minimal illustrative example (a sentence of prompt text, not a full case study — save that for Section 6), and one sentence on the tradeoff (cost, latency, or complexity) it introduces.

- **Chain-of-Thought (CoT):** Prompting the model to externalize intermediate reasoning steps before producing a final answer, improving performance on multi-step logical or arithmetic tasks. Note the tradeoff: longer outputs, higher token cost. (Cross-reference the 2.2 currency note: on native reasoning models this is now often automatic.)
- **Tree-of-Thoughts (ToT):** An extension of CoT where the model explores multiple reasoning branches in parallel, evaluates them, and prunes weaker paths before converging on an answer — useful for problems with multiple viable solution paths. Note the tradeoff: significantly higher compute/latency cost, generally reserved for complex planning or search-like tasks.
- **ReAct (Reason + Act):** A pattern where the model interleaves reasoning steps with actions (e.g., tool calls, searches) and observations, looping until it reaches a final answer — the foundation of most modern agentic systems. Note that this is less about a single prompt and more about a prompting *pattern* used in multi-turn/tool-using systems.
- **Self-Correction Techniques — Self-Consistency, Reflexion, and Self-Refine (grouped):** Explain all three as variations on one core idea — the model checking or improving its own output — while being precise that the mechanisms differ. **Self-Consistency** samples multiple independent reasoning paths for the same problem and takes the majority/most consistent answer. **Reflexion** has the model critique its own prior attempt in natural language and use that critique to generate an improved attempt, often across multiple iterations. **Self-Refine** is the tightest, most widely cited version of the loop today: generate → self-critique → revise, repeated until quality plateaus. Keep each to a tight paragraph, not three long standalone entries. **Why Self-Refine earns its spot:** it is the direct single-model ancestor of the Multi-LLM Feedback Loop — the technique in Section 4 is, in one sentence, "Self-Refine, but the critique step is delegated to several *independent* models instead of the same one."

### 3.2 Meta-Prompting

**What to write:** This subsection is your conceptual bridge to Section 4, so end it with a transition sentence rather than letting it dead-end. Define:

- **Automatic Prompt Engineering (APE):** Using an LLM to generate, evaluate, and select candidate prompts for a given task automatically, often by generating many variants and scoring them against a metric or held-out examples. **Currency note:** flag that APE's ideas have matured into named, tooling-backed *automated prompt optimization* frameworks (e.g., DSPy) that treat prompts as compiled, optimizable modules rather than hand-written strings. One sentence is enough — you're scoping the frameworks themselves out (see Section 9 Further Reading).
- **Conversational Prompt Engineering (CPE):** An interactive process where a human and an LLM iteratively refine a prompt together through dialogue — the human states a goal, the LLM proposes a prompt, the human gives feedback, and the LLM revises.

Close the subsection with a bridging paragraph: APE, CPE, and Self-Refine (from 3.1) all demonstrate that prompts themselves can be treated as objects to be engineered, tested, and revised — not just written once. The Multi-LLM Feedback Loop (Section 4) extends this same idea across *multiple independent models acting as critics*, rather than a single model, a single human-model pair, or an automated optimizer scoring against one metric.

### 3.3 Practical Enhancers

**What to write:** Two lightweight, practical techniques, kept brief and concrete:

- **XML Tags:** Using structural tags (e.g., `<context>`, `<instructions>`, `<example>`) to delimit distinct parts of a prompt, which measurably improves instruction-following in many models by making the prompt's structure unambiguous. Include one short example prompt.
- **Emotional Prompting:** Adding stakes, urgency, or emotional framing to a prompt (e.g., "this is critical for my job") which some research and practitioner testing has shown can nudge output quality or effort in certain models. Present this evenhandedly — note that results are model-dependent and inconsistent, so frame it as "a lever worth testing" rather than a guaranteed win.

> **Scope note (do not re-add):** `r.jina.ai` is deliberately **not** a Toolkit technique. It's a resource-gathering *tool*, so it lives in Section 5.2, not here.

---

## 4. Introducing the Multi-LLM Feedback Loop

**Where it lives:** Comprehensive file (full — this is your core differentiator and deserves complete treatment in the main file, not just a summary) + `docs/04-feedback-loop.md` for extended examples. **Status: README full version written; `docs/04-feedback-loop.md` is a queued deep-dive — see brief below and the note on what's new to fold in now that Run 1 is complete.**

### 4.1 Core Concept & Why It Works

**What to write:** This is the most important section in the repository — write it with the most care. Walk through the three-step loop explicitly:

1. **Draft (Architect):** LLM 'A' produces an initial prompt for a defined task.
2. **Critique (Critics):** The draft is distributed, unmodified, to multiple *different* LLMs (different vendors or model families, not just different instances of the same model) which independently review it for ambiguity, missing constraints, failure modes, and structural weaknesses.
3. **Synthesize (Architect, again):** All critiques are fed back to the original Architect model, which reconciles overlapping or conflicting feedback and produces a refined prompt.

Explain *why* this works, not just what it is: a single model, even a strong one, has blind spots and biases baked into its own training — it's a weak self-critic on its own outputs (the same failure mode that limits pure self-reflection techniques like Reflexion and Self-Refine). Using multiple, architecturally distinct models as critics diversifies the error-detection surface, similar in spirit to ensemble methods or peer review in academic writing — different reviewers catch different blind spots precisely because they weren't trained the same way. Explicitly connect this back to Section 3: APE, CPE, and Self-Refine showed that prompts can be iteratively engineered; this technique scales that iteration across multiple independent evaluators instead of one.

**When you write `docs/04-feedback-loop.md`, use the real Run 1 critique transcripts as your worked example — they're all finalized now.** All four are committed at `case-study/03-advanced-feedback-loop/02-critic-feedback/critic-{gpt-oss,qwen,gemma,phi4}.md`. This is a meaningful upgrade over drafting from a hypothetical example: you can now show, with real quotes, how four differently-trained critics converged on some issues (e.g., more than one critic independently flagged frame-rate independence / delta-time handling as a high-severity gap) and diverged on others, and how the synthesizing Architect (Sonnet 5) had to arbitrate. A concrete worked reconciliation — "critics X and Y both flagged Z, here's how the final prompt resolved it; critic W raised a structural point no one else caught, here's why it was kept" — is exactly the kind of extended example this deep-dive file exists for, and you didn't have this data available in earlier drafting passes.

**Diagram (locked, do not revisit):** The Architect → Critics (parallel) → Architect → Final Prompt flow is rendered as an **inline Mermaid diagram** directly in the markdown of both `README.md` and `case-study/README.md`. This has been reviewed and confirmed as the final version — GitHub renders it natively, it version-controls as text, and no image tooling or exported PNG is needed. Do not replace it or add a competing exported-image version; `assets/diagrams/` remains an optional, unused slot.

### 4.2 When to Use It (and When Not To)

**What to write:** This section exists to keep the repository credible — no technique is universally correct, and stating limits builds trust. Cover:

- **Use it when:** the task is high-stakes or will be reused many times (production prompts, templates, agents), the failure cost of a mediocre prompt is high, or you're prompting for a domain where you personally lack expertise to judge quality (the critics compensate for your blind spots too).
- **Avoid or skip it when:** the task is one-off/low-stakes (the iteration overhead isn't worth it), you're under tight latency constraints, or the task is simple enough that a single well-constructed CoT or few-shot prompt already performs at ceiling — running a feedback loop against a task that's already saturated wastes calls without improving output.
- **Cost/latency honesty:** Be explicit that this technique multiplies calls (1 draft + N critics + 1 synthesis, minimum), so it should be positioned as a tool for *important, reusable* prompts rather than a default for every prompt you write.

**New nuance to add now that Run 1 is complete:** the loop reliably improves the *prompt*. It does not, by itself, guarantee the *output* — Section 6.4's result is the concrete proof. Say plainly in 4.2 that the Feedback Loop should be paired with the Section 5.4 Validation step; a refined prompt handed to a small or unreliable generator without a separate validation pass can still ship a broken result, and that's exactly what nearly happened in the case study.

---

## 5. The Master Tutorial (5-Part Framework)

**Where it lives:** Comprehensive file (condensed steps) + `docs/05-master-tutorial.md` (full walkthrough with expanded examples). **Status: README condensed version written; `docs/05-master-tutorial.md` is queued — write this after Sections 2–4's deep dives, since it references all of them.**

**Framing note:** Open this section by telling the reader this is the applied, step-by-step version of everything covered so far — Sections 2–4 were the "what," this is the "how, in order."

### 5.1 Goal Definition

**What to write:** Explain that this step is about producing a precise task specification before writing a single word of prompt. Give the reader a concrete checklist to include: What is the exact output format expected (code, prose, JSON, etc.)? Who or what is the output for? What does "success" look like — is there a measurable criterion? What are the hard constraints (length, language, tools allowed)? Emphasize a common intermediate-level mistake: starting to write the prompt before the goal is fully specified, which causes wasted iteration later in Section 5.3.

### 5.2 Resource Gathering

**What to write:** Cover what context needs to be collected before drafting: reference documentation, examples of desired/undesired output, domain-specific constraints, and prior successful prompts if any exist. This is where **r.jina.ai** belongs — introduce it as a practical tool for pulling clean, LLM-readable text from a URL to use as grounding context in a prompt, and give a one-line usage example (prefix any URL with `https://r.jina.ai/`, e.g., `https://r.jina.ai/https://example.com/docs`). Add the practical caveat: unauthenticated use is free but rate-limited (roughly 20 requests/minute), and a free API key raises the limit — fine for the manual, low-volume workflow this repo teaches. Frame the whole section around a single idea: the quality of the Architect's first draft in Section 5.3 is bounded by the quality of the resources it's given here.

### 5.3 The Execution

**What to write:** This is where you formally apply the Multi-LLM Feedback Loop from Section 4 as a concrete procedure. Walk through it as an operational sequence: (1) feed the Goal Definition and gathered Resources to the Architect model to produce Draft v1; (2) send Draft v1 as-is to your chosen set of Critic models with a standardized critique request; (3) collect the critiques. Give the reader the actual reusable critique-request template they can copy — the canonical version lives at `case-study/03-advanced-feedback-loop/00-critique-request-template.md`; reproduce it here so this section is self-contained. The template's defining rule: **reviewers list issues, they do not rewrite.** (Rationale to state briefly: a rewrite collapses N independent critiques into N competing drafts, which defeats the synthesis step — you want diagnosis from the critics and synthesis from the Architect, not five rewrites to reconcile.) Note that this section should read as a procedure the reader can literally follow, not just a description.

**Now that all four Run 1 critiques are finalized, you can grade this template against its own output.** Look at the four transcripts side by side: each independently produced severity-labeled findings across the same four categories (ambiguity, missing requirements, failure modes, structural weaknesses) plus a single prioritized closing recommendation, with no rewrites present in any of them. That's a clean confirmation the template did its job as designed — worth one sentence in this section as evidence the format works, not just a claim that it should.

### 5.4 Validation

**What to write:** Explain the distinction between this step and 5.3's critique step: 5.3 critiques the *prompt itself* before it's ever run; 5.4 validates the *output the prompt produces* once executed, again using secondary LLMs as reviewers. Cover what a good validation request looks like — asking a secondary model to check the output against the original success criteria defined in 5.1, flag hallucinations or unmet constraints, and score quality on a simple rubric. This is also the natural place to introduce the idea of a repeatable evaluation rubric, which sets up Section 6.4's benchmarking approach.

**Important framing to add now:** this step is not yet fully executed in your own case study (see Locked Decisions — the grading model decision and run are your next-update task). Say so honestly in this section rather than implying it's finished: describe what *should* happen at this step (a distinct, non-generator model grading against the rubric, run multiple times and averaged), and note that Section 6 will report the grading results once that step is complete. A guide that models "here's the step we're mid-completing, and here's why" is more credible than one that quietly glosses over its own incomplete step.

### 5.5 Finalization

**What to write:** Cover the closing step: reconciling validation feedback into a final version, and — since this is a prompt engineering technique — briefly note the discipline of *saving* the final prompt as a versioned artifact (a plain-text or markdown file, with a short changelog comment) rather than letting it live only in a chat window. This one or two sentences on version control sets up Section 7's best practices without needing a full standalone section.

---

## 6. Case Study: The Flappy Bird Experiment

**Where it lives:** Comprehensive file (condensed results table + interpretive paragraph) + `case-study/README.md` (full prompts, full code outputs, full benchmark commentary). **Status: both are written and reflect the real Run 1 data. The one open item affecting this section is the grading step — see below.**

**Framing note — the experiment's design:** Open with one paragraph stating the design: the same task (a Flappy Bird clone) is attempted using four progressively more sophisticated prompting approaches, and each resulting program is scored by the same evaluator model using a consistent rubric, so results are comparable across stages.

**Three model roles — state these explicitly, up front, and never conflate them.** The case study involves three distinct model *roles*. Naming them separately is the single most important clarification in this section, because a reader who conflates "the model that wrote the prompt" with "the model that ran it" or "the model that graded it" will misread the entire benchmark:

1. **Architect & Critic models — the *prompt constructors* (Stage 6.3 only).** The Architect drafts and later synthesizes the advanced prompt; the Critics review the draft. These models *build a prompt*; they never execute it and never grade code. They appear **only** in Stage 6.3. Roster (as run, final): Architect draft = Claude Opus 4.8; Critics = `gpt-oss:20b`, `qwen3.6:27b`, `gemma4:26b`, `phi4-reasoning:14b` — **all four critique transcripts are now finalized and committed**; Synthesis = Claude Sonnet 5.
2. **The code-generation model — the *prompt executor* (all three stages).** This is the single model that actually *runs* each of the three final prompts (zero-shot, standard, and the synthesized advanced prompt) to produce a Flappy Bird implementation. **It must be held constant across all three stages** (`gpt-oss:20b`, as run) — this is what makes "the prompt improved the output" a defensible claim rather than a confound.
3. **The evaluator — the *grader* (all three stages).** **This role is your one remaining open decision.** In Run 1, the intended grader (`gpt-oss:20b`) was also the generator and one of the four critics — a self-preference risk that has already been flagged and honestly disclosed rather than quietly used anyway. Your next-update task is to pick a grader from a *different* lineage than the generator, fix its reasoning-effort setting, score each program three times, and average. Until that's done, treat every score in 6.4 as provisional/functional-review-only, not final rubric output — and say so explicitly in the prose rather than presenting the table as finished.

A one-line mnemonic worth putting in the prose: **Architect/Critics build the prompt, the generator runs the prompt, the evaluator grades the result — three roles, never merged.**

### 6.1 Zero-Shot Baseline

**What to write:** Show the exact zero-shot prompt used ("Write code for a Flappy Bird clone" or similar minimal instruction — the canonical version is `case-study/01-zero-shot/prompt.md`), executed by the **fixed code-generation model** (role 2). Give a short commentary on what came back — note common failure patterns you'd expect at this stage (missing collision logic, no game-over state, incomplete scoring) without yet giving the numeric score, which belongs in 6.4.

**When you add gameplay screenshots (your other queued next-update task), this is a natural place for the zero-shot screenshot** — a short caption noting what the baseline visually looks like running is enough; don't let the image substitute for the functional commentary above.

### 6.2 Standard Prompt

**What to write:** Show the upgraded prompt with explicit requirements added (language/framework, game mechanics, controls, win/lose conditions) — canonical version `case-study/02-standard/prompt.md` — again executed by the **same fixed code-generation model**. Briefly note what improved qualitatively versus 6.1. Add its screenshot here when ready, same treatment as 6.1.

### 6.3 Advanced Technique-Enhanced Prompt

**What to write:** This is where the Multi-LLM Feedback Loop is actually demonstrated end-to-end on a concrete task, and the only stage where the Architect and Critic roles appear. Show: the Architect's initial draft prompt for the Flappy Bird task (`case-study/03-advanced-feedback-loop/01-architect-draft.md`), a condensed summary of what the Critic models flagged (2–4 bullet points is enough — don't reproduce full critique transcripts here; those live per-critic in `case-study/03-advanced-feedback-loop/02-critic-feedback/`, **all four now finalized**), and the final synthesized prompt that resulted (`03-final-prompt.md`). Make the role boundary visible in the prose: the Architect and Critics produce the *prompt*; that final prompt is then handed to the **same fixed code-generation model** used in 6.1 and 6.2 to produce the actual implementation. This section is your proof-of-concept — treat it as the centerpiece of the whole repository. Add the advanced-stage screenshot here too when ready — and given the known ground/ceiling collision bug (6.4), consider a short caption noting what to look for if you want the screenshot to visually corroborate the bug rather than just show a nice-looking bird sprite.

### 6.4 Benchmark Results

**What to write:** Present a comparison table with rows for Zero-Shot / Standard / Advanced, and columns for the rubric dimensions you score with the evaluator (correctness, completeness, code quality, adherence to constraints), plus an overall score per stage. State the evaluation method explicitly and briefly, per the Locked Decision below:

- **Generation:** one run per stage, produced by the fixed code-generation model at a disclosed, fixed decoding setting (state the temperature/seed you actually used). Disclose single-run generation honestly as a limitation — this is a clear demonstration of technique differences, not a statistically averaged benchmark.
- **Evaluation:** currently an independent functional review (each program run headlessly + code inspected), pending the actual grading-model decision and run. Once decided, score each program three times with the chosen grader at a fixed reasoning-effort level and average, to smooth grader-side variance without multiplying the manual generation work. Report the averaged score and, if you like, the spread.

Close with a short interpretive paragraph — not just the raw numbers — connecting the score progression back to the techniques introduced in Sections 2–5. **Keep the honest, non-monotonic Run 1 finding exactly as documented: prompt quality improved sharply and monotonically, but generated-code quality did not** — the advanced stage scored lowest (7.0) despite the best-engineered prompt, because the single generation run dropped the required ground/ceiling collision check. Say plainly that this is the §2.2/§5.4 caution playing out in real data, not a result to reframe as a clean win. **Do not let the eventual distinct-grader re-scoring quietly smooth this over** — if the new scores still show the same non-monotonic pattern, report it as further confirmation; if they *don't* reproduce it, report that discrepancy honestly too rather than picking whichever scoring run tells the nicer story.

---

## 7. Best Practices & Common Pitfalls

**Where it lives:** Comprehensive file (condensed list) + optional `docs/07-pitfalls.md` if you want extended examples per pitfall. **Status: README condensed version written; `docs/07-pitfalls.md` is optional and lowest priority.**

**What to write:** A practical, scannable section — bullets are appropriate here more than prose. Cover: over-prompting (piling on constraints until the model loses the core instruction), shot-count bloat (tie back explicitly to Section 2.2), conflicting instructions across a long prompt, treating Critic feedback as universally correct without reconciling contradictions between critics, letting a Critic *rewrite* instead of *diagnose* (tie back to 5.3), skipping Goal Definition (Section 5.1) and iterating blind, conflating the three case-study model roles (tie back to Section 6), and forgetting to version-control final prompts (tie back to Section 5.5). Each pitfall: one sentence describing it, one sentence on the fix.

**Ninth pitfall to add, earned by Run 1 itself:** skipping output validation (§5.4). The fix: even a well-reviewed prompt needs a distinct-model grading/validation pass before you trust the output, because prompt quality and output quality are not the same axis — precisely the gap the grading-model task (still open) exists to close.

---

## 8. Quick-Reference Cheat Sheet

**Where it lives:** Comprehensive file **only** — do **not** split this into the deep-dive docs, and do **not** create a separate `docs/glossary.md` for it. **Status: written, README-only, confirmed not duplicated anywhere.**

**What to write:** A single table or tightly formatted list mapping every named technique in the repo — Zero/One/Few-Shot, CoT, ToT, ReAct, Self-Consistency, Reflexion, Self-Refine, APE, CPE, XML tags, Emotional Prompting, and the Multi-LLM Feedback Loop — to a one-line definition and a "use when" tag. This is a lookup tool, not a teaching tool — keep every entry to one line.

---

## 9. References

**Where it lives:** Comprehensive file, final section. **Status: written.**

**What to write:** List sources actually used while researching each technique (papers, official documentation, blog posts) grouped by the section they support, plus a short **"Further Reading"** subsection pointing toward adjacent topics you deliberately scoped out so readers know the technique's place in the wider landscape without you having to teach it here. Scoped-out adjacents worth naming: automated prompt-optimization frameworks such as **DSPy** (the tooling successor to APE, from 3.2); reasoning-path variants not covered in 3.1 — **Step-Back**, **Least-to-Most**, **Graph-of-Thoughts**; the broader discipline of **context engineering**; and **multi-agent orchestration frameworks** (the natural next step beyond a single feedback loop). For GPT-OSS-20B, cite the OpenAI model card (arXiv 2508.10925, August 2025, Apache 2.0). For r.jina.ai, cite the Jina Reader docs.

---

## Locked Decisions (confirmed — reflects the real, current state of the repo)

- **Model roster (Section 6.3) — as run, final.**
  - **Architect (draft v1):** Claude Opus 4.8 (Anthropic).
  - **Critics (four architecturally distinct open-weight lineages):** `gpt-oss:20b` (OpenAI), `qwen3.6:27b` (Alibaba/Qwen), `gemma4:26b` (Google/Gemma), `phi4-reasoning:14b` (Microsoft/Phi). **All four transcripts are finalized and committed; nothing further to do here.**
  - **Synthesis (final prompt):** Claude Sonnet 5 (Anthropic).
  - *Rationale:* The premise — a diverse error-detection surface from *different training lineages* — is fully satisfied by four distinct open-weight families, and using local models makes the whole loop reproducible at zero cost, which suits the repo's small-/local-model theme.
- **Benchmark methodology (Section 6.4) — current state and open task.** One code-generation run per stage, generator (`gpt-oss:20b`) held constant. **Open task:** the intended grader was `gpt-oss:20b`, but since it was also generator and one of the four critics, a distinct grader must be chosen for v2 to avoid self-preference bias — this is explicitly your next-update item, not a settled decision. Once chosen: fix its reasoning-effort setting, grade each program 3× and average.
- **Code language/framework (Section 6).** Python + **pygame-ce** (the actively maintained community fork of Pygame; `pip install pygame-ce`, import is still `import pygame`). Confirmed, no change.
- **Diagrams (Section 4.1).** Inline **Mermaid** diagram in the markdown, used in both `README.md` and `case-study/README.md`. **Confirmed final this pass — reviewed and explicitly approved, no PNG export planned, no further changes needed.**
- **Evaluator (Section 6.4).** Grader model **not yet chosen** — this is the single most important open item in the whole repo right now. Keep gpt-oss-class models as an option if you want, but it must be a *different* specific model/lineage from the generator to be valid. Once chosen, fix its reasoning-effort setting for reproducibility and document the choice with a one-line rationale, the same way every other roster decision in this file is documented.
- **Repository housekeeping.** `LICENSE`, `CONTRIBUTING.md`, and `.gitignore` are confirmed present in the repository — no action needed.
- **Screenshots.** Not yet added. Queued as a next-update task: one gameplay screenshot per stage (6.1, 6.2, 6.3), placed in `assets/screenshots/`, referenced inline in `case-study/README.md` with a short caption. Optional for `README.md` itself — the condensed Section 6 doesn't need to carry images if the full case-study file does.

---

## Your Next-Update Checklist

This is the actionable summary of everything still open, pulled out of the sections above so you don't have to hunt for it:

1. **Decide and run the grading model.** Pick a model from a different lineage than the generator (`gpt-oss:20b`) and not already used as one of the four critics. Fix its reasoning-effort setting. Score each of the three `flappy_bird.py` programs 3× and average. Update `evaluation.md` in each stage folder and `benchmark-results.md` with the real numbers, replacing the current "functional review" scores or clearly labeling both if you want to preserve the comparison.
2. **Add gameplay screenshots.** One per stage, into `assets/screenshots/`, referenced from `case-study/README.md` (6.1–6.3).
3. **Write the four `docs/` deep-dives, in this order:** `02-foundations.md` → `03-toolkit.md` → `04-feedback-loop.md` → `05-master-tutorial.md`. Use the briefs above — note the two sections (4.1 and 5.3) that now specifically call out using the real, finalized critic transcripts as worked examples, which you couldn't do in earlier drafts.
4. **Optional:** `docs/07-pitfalls.md`, extended pitfall examples.
5. **Revisit `README.md` once the deep-dives exist**, to make sure the condensed sections still match the full versions in tone and emphasis — not a rewrite, just a consistency pass.

---

## Appendix A: Changelog (what changed this revision and why)

- **All four critic transcripts confirmed finalized.** Previously `critic-gpt-oss.md`, `critic-gemma.md`, and `critic-phi4.md` were stubs pending pasted-in data; `critic-qwen.md` was confirmed identical to the original model output. All four are now treated as done throughout this guide, including in Section 4.1 and 5.3, which now specifically recommend using them as real worked examples in the deep-dive writing. *Why:* this was the single largest "not yet done" item in the previous revision, and it's now closed.
- **Grading model decision and run explicitly separated out as the one major open item**, rather than being folded into "Locked Decisions" as if resolved. Section 5.4, 6 (role 3), and 6.4 all now say plainly that scores are provisional (functional-review-only) until this happens, and give the reasoning-effort/3x-averaging procedure to follow once a grader is chosen. *Why:* the previous draft's Locked Decisions section described this as something "to do in v2" in a way that risked being treated as settled; it isn't, and the guide should be honest about that at every point where it matters, not just once.
- **Screenshots added as an explicit queued task** in Section 6.1–6.3 and the Next-Update Checklist. *Why:* newly confirmed as planned but not yet done.
- **LICENSE, CONTRIBUTING.md, and .gitignore confirmed present** — removed as an open question from Locked Decisions. *Why:* confirmed directly.
- **Diagram explicitly marked as reviewed and approved, with no further changes planned.** *Why:* previously left as a "decision locked" note without confirmation it had actually been reviewed against the rendered output; now confirmed.
- **New nuance added to Section 4.2 and the ninth pitfall in Section 7**, tying the Feedback Loop's known limitation (improves the prompt, doesn't guarantee the output) explicitly to the still-open validation/grading task, so a future reader understands *why* that task matters and isn't just told to do it.
- **Added a "Your Next-Update Checklist" section** at the end, consolidating every open action item in one place so future-you doesn't have to re-read the whole document to find what's left.
