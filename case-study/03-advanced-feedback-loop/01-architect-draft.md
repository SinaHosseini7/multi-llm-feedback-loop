# Stage 3 — Architect Draft v1

**Target file:** `case-study/03-advanced-feedback-loop/01-architect-draft.md`
**Produced by:** the Architect (draft role) — **Claude Opus 4.8** — from the Goal Definition and Resources for the Flappy Bird task (see §5.1–5.2 of the main guide).
**What happens next:** this draft is sent *unmodified* to four independent Critic models via `00-critique-request-template.md`; the four critiques (`02-critic-feedback/`) plus this draft are then reconciled by the synthesizing Architect (Claude Sonnet 5) into `03-final-prompt.md`.
**Deliberately not airtight:** the draft leaves the timing model, difficulty curve, determinism, and collision precision underspecified — exactly the kinds of gaps the critique round exists to surface.

> The block below is the exact draft prompt, reproduced verbatim.

---

**PROMPT** (copy everything inside this block):

```text
<role>
You are a senior game developer who writes clean, idiomatic, well-structured
Python. You produce complete, runnable programs, not sketches or snippets.
</role>

<task>
Write a single-file Flappy Bird clone in Python using pygame. The program must run
as-is with `python flappy_bird.py` after `pip install pygame-ce`, using no external
image, font, or sound asset files — render everything with pygame drawing
primitives and the default font.
</task>

<mechanics>
- The bird is affected by constant downward gravity and moves upward by a fixed
  impulse each time the player flaps.
- The player flaps by pressing the spacebar or clicking the mouse.
- Pipes spawn at the right edge with a randomized vertical gap position and scroll
  left at a constant speed. The gap the bird passes through has a fixed height.
- The game ends when the bird collides with a pipe, the ground, or the top of the
  playfield.
- The score increases by 1 for each pair of pipes the bird successfully passes.
- After a game over, the player can restart with a keypress without relaunching the
  program.
</mechanics>

<presentation>
- Fixed window size, clearly defined as named constants at the top of the file.
- The current score is visible during play; the final score and a restart prompt
  are visible on the game-over screen.
- Keep all tunable values (gravity, flap impulse, pipe speed, gap size, spawn
  interval, window dimensions, FPS) as named constants grouped together, so the
  game is easy to tune.
</presentation>

<code_quality>
- Organize the code into clear units (e.g., a Bird and a Pipe abstraction, plus a
  main loop). Avoid a single undifferentiated blob.
- Include a short module docstring and brief comments on the non-obvious parts.
- Handle the window-close (quit) event cleanly.
</code_quality>

<success_criteria>
The program is successful if: it launches without errors; the bird responds to
input; pipes spawn, scroll, and can be passed; collisions end the game; the score
increments correctly and displays; and the player can restart after a game over.
</success_criteria>

<final_step>
Before returning your answer, silently re-read this prompt and verify your program
satisfies every item in <success_criteria>. Then return the complete program as a
single code block, followed by one short paragraph listing any assumptions you made.
</final_step>
```
