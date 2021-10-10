import numpy as np
from matplotlib import pyplot as plt, ticker
from scipy import signal

fm = 2000
tick = 1 / fm

legend_labels = ['Electrocardiograma', 'Linea de mercurio', 'Esfigmomanómetro', 'Sonidos Korotkoff', 'Observardor']

channels = []
for i in range(len(legend_labels)):
    fid = open(f'S-31/REGTOT11.C{i + 1}', 'rb')
    # fid = open(f'S-28/REGTOT2.C{i + 1}', 'rb')
    c = np.fromfile(fid, np.int16)

    Wn = .5
    N = 1
    b, a = signal.butter(N, Wn, 'low')
    c = signal.filtfilt(b, a, c)

    channels.append(c)

for idx in range(len(channels)):
    channels[idx] = list(filter(lambda x: x > 1, channels[idx]))

ax = plt.subplot(111)

# finding peaks
observerChannel = np.array(channels[-1])
# observerChannel = np.array(list(filter(lambda x: x > observerChannel.max() / 10, observerChannel)))
# print(observerChannel.min(), observerChannel.max())
inverted_channel = np.negative(observerChannel)
inverted_channel = inverted_channel + abs(inverted_channel.min())
peaks, _ = signal.find_peaks(inverted_channel, distance=10000, height=inverted_channel.max() / 10)
peak_y = list(map(lambda x: channels[-1][x], peaks))

font = {
    'family': 'normal',
    'weight': 'bold',
    'size': 22
}

startTime = 0
endTime = int(len(channels[0]) / fm)
if len(peaks) > 1:
    firstPeakTime = peaks[0] / fm
    lastPeakTime = peaks[-1] / fm
    timeGap = 5
    startTime = int(firstPeakTime - 5)
    endTime = int(lastPeakTime + 5)
    print(f'first peak = {firstPeakTime}')
    print(f'last peak = {lastPeakTime}')

print(f'startTime = {startTime}')
print(f'endTime = {endTime}')

new_x = []
for i in channels:
    step = 1
    offsets = int(fm / step)
    new_x = np.arange(0, len(i), step)
    new_x = new_x[startTime * offsets:endTime * offsets]
    new_y = []
    for j in new_x:
        new_y.append(i[j])
    ax.plot(new_x, new_y)

plt.plot(peaks, peak_y, "x")
legend_labels.append('picos de sonido')


# FuncFormatter can be used as a decorator
@ticker.FuncFormatter
def x_formatter(x, pos):
    return "%d" % (int(x) / fm)


# FuncFormatter can be used as a decorator
@ticker.FuncFormatter
def y_formatter(y, pos):
    return "%.2f" % (int(y) / 1000)


ax.xaxis.set_ticks(np.arange(startTime * fm, len(channels[0][:endTime * fm]), fm * 10))
ax.yaxis.set_major_formatter(y_formatter)
ax.xaxis.set_major_formatter(x_formatter)
# plt.xticks(ticks)

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0.5))

# plt.plot(range(0, len(channels[4])), channels[4])
plt.xlabel('Time (s)')
plt.ylabel('Amp (V)')

fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)
plt.savefig('graph', dpi=400)
plt.show()
