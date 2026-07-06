# Stage 3 — Final Synthesized Prompt

**Target file:** `case-study/03-advanced-feedback-loop/03-final-prompt.md`
**How it was produced:** The Architect's Draft v1 (`01-architect-draft.md`) was sent unmodified to four independent open-weight Critic models — `gpt-oss:20b` (OpenAI), `qwen3.6:27b` (Alibaba/Qwen), `gemma4:26b` (Google/Gemma), and `phi4-reasoning:14b` (Microsoft/Phi) — using `00-critique-request-template.md`. The four critiques plus the original draft were then handed to **Claude Sonnet 5**, acting as the synthesizing Architect, which reconciled the feedback into the final prompt below.
**Role boundary:** this is the *prompt*. It is executed by the fixed **code-generation model** (`gpt-oss:20b`) to produce `flappy_bird.py` in this folder — the same generator used for the zero-shot and standard stages.

> The block below is the exact final prompt, reproduced verbatim.

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
<physics_and_timing>
- Use delta-time-based physics: compute dt (seconds since last frame) each loop
  iteration and scale all movement/velocity updates by dt, so gameplay speed is
  frame-rate independent regardless of actual FPS achieved.
- Gravity is a constant downward acceleration (units: pixels/sec^2) applied to the
  bird's vertical velocity every frame, scaled by dt.
- Flapping SETS the bird's vertical velocity to a fixed negative (upward) value
  (units: pixels/sec) — it does not add to the existing velocity. This keeps flap
  behavior consistent regardless of current fall speed.
- Clamp the bird's vertical velocity to a sane maximum fall speed to prevent
  collision tunneling through pipes at high velocity.
- Pipe scroll speed is in pixels/sec, scaled by dt.
</physics_and_timing>
<mechanics>
- The bird is affected by constant downward gravity (see physics_and_timing) and
  moves upward by a fixed impulse (velocity set, not added) each time the player
  flaps.
- The player flaps by pressing the spacebar or clicking the mouse. Flapping is
  edge-triggered: a held-down key or held-down mouse button must NOT cause
  repeated flaps. Only a fresh key-down / mouse-down event triggers one flap.
- Pipes spawn at the right edge at a fixed time interval (in seconds, using dt-based
  timing, not frame count), with a randomized vertical gap position. The gap
  position must be constrained so the gap (and the minimum pipe segment above and
  below it) always stays fully within the playfield, never flush against or off
  the top/bottom edges.
- The gap the bird passes through has a fixed height, defined as a named constant.
- Pipe width is a named constant. Choose the spawn interval and pipe speed such
  that consecutive pipes never overlap or visually collide with each other.
- Pipes that have fully scrolled off the left edge of the screen must be removed
  from the active pipe list/collection so the game does not accumulate unbounded
  objects over a long play session.
- Collision detection uses axis-aligned bounding rectangles (pygame.Rect /
  colliderect) between the bird and each pipe segment, and between the bird and
  the ground/ceiling boundaries.
- The ground is a visible strip along the bottom of the window with a defined
  height (named constant); its top edge is the collision boundary. The top of the
  playfield (y = 0) is the collision boundary for the ceiling.
- The game ends immediately when the bird's rect collides with a pipe rect, the
  ground boundary, or the ceiling boundary.
- The score increases by 1 for each pair of pipes the bird successfully passes
  (i.e., when the bird's x-position passes the pipe pair's x-position, checked
  once per pipe pair).
- After a game over, all game state resets on restart: score, bird position/
  velocity, and the pipe list must all be freshly reinitialized — no leftover
  pipes, velocity, or score from the previous run.
- The player restarts by pressing the same flap key/button (spacebar or mouse
  click) while on the game-over screen. This restart input must not itself be
  misinterpreted as a flap in the new game (i.e., debounce the transition so the
  same press doesn't also apply a flap impulse on the first frame of the new run).
- While in the game-over state, gameplay logic (pipe spawning, pipe movement,
  scoring, physics updates) must be fully paused — only the restart-input check is
  active.
</mechanics>
<presentation>
- Fixed window size, clearly defined as named constants at the top of the file.
- The current score is visible during play; the final score and a restart prompt
  are visible on the game-over screen.
- Keep all tunable values (gravity, flap impulse velocity, max fall speed, pipe
  speed, gap size, pipe width, spawn interval, ground height, window dimensions,
  FPS cap) as named constants grouped together near the top of the file, so the
  game is easy to tune. Note: FPS here is only a rendering/clock cap (used for
  clock.tick and dt calculation), not a driver of physics speed — physics must
  remain correct even if the achieved frame rate varies.
</presentation>
<code_quality>
- Organize the code into clear units (e.g., a Bird class, a Pipe class, a
  PipePair/collection abstraction, and a main loop/game-state function). Avoid a
  single undifferentiated blob.
- Include a short module docstring and brief comments on the non-obvious parts
  (e.g., the dt-based physics, gap-position clamping, edge-triggered input,
  restart debounce).
- Handle the window-close (QUIT) event cleanly at all times, including during the
  game-over state.
</code_quality>
<success_criteria>
The program is successful if: it launches without errors; the bird responds to
edge-triggered flap input with velocity-setting impulses; gravity and pipe motion
are dt-scaled and frame-rate independent; pipes spawn at randomized-but-bounded
gap positions, scroll left, and are removed once off-screen; collisions (pipe,
ground, ceiling) end the game reliably even at high fall speed; the score
increments correctly and displays during play; the game-over screen shows the
final score and a restart prompt; and pressing the flap key/button on the
game-over screen fully resets state and starts a fresh run without an accidental
first-frame flap.
</success_criteria>
<final_step>
Before returning your answer, silently re-read this entire prompt — including
<physics_and_timing>, <mechanics>, <presentation>, and <code_quality> — and verify
your program satisfies every item in <success_criteria> as well as every explicit
requirement in the other sections (not just the success criteria list). Then
return the complete program as a single code block, followed by one short
paragraph listing any assumptions you made.
</final_step>
```
