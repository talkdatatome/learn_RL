import gymnasium as gym

if __name__ == "__main__":
    env = gym.make("LunarLander-v2", render_mode="human")
    obs, info = env.reset()
    
    for _ in range(1000):
        action = env.action_space.sample() # real policy goes here...
        obs, reward, terminated, truncated, info = env.step(action)
    
        if terminated or truncated:
                obs, info = env.reset()
    
    env.close()
