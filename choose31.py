'''
choose what to do
'''
from simulator import *

def main():
    cnt = 0
    for i in range(20):
        s = choose1(Parameter1)
        print (s)
        cnt += s.count
    print("The average count is ",cnt / 20)

def once(parameter):
    return choose1(parameter)

def choose1(parameter):

    MAX_TIME = 28801

    s = Simulator(parameter,verbose=False,err_rate=0.01)

    while s.time < 28800 :
        pos = s.rgv.position
        cncNo = pos * 2 + 1

        if s.Cnc(cncNo).status == IDLE and s.time + parameter.rgv[0] < MAX_TIME :
            s.feed(cncNo)
            continue
        if s.Cnc(cncNo+1).status == IDLE and s.time + parameter.rgv[1] < MAX_TIME:
            s.feed(cncNo+1)
            continue
        'if the cnc beside the rgv is IDLE, feed it'

        if s.Cnc(cncNo).finish_time() <= s.time and s.time + parameter.rgv[0] < MAX_TIME:
            s.feed(cncNo)
            if s.rgv.has == FINISHED:
                if s.time + parameter.clean < MAX_TIME:
                    s.clean()
                else : break
            continue
        if s.Cnc(cncNo+1).finish_time() <= s.time and s.time + parameter.rgv[1] < MAX_TIME:
            s.feed(cncNo+1)
            if s.rgv.has == FINISHED:
                if s.time + parameter.clean < MAX_TIME:
                    s.clean()
                else : break
            continue
        'if the cnc beside the rgv is done, feed it and clean'

        time_list = []
        for i in range(1,9):
            cncpos = (i-1) // 2
            dis = abs(pos-cncpos)
            walk_finish = parameter.mov[dis] + s.time
            time_list.append(max(walk_finish,s.Cnc(i).finish_time()))
        min_time = MAX_TIME
        for i in range(8):
            if time_list[i] < min_time:
                min_time = time_list[i]
                mini = i + 1
        target_pose=(mini-1)//2
        if(target_pose == pos): s.wait(1)
        else: s.move2(target_pose)

    return s

if __name__ == "__main__":
    main()

