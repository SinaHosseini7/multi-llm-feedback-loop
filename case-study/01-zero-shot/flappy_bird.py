#!/usr/bin/env python3
# flappy_bird.py
"""
A tiny Flappy‑Bird clone using pygame.
All graphics are drawn with simple shapes (no images needed).
"""

import random
import sys
import math
import pygame

# --------------------------------------------------------------------------- #
# Constants – tweak these to change the feel of the game
# --------------------------------------------------------------------------- #

WIDTH, HEIGHT = 400, 600                # window size
FPS = 60                                 # target frames per second

GRAVITY = 1200.0                        # pixels / s^2
FLAP_STRENGTH = -350.0                  # initial velocity when flapping (negative → up)
BIRD_SIZE = 30                           # width & height of the bird (square)

PIPE_WIDTH = 70
PIPE_GAP_MIN = 150                       # minimal vertical gap between pipes
PIPE_GAP_MAX = 200                       # maximal vertical gap
PIPE_DISTANCE = 250                      # horizontal distance between successive pipe pairs
PIPE_SPEED = 200.0                       # pixels / s

GROUND_HEIGHT = 80                       # height of the invisible “floor”
GRAVITY = 1200.0                         # acceleration due to gravity (px/s^2)

# Colours – all RGB tuples
BG_COLOR      = (135, 206, 235)   # sky blue
BIRD_COLOR    = (255, 255, 0)     # yellow
PIPE_COLOR    = (34, 139, 34)     # forest green
GROUND_COLOR  = (222, 184, 135)   # burlywood
TEXT_COLOR    = (255, 255, 255)   # white

# Game states
START, PLAYING, GAMEOVER = 0, 1, 2


# --------------------------------------------------------------------------- #
# Helper classes: Bird and PipePair
# --------------------------------------------------------------------------- #

class Bird:
    """Simple bird that can flap, falls under gravity, and draws itself."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vy = 0.0          # vertical velocity

    @property
    def rect(self):
        """Return the pygame.Rect representing this bird for collision tests."""
        return pygame.Rect(self.x - BIRD_SIZE // 2,
                           self.y - BIRD_SIZE // 2,
                           BIRD_SIZE, BIRD_SIZE)

    def flap(self):
        """Apply an instantaneous upward velocity."""
        self.vy = FLAP_STRENGTH

    def update(self, dt):
        """Update position using simple Euler integration."""
        self.vy += GRAVITY * dt
        self.y += self.vy * dt

    def draw(self, surface):
        pygame.draw.circle(surface,
                           BIRD_COLOR,
                           (int(self.x), int(self.y)),
                           BIRD_SIZE // 2)


class PipePair:
    """A single pair of pipes: top & bottom."""
    def __init__(self, x):
        self.x = x
        # Randomly decide where the gap starts
        self.gap_y = random.randint(PIPE_GAP_MIN,
                                    HEIGHT - GROUND_HEIGHT - PIPE_GAP_MAX)
        self.height_top   = self.gap_y - (PIPE_GAP_MIN // 2)   # top pipe height
        self.height_bottom = HEIGHT - GROUND_HEIGHT - self.gap_y - (PIPE_GAP_MIN // 2)

    def update(self, dt):
        self.x -= PIPE_SPEED * dt

    @property
    def rect_top(self):
        return pygame.Rect(self.x,
                           0,
                           PIPE_WIDTH,
                           self.height_top)

    @property
    def rect_bottom(self):
        return pygame.Rect(self.x,
                           HEIGHT - GROUND_HEIGHT - self.height_bottom,
                           PIPE_WIDTH,
                           self.height_bottom)

    def draw(self, surface):
        pygame.draw.rect(surface, PIPE_COLOR, self.rect_top)
        pygame.draw.rect(surface, PIPE_COLOR, self.rect_bottom)


# --------------------------------------------------------------------------- #
# Main Game class
# --------------------------------------------------------------------------- #

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Flappy Bird – Pygame Clone")
        self.clock = pygame.time.Clock()

        # Fonts
        self.font_big   = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 32)

        self.reset_game()

    def reset_game(self):
        """Prepare everything for a fresh start."""
        self.state = START
        self.score = 0
        self.high_score = getattr(self, 'high_score', 0)   # keep high score across restarts

        self.bird = Bird(WIDTH // 4, HEIGHT // 2)

        # Create initial set of pipes spaced by PIPE_DISTANCE
        first_pipe_x = WIDTH + PIPE_WIDTH
        self.pipes = [PipePair(first_pipe_x + i * PIPE_DISTANCE)
                      for i in range(3)]   # three pairs on screen initially

    def run(self):
        """Main loop."""
        while True:
            dt = self.clock.tick(FPS) / 1000.0   # delta time in seconds
            self.handle_events()
            if self.state == PLAYING:
                self.update(dt)
            self.draw()

    # ----------------------------------------------------------------------- #
    # Event handling (keyboard & mouse)
    # ----------------------------------------------------------------------- #

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # Start or restart the game on spacebar
                if event.key == pygame.K_SPACE:
                    if self.state in (START, GAMEOVER):
                        self.reset_game()
                        self.state = PLAYING
                    else:  # during playing -> flap
                        self.bird.flap()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state in (START, GAMEOVER):
                    self.reset_game()
                    self.state = PLAYING
                else:
                    self.bird.flap()

    # ----------------------------------------------------------------------- #
    # Game logic: physics, collision detection, scoring, pipe management
    # ----------------------------------------------------------------------- #

    def update(self, dt):
        self.bird.update(dt)

        # Update pipes and remove those that have moved off screen
        for pipe in list(self.pipes):  # copy to allow removal while iterating
            pipe.update(dt)
            if pipe.x + PIPE_WIDTH < -100:   # a small buffer before deletion
                self.pipes.remove(pipe)
                # add new pipe at the far right
                max_x = max(p.x for p in self.pipes) if self.pipes else WIDTH
                new_pipe = PipePair(max_x + PIPE_DISTANCE)
                self.pipes.append(new_pipe)

        # Collision detection
        bird_rect = self.bird.rect

        # Ground or ceiling
        if (self.bird.y - BIRD_SIZE // 2 <= 0 or
            self.bird.y + BIRD_SIZE // 2 >= HEIGHT - GROUND_HEIGHT):
            self.state = GAMEOVER
            self.high_score = max(self.score, self.high_score)
            return

        # Pipes
        for pipe in self.pipes:
            if bird_rect.colliderect(pipe.rect_top) or bird_rect.colliderect(pipe.rect_bottom):
                self.state = GAMEOVER
                self.high_score = max(self.score, self.high_score)
                return

        # Scoring: count pipes that have just passed the bird
        for pipe in self.pipes:
            if not getattr(pipe, 'passed', False) and pipe.x + PIPE_WIDTH < self.bird.x - BIRD_SIZE // 2:
                pipe.passed = True
                self.score += 1

    # ----------------------------------------------------------------------- #
    # Rendering: background, pipes, bird, ground & UI text
    # ----------------------------------------------------------------------- #

    def draw(self):
        self.screen.fill(BG_COLOR)

        # Draw all pipes
        for pipe in self.pipes:
            pipe.draw(self.screen)

        # Draw the bird
        self.bird.draw(self.screen)

        # Draw the "ground" as a simple rectangle (optional)
        pygame.draw.rect(self.screen,
                         GROUND_COLOR,
                         (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

        # UI text
        if self.state == START:
            msg = "Press Space or Click to Start"
            txt_surf = self.font_big.render(msg, True, TEXT_COLOR)
            self.screen.blit(txt_surf, txt_surf.get_rect(center=(WIDTH // 2,
                                                                HEIGHT // 2)))
        elif self.state == GAMEOVER:
            msg = f"Game Over! Score: {self.score}"
            txt_surf = self.font_big.render(msg, True, TEXT_COLOR)
            self.screen.blit(txt_surf, txt_surf.get_rect(center=(WIDTH // 2,
                                                                HEIGHT // 2 - 30)))

            high_msg = f"High Score: {self.high_score}"
            high_surf = self.font_small.render(high_msg, True, TEXT_COLOR)
            self.screen.blit(high_surf, high_surf.get_rect(center=(WIDTH // 2,
                                                                   HEIGHT // 2 + 20)))

            restart_msg = "Press Space or Click to Restart"
            restart_surf = self.font_small.render(restart_msg, True, TEXT_COLOR)
            self.screen.blit(restart_surf, restart_surf.get_rect(center=(WIDTH // 2,
                                                                        HEIGHT // 2 + 60)))
        else:   # PLAYING
            score_text = f"Score: {self.score}"
            txt_surf = self.font_small.render(score_text, True, TEXT_COLOR)
            self.screen.blit(txt_surf, (10, 10))

        pygame.display.flip()


# --------------------------------------------------------------------------- #
# Entrypoint
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    Game().run()
