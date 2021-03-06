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
        [0, 0, 0, 0, 0, 1, 1, 0, 2, 1, 0, 1, 4, 6, 4, 10, 17, 16, 22, 33, 43, 57, 55, 76, 116, 135, 180, 201, 263, 321, 413, 521, 676, 818, 1003, 1171, 1396, 1714, 1982, 2352, 2728, 3142, 3537, 3676, 3820, 4160, 3397, 3620, 3020, 1744, 2330, 167, 1048, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 4, 2, 7, 10, 9, 7, 28, 26, 39, 43, 53, 62, 99, 88, 124, 185, 193, 233, 317, 392, 487, 616, 773, 939, 1166, 1447, 1655, 2036, 2334, 2837, 3013, 3612, 3706, 3804, 4229, 3328, 3648, 2968, 1722, 2498, 156, 1102, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 4, 2, 10, 8, 10, 25, 18, 25, 36, 53, 59, 65, 92, 111, 130, 164, 203, 264, 333, 389, 505, 648, 766, 970, 1163, 1500, 1648, 1957, 2375, 2744, 2980, 3587, 3651, 3836, 4186, 3448, 3535, 3011, 1713, 2534, 156, 1077, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 3, 0, 0, 0, 4, 0, 2, 8, 11, 12, 18, 32, 36, 36, 56, 56, 73, 92, 173, 180, 192, 244, 285, 424, 510, 651, 758, 966, 1222, 1397, 1664, 1992, 2432, 2845, 3137, 3541, 3739, 3817, 4110, 3408, 3611, 3015, 1653, 2388, 150, 1056, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    c = [0 for i in range(start, end)]
    for i in range(4):
        for j in range(end-start):
            c[j] += cs[i][j]
    plot(c, start, end)

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
