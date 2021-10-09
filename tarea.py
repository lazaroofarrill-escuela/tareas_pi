import numpy as np
from matplotlib import pyplot as plt

fm = 2000

channels = []
for i in range(1, 6):
    fid = open(f'S-31/REGTOT11.C{i}', 'rb')
    c = np.fromfile(fid, np.int16)
    channels.append(c)

for idx in range(len(channels)):
    channels[idx] = list(filter(lambda x: x != 0, channels[idx]))

for i in channels:
    plt.plot(range(0, len(i)), i)

# plt.plot(range(0, len(channels[4])), channels[4])
plt.xlabel('Time (ms)')
plt.ylabel('Amp (mV)')
plt.show()
