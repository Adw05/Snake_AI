import time
import pygame
from snake_game.Snake_Game_AI.rl.agent import Agent
from snake_game.Snake_Game_AI.rl.environment import SnakeEnv


def play():
    env = SnakeEnv()
    env.render_mode = True  # Render for viewing
    agent = Agent(state_size=14, action_size=3)

    # Load the model
    agent.load('smart_modelv2.pth')

    # Disable randomness
    agent.epsilon = 0

    print("Game Started!")

    running = True
    while running:
        state = env.get_state()
        action = agent.choose_action(state)
        _, _, done, _ = env.step(action)

        time.sleep(0.05)  # Slower for viewing

        if done:
            head = env.snake.head
            score = env.scoreboard.score

            if (head.x > 580 or head.x < 0 or
                    head.y > 580 or head.y < 0):
                print(f"Game Over: Wall hit")
            else:
                print(f"Game Over: Tail bitten")

            print(f"Final Score: {score}")
            env.scoreboard.draw_game_over(env.screen)
            pygame.display.flip()
            time.sleep(2)
            break

    pygame.quit()


if __name__ == '__main__':
    play()