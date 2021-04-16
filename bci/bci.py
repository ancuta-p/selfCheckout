import matplotlib.pyplot as plt


def bci(file):
    ds = []
    for line in open(file, 'r').readlines():
        data = line.strip().split()
        data = [float(val) for val in data if data]
        ds.append(data)

    noChannels = int(ds[0][0])
    noSamples = int(ds[1][0])
    noTrials = int(ds[2][0])
    freq = int(ds[4][0])
    ds = ds[5:]
    print(f'dataset = \'{file}\', channels = {noChannels}, samples = {noSamples}, trials = {noTrials}, freq = {freq}')

    # baseline correction
    for data in ds:
        if data:
            avg = sum(data[:26]) / 26
            for i in range(0, 26):
                data[i] -= avg

    time = [i / freq for i in range(noSamples)]
    trial = []
    for k in range(0, noChannels):
        channel = []
        for i in range(0, noSamples):
            samples = []
            for j in range(0, noTrials):
                # print(ds[k::noChannels + 1][j])
                # print(len(ds[k::noChannels + 1][j]))
                samples.append(ds[k::noChannels + 1][j][i])
            # print(channel)
            avg = sum(samples) / noTrials
            channel.append(avg)
        trial.append(channel)
    return trial, time, noChannels


if __name__ == '__main__':
    trialT, timeT, noTChannels = bci('ep8chTargets.dat')
    trialNonT, timeNonT, noNonTChannels = bci('ep8chNONTargets.dat')
    # plot
    channels = min(noTChannels, noNonTChannels)
    time = min(timeT, timeNonT)
    for i in range(channels):
        plt.plot(time, trialT[i], 'g')
        plt.plot(time, trialNonT[i], 'b')
        plt.ylim(-10, 10)
        plt.xlabel('time')
        plt.ylabel('values')
        plt.show()
