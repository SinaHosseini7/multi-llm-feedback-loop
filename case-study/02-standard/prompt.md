# Stage 2 — Standard Prompt

> **⚠️ STUB — verbatim prompt text pending.**
> The exact standard-stage prompt used in Run 1 was not included in the assembly bundle. Paste it here verbatim, replacing this notice. Per the repo's integrity rules, it must **not** be reconstructed from memory or from the description below — experimental artifacts are committed exactly as used, or clearly marked as missing.

**What it was (from the Run 1 records):** a conventional, careful specification of roughly seven explicit requirements — game mechanics, controls, win/lose conditions, scoring, restart behavior, a fixed window size, and no external asset files — but without delta-time physics, unit definitions, or edge-case handling (those only appear in the Stage 3 prompt).

**Role boundary:** this prompt was executed by the fixed **code-generation model** (`gpt-oss:20b`) — the same generator used in all three stages — to produce `flappy_bird.py` in this folder. No Architect or Critic models were involved at this stage. See `evaluation.md` for the functional review of the output.
