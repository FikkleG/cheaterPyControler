from gym.envs.registration import register

register(
    id='miniCheetah_env-v0',                                   # Format should be xxx-v0, xxx-v1....
    entry_point='cheetah_gym.envs:MiniCheetahEnv',              # Expalined in envs/__init__.py
)
