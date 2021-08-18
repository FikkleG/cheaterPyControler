import lcm
from cheetah_gym.envs.control_t import control_t as ctrl

lc = lcm.LCM()

ctrlMsg = ctrl()

lc.publish("pyControl", ctrlMsg.encode())
print('send successfully')
