# since starting a new engine really consume time, it's recommended to connect to a shared MATLAB session
# to shared the session in MATLAB GUI, just call this in MATLAB ------------------  `matlab.engine.shareEngine`
# I found that if there's no shared sessions, it will automatically create one and then delete, which really consume time (about 5s)

import os, math, random, time
import matplotlib.pyplot as plt

def main(point = 400, testfor = 1000000, err_rate = 0.01, plotfist = 30):
    cntcnt = [0 for i in range(point)]
    t = time.time()
    for i in range(testfor):
        if time.time() - t > 1:
            print(i)
            t = time.time()
        cnt = 0
        for j in range(point):
            if random.random() < err_rate:
                cnt += 1
        cntcnt[cnt] += 1
    plt.plot([i/point for i in range(plotfist)], cntcnt[:plotfist])
    plt.show()

if __name__ == '__main__':
    main()
