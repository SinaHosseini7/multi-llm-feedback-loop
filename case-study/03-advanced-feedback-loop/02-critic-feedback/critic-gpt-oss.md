# Critic Feedback — gpt-oss:20b

**Role:** Critic — one of four independent open-weight reviewers of the Architect's Draft v1.
**Model:** `gpt-oss:20b` (OpenAI, open-weight). Note: this model also served as the code generator and intended grader in this run — the self-preference caveat is logged in `../../benchmark-results.md`.
**Input:** `../01-architect-draft.md`, sent **unmodified** inside `../00-critique-request-template.md`.
**Rules in force:** list issues only — no rewrites, no code, severity labels, quoted spans, one prioritized change at the end.
**Consumed by:** the synthesizing Architect (Claude Sonnet 5) to produce `../03-final-prompt.md`.

> The transcript below is the critic's raw output, reproduced verbatim.

---

**Ambiguity**

- **Gravity definition** – High – “constant downward gravity” – The prompt does not state whether this is an acceleration added each frame or a constant velocity, leading to inconsistent physics if misinterpreted.  
- **Flap impulse effect** – High – “fixed impulse each time the player flaps” – It’s unclear if the impulse adds to or sets the bird's vertical velocity, which determines how the bird reacts to input.  
- **Restart key mapping** – Medium – “restart with a keypress” – The prompt does not specify which key(s) trigger a restart, so generated code may either fail to restart or accept unintended keys.  
- **Pipe width & spacing** – Medium – “Pipes spawn at the right edge” – No width is provided for pipes, causing ambiguity in rendering and collision detection.  
- **Spawn interval units** – Medium – “spawn interval” – The prompt omits whether this value refers to frames or seconds, leading to unpredictable pipe timing.  
- **Gap vertical bounds** – Medium – “randomized vertical gap position” – Without limits relative to the playfield edges, generated gaps could be impossible to pass or cause off‑screen rendering.  
- **Collision shape/algorithm** – High – No explicit collision detection method is described – ambiguity between bounding boxes, circles, or pixel‑perfect checks can result in missed or false collisions.

---

**Missing requirements / Edge cases**

- **Frame‑rate independence** – High – There’s no requirement that physics be independent of FPS; if tied to frame count the game will run at different speeds on various hardware.  
- **Ground height boundary** – Medium – The “ground” is referenced but its Y coordinate isn’t defined, so ground collision may be calculated incorrectly.  
- **Restart resets all state** – Medium – It’s not stated that score, pipes, and bird state reset after a restart, which can lead to lingering objects or scores persisting across games.  
- **Pipe removal after off‑screen** – Low – Without a clear rule for deleting pipes that have moved past the left edge, the pipe list could grow indefinitely and cause memory pressure.  
- **Continuous key press handling** – Low – The prompt does not clarify whether holding space should apply multiple impulses; ambiguous handling may produce unintended continuous flaps.

---

**Failure modes**

- **Collision skipping due to high speed** – High – If the bird moves fast enough between frames, discrete collision checks might miss a pipe collision and fail to end the game.  
- **Pipe overlap causing false collisions** – Medium – An overly short spawn interval relative to pipe width can cause pipes to intersect, triggering an unintended game over.  
- **No FPS control** – High – Without limiting updates with a clock tick, frame rates will vary, producing inconsistent gameplay speed and potentially high CPU usage.

---

**Structural weaknesses**

- None found; the prompt’s structure is clear and free of contradictions.

---

*Prioritize clarifying whether gravity is an acceleration applied each frame and how the flap impulse modifies vertical velocity (e.g., adds to or sets it), so that the generated code implements physics consistently.*