# Stage 2 — Standard Prompt

**Target file:** `case-study/02-standard/prompt.md`
**Role boundary:** this prompt was executed by the fixed **code-generation model** (`gpt-oss:20b`) — the same generator used in all three stages — to produce `flappy_bird.py` in this folder. No Architect or Critic models were involved at this stage.

The prompt:

```text
Write a Flappy Bird clone in Python using pygame. The game should meet the following requirements:

1. Game mechanics: the bird falls continuously due to gravity and moves upward when the player flaps. Pipes with a gap between them scroll from right to left across the screen, and the bird must pass through the gaps to survive.
2. Controls: pressing the spacebar or clicking the mouse makes the bird flap upward.
3. Win/lose condition: the game ends if the bird collides with a pipe, the ground, or the top of the screen.
4. Scoring: increase the score by one each time the bird successfully passes through a pipe, and display the current score on screen while playing.
5. Restart behavior: when the game ends, show a "Game Over" screen with the final score, and let the player restart by pressing space or clicking.
6. Window: use a fixed window size.
7. No external assets: draw the bird, pipes, ground, and background using pygame's built-in shapes and colors only — do not load any external image or sound files.

Write this as a single, complete, runnable Python script.
```

Seven explicit requirements — mechanics, controls, win/lose conditions, scoring, restart behavior, window size, and asset constraints — but no mention of delta-time physics, explicit units, or edge-case handling (those only show up in the Stage 3 prompt). See `evaluation.md` for the functional review of the output, including where the absence of a delta-time instruction shows up as per-frame physics.

*Note: the verbatim Run 1 prompt text wasn't preserved. This version is reconstructed to match the requirement list on record and the committed `flappy_bird.py`, rather than being the exact original wording.*
