'''
choose what to do
'''
from simulator import *

def main():
    count = 0
    max_count = 0
    for i1 in range(1,3):
        for i2 in range(1,3):
            for i3 in range(1,3):
                for i4 in range(1,3):
                    for i5 in range(1,3):
                        for i6 in range(1,3):
                            for i7 in range(1,3):
                                for i8 in range(1,3):
                                    count += 1
                                    if count == 1 or count == 256: continue
                                    Run1 = []
                                    Run2 = []
                                    Run1.append(1) if i1 == 1 else Run2.append(1)
                                    Run1.append(2) if i2 == 1 else Run2.append(2)
                                    Run1.append(3) if i3 == 1 else Run2.append(3)
                                    Run1.append(4) if i4 == 1 else Run2.append(4)
                                    Run1.append(5) if i5 == 1 else Run2.append(5)
                                    Run1.append(6) if i6 == 1 else Run2.append(6)
                                    Run1.append(7) if i7 == 1 else Run2.append(7)
                                    Run1.append(8) if i8 == 1 else Run2.append(8)
                                    s = choose2(Parameter3,Run1,Run2)
                                    if s.count > max_count:
                                        max_count = s.count
                                        max_run1 = Run1
                                        max_run2 = Run2
    print(max_run1,max_run2)
    print(choose2(Parameter3,max_run1,max_run2))


def choose2(parameter,Run1,Run2):

    MAX_TIME = 28801

    s = Simulator(parameter,Run1,Run2,verbose=False)

    while s.time < 28800 :
        pos = s.rgv.position
        cncNo = pos * 2 + 1

        time_list = []
        for i in range(1,9):
            cncpos = (i-1) // 2
            dis = abs(pos - cncpos)
            walk_finish = parameter.mov[dis]+s.time
            if(s.Cnc(i).status == IDLE):
                if(s.Cnc(i).possible_run == RUN1): time_list.append(walk_finish)
                else : time_list.append(MAX_TIME)
            else: time_list.append(max(walk_finish,s.Cnc(i).finish_time()))

        min_time = MAX_TIME + 1

        for i in range(8):
            if time_list[i] < min_time:
                min_time = time_list[i]
                mini = i + 1

        if min_time >= MAX_TIME: break
        target_pose = (mini - 1) // 2

        if target_pose != pos : s.move2(target_pose)
        'if s.time < min_time : s.time = min_time'
        if s.time < s.Cnc(mini).finish_time(): s.time = s.Cnc(mini).finish_time()


        if s.Cnc(mini).possible_run == RUN1 :
            if s.time + parameter.rgv[(mini+1)%2] >= MAX_TIME : break
            s.feed(mini)
            if(s.rgv.has == HALF_FINISHED):
                pos = s.rgv.position
                time_list2 = []
                for i in range(1,9):
                    if s.Cnc(i).possible_run == RUN2 :
                        cncpos = (i - 1) // 2
                        dis = abs(pos - cncpos)
                        walk_finish = parameter.mov[dis]+s.time
                        if(s.Cnc(i).status == IDLE):time_list2.append(walk_finish)
                        else: time_list2.append(max(walk_finish,s.Cnc(i).finish_time()))
                    else:
                        time_list2.append(MAX_TIME)
                min_time2 = MAX_TIME + 1
                for i in range(8):
                    if s.Cnc(i+1).possible_run == RUN2 and time_list2[i] < min_time2:
                        min_time2 = time_list2[i]
                        mini2 = i + 1
                if min_time2 >= MAX_TIME: break
                target_pose = (mini2 - 1) // 2
                if target_pose != pos : s.move2(target_pose)
                if s.time < s.Cnc(mini2).finish_time() : s.time = s.Cnc(mini2).finish_time()

                if(s.time + parameter.rgv[(mini2+1)%2] >= MAX_TIME):break
                s.feed(mini2)
                if s.rgv.has == FINISHED :
                    if s.time + parameter.clean < MAX_TIME: s.clean()
                    else : break

        elif s.Cnc(mini).possible_run == RUN2 :
            if s.time + parameter.rgv[(mini+1)%2] >= MAX_TIME: break
            s.feed(mini)
            if s.rgv.has == FINISHED :
                if s.time + parameter.clean < MAX_TIME: s.clean()
                else : break

    return s

if __name__ == "__main__":
    main()