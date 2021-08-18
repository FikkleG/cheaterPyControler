import time
import lcm
from simulator_lcmt import simulator_lcmt as simLcm
import matplotlib.pyplot as plt
ax = []
ay = []
plt.ion()
st = time.time()
def my_handler(channel, data):
    msg = simLcm.decode(data)
    ax.append(time.time() - st)
    ay.append(-1*msg.v[0])
    plt.clf()
    plt.plot(ax,ay)
    plt.pause(0.0002)
    plt.ioff()
lc = lcm.LCM()
subscription = lc.subscribe("simulator_state", my_handler)
try:
    while(True):
        lc.handle()
except KeyboardInterrupt:
    pass
