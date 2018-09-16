'''
choose what to do
'''
from simulator import *

def main():
    print(choose1(Parameter3))

ans_list = [0] * 4

min_time = 128001
seq_list = [0] * 4

def choose1(parameter):
    global ans_list
    global min_time
    global seq_list

    MAX_TIME = 28801

    s = Simulator(parameter,verbose=False)

    while s.time < 28800:
        ss = s.copy()
        ss.verbose = False
        min_time = 128801
        seq_list = [0] * 4
        dfs(ss,1)
        Cncno = ans_list[1]

        target_pose = (Cncno - 1) // 2
        s.move2(target_pose)

        s.time = max(s.time, s.Cnc(Cncno).finish_time())
        s.feed(Cncno)
        if s.rgv.has == FINISHED : s.clean()
        print (s)


def dfs(ss,depth):
    global ans_list
    global seq_list
    global min_time
    if depth > 3:
        if ss.time < min_time:
            ans_list = seq_list.copy()
            min_time = ss.time
        return
    for i in range(1,9):
        pos = ss.rgv.position
        target_pose = (i - 1) // 2
        sss = ss.copy()
        sss.move2(target_pose)
        sss.time = max(sss.time, sss.Cnc(i).finish_time())
        sss.feed(i)
        if sss.rgv.has == FINISHED : sss.clean()
        seq_list[depth] = i
        dfs(sss,depth + 1)

if __name__ == "__main__":
    main()

