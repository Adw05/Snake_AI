import pygame
import numpy as np
from snake import Snake
from food import Food
from scoreboard import Scoreboard


class SnakeEnv:
    def __init__(self):
        pygame.init()
        self.width = 600
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake RL (Pygame)")
        self.clock = pygame.time.Clock()

        self.snake = Snake(self.width // 2, self.height // 2)
        self.food = Food()
        self.scoreboard = Scoreboard()
        self.done = False

    def reset(self):
        self.snake.reset()
        self.food = Food()
        self.scoreboard = Scoreboard()
        self.food.refresh()
        self.done = False
        return self.get_state()

    def step(self, action):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Action List: [Straight, Right Turn, Left Turn]
        # Clockwise angles: Right(0), Down(270), Left(180), Up(90)
        clock_wise = [0, 270, 180, 90]
        current_heading = self.snake.get_heading()

        try:
            idx = clock_wise.index(current_heading)
        except ValueError:
            idx = 0

        # Calculate new direction based on relative action
        if action == 1:  # Right Turn
            new_dir = clock_wise[(idx + 1) % 4]
            self.snake.set_direction(new_dir)
        elif action == 2:  # Left Turn
            new_dir = clock_wise[(idx - 1) % 4]
            self.snake.set_direction(new_dir)
        # if action == 0, keep straight

        self.snake.move()
        self.food.move_food()

        # Rewards & Game Over Logic
        reward = 0
        game_over = False

        # 1. Collision
        if self.is_collision():
            game_over = True
            reward = -10
            return self.get_state(), reward, game_over, {}

        # 2. Food Logic
        # Check collision with food rect
        if self.snake.head.colliderect(self.food.rect):
            self.food.refresh()
            self.snake.extend()
            self.scoreboard.add_score()
            reward = 10

        # Check food out of bounds (Wandering logic from original)
        if (self.food.xcor() > self.width - 20 or self.food.xcor() < 0 or
                self.food.ycor() > self.height - 20 or self.food.ycor() < 0):
            self.food.refresh()

        # 3. Time penalty
        reward -= 0.01

        # Render
        self.screen.fill((0, 0, 0))  # Black background
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        self.scoreboard.update_scoreboard(self.screen)
        pygame.display.flip()

        # Speed control ()
        # self.clock.tick(60)

        return self.get_state(), reward, game_over, {}

    def is_collision(self, point=None):
        # Point is expected to be an object with .x, .y attributes or the head rect
        if point is None:
            point = self.snake.head

        # Extract coordinates depending on input type
        if hasattr(point, 'x'):
            px, py = point.x, point.y
        else:  # Tuple
            px, py = point[0], point[1]

        # Wall Collision
        # Adjusted for 0-600 coordinates with 20px padding logic
        if px > self.width - 20 or px < 0 or py > self.height - 20 or py < 0:
            return True

        # Tail Collision
        # Skip the head (first segment)
        for segment in self.snake.segments[1:]:
            if hasattr(point, 'colliderect'):
                if point.colliderect(segment):
                    return True
            else:
                # Manual distance/overlap check if point is tuple
                if segment.collidepoint(px, py):
                    return True
        return False

    def get_state(self):
        head = self.snake.head

        # Points to check around the head (20px offset)
        # simulate checking "potential" future positions
        point_l = (head.x - 20, head.y)
        point_r = (head.x + 20, head.y)
        point_u = (head.x, head.y - 20)  # Up is negative Y
        point_d = (head.x, head.y + 20)  # Down is positive Y

        # Current Heading
        heading = self.snake.get_heading()
        dir_l = heading == 180
        dir_r = heading == 0
        dir_u = heading == 90
        dir_d = heading == 270

        # Helpers
        def check_collision(pt):
            # pt is a tuple (x, y). Check if it hits wall or tail
            return self.is_collision((pt[0], pt[1]))

        def check_wall(pt):
            return pt[0] > self.width - 20 or pt[0] < 0 or pt[1] > self.height - 20 or pt[1] < 0

        # State Vector construction (Logic identical to original)
        state = [
            # 1. Danger Straight
            (dir_r and check_collision(point_r)) or
            (dir_l and check_collision(point_l)) or
            (dir_u and check_collision(point_u)) or
            (dir_d and check_collision(point_d)),

            # 2. Danger Right
            (dir_u and check_collision(point_r)) or
            (dir_d and check_collision(point_l)) or
            (dir_l and check_collision(point_u)) or
            (dir_r and check_collision(point_d)),

            # 3. Danger Left
            (dir_d and check_collision(point_r)) or
            (dir_u and check_collision(point_l)) or
            (dir_r and check_collision(point_u)) or
            (dir_l and check_collision(point_d)),

            # 4. Wall Straight
            (dir_r and check_wall(point_r)) or
            (dir_l and check_wall(point_l)) or
            (dir_u and check_wall(point_u)) or
            (dir_d and check_wall(point_d)),

            # 5. Wall Right
            (dir_u and check_wall(point_r)) or
            (dir_d and check_wall(point_l)) or
            (dir_l and check_wall(point_u)) or
            (dir_r and check_wall(point_d)),

            # 6. Wall Left
            (dir_d and check_wall(point_r)) or
            (dir_u and check_wall(point_l)) or
            (dir_r and check_wall(point_u)) or
            (dir_l and check_wall(point_d)),

            # 7-10. Move Direction
            dir_l, dir_r, dir_u, dir_d,

            # 11-14. Food Location
            self.food.xcor() < head.x,  # Food Left
            self.food.xcor() > head.x,  # Food Right
            self.food.ycor() < head.y,
            # Food Up
            self.food.ycor() > head.y  # Food Down
        ]

        return np.array(state, dtype=int)