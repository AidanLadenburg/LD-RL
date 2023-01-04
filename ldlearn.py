from stable_baselines3 import DQN, PPO, A2C
import os
from ldenv import ld_env
import time
import datetime

models = {PPO: "PPO", DQN: "DQN", A2C:"A2C"}

notes = "deterministic"

now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
model_type = PPO
models_dir = f"Path//To//Models"
logdir = f"Path//To//Logs"

if not os.path.exists(models_dir):
	os.makedirs(models_dir)

if not os.path.exists(logdir):
	os.makedirs(logdir)

env = ld_env()
env.reset()

model = model_type('MlpPolicy', env, verbose=1, tensorboard_log=logdir)

TIMESTEPS = 50000
iters = 0
while True:
	iters += 1
	model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=f"{models[model_type]}")
	model.save(f"{models_dir}/{TIMESTEPS*iters}")