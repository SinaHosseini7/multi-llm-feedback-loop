#!/usr/bin/env python3
"""
A minimal, fully‑runnable Flappy Bird clone using only pygame primitives.
Author: ChatGPT (OpenAI)
"""

import sys
import random

import pygame


# --------------------------- Configuration ----------------------------------
WIDTH = 400          # Window width in pixels
HEIGHT = 600         # Window height in pixels
FPS = 60             # Frames per second

GRAVITY = 0.4        # Downward acceleration per frame
FLAP_STRENGTH = -9   # Velocity set when the bird flaps

PIPE_SPEED = 3       # Horizontal speed of pipes (pixels per frame)
PIPE_WIDTH = 50      # Width of each pipe
GAP_HEIGHT = 150     # Height of the gap between top and bottom pipes
GROUND_HEIGHT = 100  # Height of the ground area at the bottom

SPAWN_INTERVAL = 1500          # Milliseconds between new pipe pairs
MIN_GAP_Y = GAP_HEIGHT // 2 + 50           # Minimum centre Y for the gap
MAX_GAP_Y = HEIGHT - GROUND_HEIGHT - GAP_HEIGHT // 2 - 50  # Maximum centre Y


# --------------------------- Colors ---------------------------------------
SKY_COLOR = (135, 206, 235)      # Light blue sky
BIRD_COLOR = (255, 215, 0)       # Gold bird
PIPE_COLOR = (34, 139, 34)        # Forest green pipes
GROUND_COLOR = (184, 134, 11)     # Dark goldenrod ground
TEXT_COLOR = (255, 255, 255)      # White text


# --------------------------- Game Objects ----------------------------------
class Bird:
    """The player bird."""

    def __init__(self):
        self.radius = 18                     # Bird size
        self.x = WIDTH // 4                   # Horizontal position is fixed
        self.y = HEIGHT / 2                   # Start in the middle vertically
        self.vel_y = 0                        # Vertical velocity

    @property
    def rect(self) -> pygame.Rect:
        """Return a Rect that bounds the bird (used for collision)."""
        return pygame.Rect(int(self.x - self.radius),
                           int(self.y - self.radius),
                           self.radius * 2,
                           self.radius * 2)

    def update(self):
        """Apply physics to the bird."""
        self.vel_y += GRAVITY
        self.y += self.vel_y

    def flap(self):
        """Make the bird jump upward."""
        self.vel_y = FLAP_STRENGTH

    def draw(self, surface: pygame.Surface):
        """Render the bird as a circle."""
        pygame.draw.circle(surface, BIRD_COLOR,
                           (int(self.x), int(self.y)),
                           self.radius)


class PipePair:
    """A pair of top and bottom pipes with a vertical gap."""

    def __init__(self):
        self.width = PIPE_WIDTH
        self.x = WIDTH                    # Start just off the right edge
        self.gap_center_y = random.randint(MIN_GAP_Y, MAX_GAP_Y)
        self.passed = False                # Whether the bird has passed this pair

    @property
    def top_rect(self) -> pygame.Rect:
        """Rect of the upper pipe."""
        height = self.gap_center_y - (GAP_HEIGHT // 2)
        return pygame.Rect(int(self.x), 0, self.width, max(0, int(height)))

    @property
    def bottom_rect(self) -> pygame.Rect:
        """Rect of the lower pipe."""
        y_start = self.gap_center_y + (GAP_HEIGHT // 2)
        height = HEIGHT - GROUND_HEIGHT - y_start
        return pygame.Rect(int(self.x), int(y_start),
                           self.width, max(0, int(height)))

    def update(self):
        """Move the pipes leftward."""
        self.x -= PIPE_SPEED

    def draw(self, surface: pygame.Surface):
        """Render both pipes."""
        if self.top_rect.height > 0:
            pygame.draw.rect(surface, PIPE_COLOR, self.top_rect)
        if self.bottom_rect.height > 0:
            pygame.draw.rect(surface, PIPE_COLOR, self.bottom_rect)


# --------------------------- Main Game Loop --------------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird Clone")
    clock = pygame.time.Clock()

    # Font objects for rendering text
    font_small = pygame.font.SysFont(None, 32)
    font_medium = pygame.font.SysFont(None, 40)
    font_large = pygame.font.SysFont(None, 64)

    # Game state variables
    bird = Bird()
    pipes: list[PipePair] = []
    score = 0
    state = "playing"          # Can be "playing" or "game_over"
    last_pipe_spawn_time = pygame.time.get_ticks()

    running = True
    while running:
        dt = clock.tick(FPS)      # Time passed in milliseconds

        # ------------------------------------------------------------------
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif state == "playing":
                # Flap on spacebar or mouse click
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    bird.flap()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    bird.flap()

            else:  # game_over – restart on space or click
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) \
                        or event.type == pygame.MOUSEBUTTONDOWN:
                    # Reset everything for a new run
                    score = 0
                    pipes.clear()
                    last_pipe_spawn_time = pygame.time.get_ticks()
                    bird = Bird()
                    state = "playing"

        # ------------------------------------------------------------------
        if state == "playing":
            bird.update()

            # Collision with the top of the screen or the ground
            if bird.rect.top <= 0 or bird.rect.bottom >= HEIGHT - GROUND_HEIGHT:
                state = "game_over"

            # Pipe spawning
            current_time = pygame.time.get_ticks()
            if current_time - last_pipe_spawn_time > SPAWN_INTERVAL:
                pipes.append(PipePair())
                last_pipe_spawn_time = current_time

            # Update pipes and check for collisions / scoring
            for p in pipes:
                p.update()

                # Score increment when bird passes a pipe pair
                if not p.passed and p.x + p.width < bird.rect.left:
                    score += 1
                    p.passed = True

                # Collision with pipes
                if bird.rect.colliderect(p.top_rect) or bird.rect.colliderect(p.bottom_rect):
                    state = "game_over"

            # Remove pipes that have moved off screen
            pipes = [p for p in pipes if p.x + p.width > 0]

        # ------------------------------------------------------------------
        # Rendering
        screen.fill(SKY_COLOR)

        # Draw ground
        pygame.draw.rect(screen, GROUND_COLOR,
                         (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

        # Draw pipes
        for p in pipes:
            p.draw(screen)

        # Draw bird
        bird.draw(screen)

        # Display score or game over message
        if state == "playing":
            score_surf = font_small.render(f"Score: {score}", True, TEXT_COLOR)
            screen.blit(score_surf, (10, 10))
        else:
            over_surf = font_large.render("Game Over", True, TEXT_COLOR)
            final_score_surf = font_medium.render(f"Score: {score}",
                                                   True,
                                                   TEXT_COLOR)
            restart_surf = font_small.render(
                "Press Space or Click to Restart",
                True,
                TEXT_COLOR)

            # Center the messages
            over_rect = over_surf.get_rect(center=(WIDTH // 2, HEIGHT // 3))
            final_score_rect = final_score_surf.get_rect(
                center=(WIDTH // 2,
                        HEIGHT // 3 + over_rect.height + 10))
            restart_rect = restart_surf.get_rect(
                center=(WIDTH // 2,
                        HEIGHT // 3 + over_rect.height +
                        final_score_rect.height + 20))

            screen.blit(over_surf, over_rect)
            screen.blit(final_score_surf, final_score_rect)
            screen.blit(restart_surf, restart_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
