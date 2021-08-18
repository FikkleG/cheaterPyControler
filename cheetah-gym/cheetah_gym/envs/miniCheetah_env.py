import gym
import lcm
from cheetah_gym.envs.feedBack_t import feedBack_t as fb
from cheetah_gym.envs.control_t import control_t as ctrl
import os
from threading import Thread


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper
@async
def startCXXprocess():
    os.system('bash /home/gj/PycharmProjects/deepGalloping/cheetah-gym/cheetah_gym/envs/startCheetahSim.sh')

class MiniCheetahEnv(gym.Env):
    def simHandler(self,channel, data):
        self.msg = fb.decode(data)
        #print("received a message on \" %s\"" %channel)
    def __init__(self):
        # initial lcm connection and channels and parms
        self.lc = lcm.LCM()
        self.lc.subscribe("pyFeedback", self.simHandler)
        self.visual = False
        self.rsSinal = False
        #start c++ sim, if permission denid, use 'chmod +x startCheetahSim.sh'
        try:
            startCXXprocess()
        except Exception as e:
            print('sim start fail')
            assert False

        #waiting for the first feedback from c++ Sim
        self.lc.handle()
        assert self.msg.isFirst, 'sim is not initial right'
        print('cheetah env initialized')
    def step(self, action):
        ctrlMsg = ctrl()
        #ctrlMsg.controlInfo = action
        ctrlMsg.visual = self.visual
        self.lc.publish("pyControl",ctrlMsg.encode())
        #print('send control successfully')
        self.lc.handle()
        #print('cheetah env step successfully')
        return self.msg.spiData,self.msg.navInfo
    def reset(self):
        resetSinal = ctrl()
        resetSinal.reset = True
        self.lc.publish("pyControl",resetSinal.encode())
        self.lc.handle()
        assert self.msg.isFirst == True, 'sim is not reset right'
        print('cheetah env reset successfully')
        return self.msg.spiData,self.msg.navInfo
    def render(self, mode='human'):
        self.visual = True



if __name__ == "__main__":
    env = gym.make("miniCheetah_env-v0")

    for _ in range(1000):
        env.step(0)
        time.sleep(0.1)