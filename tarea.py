import numpy as np
from matplotlib import pyplot as plt, ticker

fm = 2000

tick = 1 / fm

channels = []
for i in range(1, 6):
    fid = open(f'S-31/REGTOT11.C{i}', 'rb')
    c = np.fromfile(fid, np.int16)
    c = c[15*2000:]
    channels.append(c)

for idx in range(len(channels)):
    channels[idx] = list(filter(lambda x: x != 0, channels[idx]))

ax = plt.subplot(111)

for i in channels:
    new_y = np.arange(0, len(i), 1000)
    new_x = []
    for j in new_y:
        new_x.append(i[j])

    ax.plot(new_y, new_x, label='distolica')


# FuncFormatter can be used as a decorator
@ticker.FuncFormatter
def major_formatter(x, pos):
    return "%d" % (int(x) / 2000)


ticks = np.arange(0, len(channels[0]), 2000)
ax.xaxis.set_ticks(np.arange(0, len(channels[0]), 20000))
ax.xaxis.set_major_formatter(major_formatter)
# plt.xticks(ticks)

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# plt.plot(range(0, len(channels[4])), channels[4])
plt.xlabel('Time (s)')
plt.ylabel('Amp (mV)')
plt.show()

# Shrink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.show()
