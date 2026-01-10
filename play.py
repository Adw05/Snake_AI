import time
from agent import Agent
from enviroment import SnakeEnv


def play():
    env = SnakeEnv()
    agent = Agent(state_size=14, action_size=3)

    # Load your saved model (change name if you saved it differently)
    agent.load('./final_model.pth')

    # 1. Turn off Randomness (Exploration)
    agent.epsilon = 0

    game_count = 0

    while True:
        # Get current state

        state = env.get_state()

        # 2. Get Predicted Action (No random moves)
        action = agent.choose_action(state)

        # 3. Perform Move
        _, _, done, _ = env.step(action)

        # 4. Slow down the game so you can watch it!
        time.sleep(0.1)  # Adjust this to change game speed

        if done:
            game_count += 1
            print(f"Game {game_count} Score: {env.scoreboard.score}")
            env.reset()


if __name__ == '__main__':
    play()