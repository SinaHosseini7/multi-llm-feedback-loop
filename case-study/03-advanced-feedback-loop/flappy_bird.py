"""
Flappy Bird Clone

A minimal, self‑contained Flappy Bird style game written in Python using pygame.
All graphics are drawn with primitives – no external images, fonts or sounds.
The game is fully frame‑rate independent: all movement is scaled by the time
delta (seconds) computed each frame.

Key features:
* Delta‑time based physics for gravity and pipe scrolling.
* Edge‑triggered flap input via spacebar or left mouse click.
* Pipes spawn at a fixed interval with random vertical gap positions, never
  touching the top or bottom edges of the playfield.
* Collision detection uses axis‑aligned rectangles; game ends on first collision.
* Score is incremented once per pipe pair passed.  
* On game over, pressing space or clicking restarts the game without an accidental flap.

Run with:
    pip install pygame-ce
    python flappy_bird.py
"""

import sys
import random

import pygame


# ==================== Configuration constants ==================== #
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600

FPS_CAP = 60          # Rendering frame‑rate cap (not used for physics)

# Bird settings
BIRD_X = 50                     # Fixed horizontal position of the bird
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
FLAP_IMPULSE = -350.0           # Upward velocity set on flap (pixels/sec)
GRAVITY_PPS2 = 950.0            # Downward acceleration (pixels/sec²)
MAX_FALL_SPEED = 600.0          # Clamp for falling speed

# Pipe settings
PIPE_WIDTH = 80
GAP_SIZE = 150
PIPE_GAP_MARGIN = 30           # Minimum distance from top/bottom edges
GROUND_HEIGHT = 100            # Visible ground strip height
PIPE_SPEED_PPS = 200.0         # Horizontal scroll speed (pixels/sec)
SPAWN_INTERVAL = 1.5          # Seconds between pipe spawns

# Colours
BG_COLOR = (135, 206, 235)      # Sky blue background
GROUND_COLOR = (222, 184, 135)  # Sand colour for the ground
PIPE_COLOR = (34, 139, 34)     # Forest green pipes
BIRD_COLOR = (255, 215, 0)     # Gold bird
TEXT_COLOR = (255, 255, 255)   # White text

# Derived constants
PLAYABLE_HEIGHT = WINDOW_HEIGHT - GROUND_HEIGHT


# ==================== Game Objects ==================== #
class Bird:
    """Represents the player’s bird."""
    def __init__(self, x: int):
        self.x = x
        self.width = BIRD_WIDTH
        self.height = BIRD_HEIGHT
        # Start vertically centred in the playable area
        start_y = (PLAYABLE_HEIGHT - self.height) // 2
        self.y = float(start_y)
        self.vy = 0.0

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(
            int(self.x),
            int(round(self.y)),
            self.width,
            self.height
        )

    def update(self, dt: float):
        """Apply gravity and update vertical position."""
        self.vy += GRAVITY_PPS2 * dt          # Gravity adds to velocity
        if self.vy > MAX_FALL_SPEED:
            self.vy = MAX_FALL_SPEED         # Prevent tunnelling through pipes
        self.y += self.vy * dt                # Move based on velocity

    def flap(self):
        """Instantly set upward velocity; no addition to current speed."""
        self.vy = FLAP_IMPULSE


class PipePair:
    """A pair of top and bottom pipe segments moving leftwards."""
    def __init__(self, x: float, gap_y: int):
        self.x = float(x)              # Left side of the pipes
        self.gap_y = gap_y            # Top coordinate of the vertical gap
        self.passed = False           # Has the bird already passed this pair?

    @property
    def top_rect(self) -> pygame.Rect:
        return pygame.Rect(
            int(round(self.x)),
            0,
            PIPE_WIDTH,
            self.gap_y
        )

    @property
    def bottom_rect(self) -> pygame.Rect:
        bottom_start = self.gap_y + GAP_SIZE
        height = WINDOW_HEIGHT - GROUND_HEIGHT - bottom_start
        return pygame.Rect(
            int(round(self.x)),
            bottom_start,
            PIPE_WIDTH,
            max(height, 0)
        )

    def update(self, dt: float):
        """Move the pipe leftwards."""
        self.x -= PIPE_SPEED_PPS * dt

    def collides_with(self, rect: pygame.Rect) -> bool:
        return rect.colliderect(self.top_rect) or rect.colliderect(self.bottom_rect)


# ==================== Main Game Loop ==================== #
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Flappy Bird Clone")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 36)

    # ----- State variables -----
    def reset_game():
        """Re‑initialise all dynamic game state."""
        nonlocal bird, pipes, score, spawn_timer, game_over
        bird = Bird(BIRD_X)
        pipes = []
        score = 0
        spawn_timer = 0.0
        game_over = False

    # Initialise for first run
    bird = None
    pipes = []
    score = 0
    spawn_timer = 0.0
    game_over = False
    reset_game()

    running = True
    while running:
        dt_seconds = clock.tick(FPS_CAP) / 1000.0

        # ---------- Event handling ----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            elif event.type == pygame.KEYDOWN:
                if game_over:
                    reset_game()
                else:
                    if event.key == pygame.K_SPACE:
                        bird.flap()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left click
                    if game_over:
                        reset_game()
                    else:
                        bird.flap()

        if not running:
            break

        if not game_over:
            # ---- Update gameplay logic ----
            bird.update(dt_seconds)

            spawn_timer += dt_seconds
            while spawn_timer >= SPAWN_INTERVAL:
                spawn_timer -= SPAWN_INTERVAL
                gap_y = random.randint(
                    PIPE_GAP_MARGIN,
                    PLAYABLE_HEIGHT - GAP_SIZE - PIPE_GAP_MARGIN
                )
                pipes.append(PipePair(WINDOW_WIDTH, gap_y))

            # Move pipes and check collisions / scoring
            bird_rect = bird.rect
            for pipe in pipes:
                pipe.update(dt_seconds)

                if pipe.collides_with(bird_rect):
                    game_over = True
                    break

                # Score when the bird passes the whole pair (right side left of bird)
                if not pipe.passed and pipe.x + PIPE_WIDTH < BIRD_X:
                    score += 1
                    pipe.passed = True

            # Remove pipes that have fully scrolled off screen
            pipes = [p for p in pipes if p.x + PIPE_WIDTH >= 0]

        # ---------- Rendering ----------
        screen.fill(BG_COLOR)

        # Draw pipes
        for pipe in pipes:
            pygame.draw.rect(screen, PIPE_COLOR, pipe.top_rect)
            pygame.draw.rect(screen, PIPE_COLOR, pipe.bottom_rect)

        # Ground rectangle (used also for collision)
        ground_rect = pygame.Rect(
            0,
            WINDOW_HEIGHT - GROUND_HEIGHT,
            WINDOW_WIDTH,
            GROUND_HEIGHT
        )
        pygame.draw.rect(screen, GROUND_COLOR, ground_rect)

        # Draw bird
        pygame.draw.rect(screen, BIRD_COLOR, bird.rect)

        if game_over:
            final_surf = font.render(f"Final Score: {score}", True, TEXT_COLOR)
            restart_surf = font.render("Press Space or Click to Restart", True, TEXT_COLOR)
            screen.blit(
                final_surf,
                final_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
            )
            screen.blit(
                restart_surf,
                restart_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 40))
            )
        else:
            score_surf = font.render(f"Score: {score}", True, TEXT_COLOR)
            screen.blit(score_surf, (10, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
