# Critique-Request Template

**Target file:** `case-study/03-advanced-feedback-loop/00-critique-request-template.md`
**Purpose:** the standardized request pasted to every Critic model, with the Architect's draft substituted for `{{DRAFT_PROMPT}}`. Sending the *same* template to every critic keeps the four critiques structurally comparable; the **"list issues, do not rewrite"** rule keeps critics diagnosing rather than producing competing drafts (rationale in §5.3 of the main guide).
**Used in Run 1 with:** `gpt-oss:20b`, `qwen3.6:27b`, `gemma4:26b`, `phi4-reasoning:14b` — each in a fresh session with no shared context.
**Outputs:** one transcript per critic, committed verbatim in `02-critic-feedback/`.

> The block below is the exact template, reproduced verbatim.

---

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
