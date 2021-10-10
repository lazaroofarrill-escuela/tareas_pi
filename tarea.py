import numpy as np
from matplotlib import pyplot as plt, ticker
from scipy import signal

fm = 2000

tick = 1 / fm

lines = ['observer', 'presion', 'oscilometria', 'oscilometria2', 'picos']

channels = []
for i in range(len(lines)):
    fid = open(f'S-31/REGTOT11.C{i + 1}', 'rb')
    c = np.fromfile(fid, np.int16)

    Wn = .5
    N = 1
    b, a = signal.butter(N, Wn, 'low')
    c = signal.filtfilt(b, a, c)

    channels.append(c)

for idx in range(len(channels)):
    channels[idx] = list(filter(lambda x: x != 0, channels[idx]))

ax = plt.subplot(111)

new_x = []
for i in channels:
    step = 1
    offsets = int(2000 / step)
    new_x = np.arange(0, len(i), step)
    new_x = new_x[15 * offsets:50 * offsets]
    new_y = []
    for j in new_x:
        new_y.append(i[j])
    ax.plot(new_x, new_y)


# FuncFormatter can be used as a decorator
@ticker.FuncFormatter
def major_formatter(x, pos):
    return "%d" % (int(x) / 2000)


ax.xaxis.set_ticks(np.arange(15 * 2000, len(channels[0][:50 * 2000]), 20000))
ax.xaxis.set_major_formatter(major_formatter)
# plt.xticks(ticks)

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(lines, loc='center left', bbox_to_anchor=(1, 0.5))

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
