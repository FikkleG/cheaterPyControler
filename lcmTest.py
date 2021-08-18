import time

import gym
import cheetah_gym

env = gym.make("miniCheetah_env-v0")

for _ in range(1000):
    env.step(0)
    time.sleep(0.1)