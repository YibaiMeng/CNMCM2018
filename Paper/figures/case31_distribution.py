import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import choose31
from simulator import *
import matplotlib.pyplot as plt

def main():
    start = 330
    end = 420

    # c = run(start, end)

    # these are multi-process result, paste manually to here
    cs = [
        [],
        [],
        [],
        []
    ]
    c = [0 for i in range(start, end)]
    for i in range(4):
        for j in range(end-start):
            c[j] += cs[i][j]
    plot(c)

def plot(c, start, end):
    plt.plot([i for i in range(start, end)], c)
    plt.show()

def run(start, end):
    c = [0 for i in range(end-start)]
    t = time.time()
    for i in range(50000):
        if time.time() - t > 1:
            print(i)
            t = time.time()
        s = choose31.once(Parameter1)
        if s.count >= end: print("greater:", s.count)
        elif s.count < start: print("less:", s.count)
        else: c[s.count - start] += 1
    print(c)

if __name__ == '__main__':
    main()
