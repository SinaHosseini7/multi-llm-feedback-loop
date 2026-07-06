# Stage 1 — Zero-Shot Prompt

**Target file:** `case-study/01-zero-shot/prompt.md`
**Role boundary:** this prompt was executed by the fixed **code-generation model** (`gpt-oss:20b`) — the same generator used in all three stages — to produce `flappy_bird.py` in this folder. No Architect or Critic models were involved at this stage.

The entire prompt is a single line:

```text
Write a Flappy Bird clone in Python using pygame.
```

That's it — no constraints, no examples, no success criteria. The point of this stage is to establish what the generator produces from its pretrained defaults alone, so the later stages have an honest baseline. See `evaluation.md` for what came back (spoiler: more than the prompt had any right to expect).
