import numpy as np

channels = []
for i in range(1, 6):
    fid = open(f'S-31/REGTOT11.C{i}', 'rb')
    c = np.fromfile(fid, np.int16)
    channels.append(c)

for i in channels:
    print(i)
