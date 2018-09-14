'''
choose what to do
'''
from simulator import Simulator
from simulator import Parameter1 as Parameter

# status of CNC
IDLE = 0
RUN = 1
RUN1 = 2
RUN2 = 3
BROKEN = 4

# what rgv has
NOTHING = 0
FINISHED = 1
HALF_FINISHED = 2

MAX_TIME = 28801

s = Simulator(Parameter,verbose=False)

while s.time < 28800 :
    pos = s.rgv.position
    cncNo = pos * 2 + 1

    if s.Cnc(cncNo).status == IDLE and s.time + Parameter.rgv[0] < MAX_TIME :
        s.feed(cncNo)
        continue
    if s.Cnc(cncNo+1).status == IDLE and s.time + Parameter.rgv[1] < MAX_TIME:
        s.feed(cncNo+1)
        continue
    'if the cnc beside the rgv is IDLE, feed it'

    if s.Cnc(cncNo).finish_time() <= s.time and s.time + Parameter.rgv[0] + Parameter.clean < MAX_TIME:
        s.feed(cncNo)
        s.clean()
        continue
    if s.Cnc(cncNo+1).finish_time() <= s.time and s.time + Parameter.rgv[1] + Parameter.clean < MAX_TIME:
        s.feed(cncNo+1)
        s.clean()
        continue
    'if the cnc beside the rgv is done, feed it and clean'

    time_list = []
    for i in range(1,9):
        cncpos = (i-1) // 2
        dis = abs(pos-cncpos)
        walk_finish = Parameter.mov[dis] + s.time
        time_list.append(max(walk_finish,s.Cnc(i).finish_time()))
    min_time = MAX_TIME
    for i in range(8):
        if time_list[i] < min_time:
            min_time = time_list[i]
            mini = i + 1
    target_pose=(mini-1)//2
    if(target_pose == pos): s.wait(1)
    else: s.move2(target_pose)

print(s)