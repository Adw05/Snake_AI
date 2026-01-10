from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import numpy as np
import time


class SnakeEnv:
    def __init__(self):
        self.screen = Screen()
        self.screen.setup(width=600, height=600)
        self.screen.bgcolor("black")
        self.screen.title("Snake RL")
        self.screen.tracer(0)  # Turn off animation for speed

        self.snake = Snake()
        self.food = Food()
        self.scoreboard = Scoreboard()
        self.done = False

    def reset(self):
        self.snake.reset()  # Assuming you added a reset method to snake.py, or recreate it:
        self.screen.clear()
        self.screen.bgcolor("black")
        self.screen.tracer(0)
        self.snake = Snake()
        self.food = Food()
        self.scoreboard = Scoreboard()
        self.food.refresh()
        self.done = False
        return self.get_state()

    def step(self, action):
        # Action List: [Straight, Right Turn, Left Turn]
        # index 0 = Straight, 1 = Right, 2 = Left

        clock_wise = [0, 270, 180, 90]  # Right, Down, Left, Up
        current_heading = self.snake.head.heading()
        idx = clock_wise.index(current_heading)

        # Calculate new direction based on relative action
        if action == 1:  # Right Turn
            new_dir = clock_wise[(idx + 1) % 4]
            self.snake.head.setheading(new_dir)
        elif action == 2:  # Left Turn
            new_dir = clock_wise[(idx - 1) % 4]
            self.snake.head.setheading(new_dir)
        # if action == 0, we do nothing (keep going straight)

        self.snake.move()

        # --- Rewards & Game Over Logic ---
        reward = 0
        game_over = False

        # 1. Collision (Wall or Self)
        if self.is_collision():
            game_over = True
            reward = -10
            return self.get_state(), reward, game_over, {}

        # 2. Food Logic
        if self.snake.head.distance(self.food) < 15:
            self.food.refresh()
            self.snake.extend()
            self.scoreboard.score += 1  # Update internal score
            reward = 10

        # 3. Optional: Time penalty to prevent looping
        # reward -= 0.01

        self.screen.update()

        return self.get_state(), reward, game_over, {}

    def is_collision(self, point=None):
        if point is None:
            point = self.snake.head

        # Wall
        if point.xcor() > 280 or point.xcor() < -280 or point.ycor() > 280 or point.ycor() < -280:
            return True

        # Tail (skip head)
        for segment in self.snake.segments[1:]:
            if point.distance(segment) < 20:
                return True
        return False

    def get_state(self):
        head = self.snake.head

        # Create test points for "Danger" checks
        point_l = (head.xcor() - 20, head.ycor())
        point_r = (head.xcor() + 20, head.ycor())
        point_u = (head.xcor(), head.ycor() + 20)
        point_d = (head.xcor(), head.ycor() - 20)

        dir_l = head.heading() == 180
        dir_r = head.heading() == 0
        dir_u = head.heading() == 90
        dir_d = head.heading() == 270

        # Helper to check collision for a coordinate tuple
        def check(pt):
            # Create a dummy object with xcor/ycor methods for compatibility
            class Pt:
                def xcor(self): return pt[0]

                def ycor(self): return pt[1]

                def distance(self, o):
                    return ((self.xcor() - o.xcor()) ** 2 + (self.ycor() - o.ycor()) ** 2) ** 0.5

            return self.is_collision(Pt())

        state = [
            # Danger Straight
            (dir_r and check(point_r)) or
            (dir_l and check(point_l)) or
            (dir_u and check(point_u)) or
            (dir_d and check(point_d)),

            # Danger Right
            (dir_u and check(point_r)) or
            (dir_d and check(point_l)) or
            (dir_l and check(point_u)) or
            (dir_r and check(point_d)),

            # Danger Left
            (dir_d and check(point_r)) or
            (dir_u and check(point_l)) or
            (dir_r and check(point_u)) or
            (dir_l and check(point_d)),

            # Move Direction
            dir_l, dir_r, dir_u, dir_d,

            # Food Location
            self.food.xcor() < head.xcor(),  # Food Left
            self.food.xcor() > head.xcor(),  # Food Right
            self.food.ycor() > head.ycor(),  # Food Up
            self.food.ycor() < head.ycor()  # Food Down
        ]

        # Convert True/False to 1/0
        return np.array(state, dtype=int)