import pygame
import random

BLOCK_SIZE = 20
WIDTH = 600
HEIGHT = 600


class Food:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, BLOCK_SIZE, BLOCK_SIZE)
        # Speed = 10
        self.vel_x = 0
        self.vel_y = 0
        self.refresh()
        self.escape_count = 0

    def pick_new_direction(self):

        direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        if direction == 'UP':
            self.vel_x, self.vel_y = 0, -10
        elif direction == 'DOWN':
            self.vel_x, self.vel_y = 0, 10
        elif direction == 'LEFT':
            self.vel_x, self.vel_y = -10, 0
        elif direction == 'RIGHT':
            self.vel_x, self.vel_y = 10, 0

    def refresh(self):
        x = random.randint(1, (WIDTH // BLOCK_SIZE) - 2) * BLOCK_SIZE
        y = random.randint(1, (HEIGHT // BLOCK_SIZE) - 2) * BLOCK_SIZE
        self.rect.x = x
        self.rect.y = y

        # Pick a fresh direction when respawning
        self.pick_new_direction()

    def move_food(self):

        # 1. Apply Momentum (Move in the current direction)
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # 2. Random Turn Chance (5% chance per frame)
        if random.random() < 0.05:
            self.pick_new_direction()


    def xcor(self):
        return self.rect.x

    def ycor(self):
        return self.rect.y

    def add_escape(self):
        self.escape_count += 1

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)  # Red Food