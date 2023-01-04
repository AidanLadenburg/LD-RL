from stable_baselines3 import DQN, PPO, A2C
import os
from ldenv import ld_env

model_name = "2022-06-29_17-00-36_rooted"
model_num = 1800000

env = ld_env()
env.reset()

model = PPO.load(f"Path//To//Model")

episodes = 500

for ep in range(episodes):
    obs = env.reset()
    done = False
    while not done:
        action, _states = model.predict(obs)
        obs, rewards, done, info = env.step(action)
        print(rewards)