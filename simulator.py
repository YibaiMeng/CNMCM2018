"""
simulate the behavior of every CNC and RGV
providing API with whether an action satisfy the constrains
"""
import copy, os, time

def main():
    if False:
        print("demo for question 1")
        s = Simulator(Parameter1, verbose=True)
        s.move2(1)
        s.move2(3)
        s.feed(8)
        s.wait(1000)
        s.feed(8)
        s.clean()
        print(s)

    if True:
        print("demo for question 2")
        s = Simulator(Parameter1, run1=[1,2,3], run2=[4,5,6,7,8], verbose=True)
        a = s.copy()
        s.move2(1)
        s.feed(3)
        s.wait(1000)
        s.feed(3)
        s.wait(1000)
        s.feed(4)
        s.wait(1000)
        s.feed(4)
        s.clean()
        print(s)
        print(s.log)
        print(a)
        s.save("tmp_ques2.txt")

'''
<<<<<<< HEAD

=======
        
>>>>>>> aa15f8a4eeb9d6123a749e9b0663e242374f8f1d
'''



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

class Parameter1:
    mov = [0, 20, 33, 46]
    run = [560, 400, 378]
    rgv = [28, 31]
    clean = 25

class Parameter2:
    mov = [0, 23, 41, 59]
    run = [580, 280, 500]
    rgv = [30, 35]
    clean = 30

class Parameter3:
    mov = [0, 18, 32, 46]
    run = [545, 455, 182]
    rgv = [27, 32]
    clean = 25

class CNC:
    def __init__(self, possible_run, parameter):  # possible_run is in [RUN, RUN1, RUN2]
        self.status = IDLE
        self.start = -1
        self.parameter = parameter
        self.possible_run = possible_run

    def finish_time(self):
        if self.status == IDLE: return -1
        if self.status == RUN: return self.start + self.parameter.run[0]
        if self.status == RUN1: return self.start + self.parameter.run[1]
        if self.status == RUN2: return self.start + self.parameter.run[2]
        else: raise Exception("not implemented")

class RGV:
    def __init__(self, parameter):
        self.parameter = parameter
        self.position = 0
        self.has = NOTHING

class Simulator:
    def __init__(self, parameter, run1=[], run2=[], err_rate=0, verbose=False):
        self.cnc = [CNC(RUN, parameter) for i in range(8)]
        for idx in run1: self.cnc[idx-1].possible_run = RUN1
        for idx in run2: self.cnc[idx-1].possible_run = RUN2
        self.rgv = RGV(parameter)
        self.time = 0
        self.parameter = parameter
        self.err_rate = err_rate
        self.verbose = verbose
        self.count = 0
        self.log = []  # record the verbose output

    def move2(self, position):  # position in [0,1,2,3]
        lastpos = self.rgv.position
        distance = abs(lastpos - position)
        deltaT = self.parameter.mov[distance]
        self.rgv.position = position
        self.log.append("%d+%d: rgv move from %d to %d" % (self.time, deltaT, lastpos, position))
        if self.verbose: print(self.log[-1])
        self.time += deltaT  # check by default, if out of range, raise exception

    def feed(self, idx):
        pos = (idx-1) // 2
        if self.rgv.position != pos: raise Exception("not in this position")
        cnc = self.cnc[idx-1]
        if cnc.finish_time() > self.time : raise Exception("work not finished")
        got = NOTHING if cnc.status == IDLE else (HALF_FINISHED if cnc.status == RUN1 else FINISHED)
        gotstr = {NOTHING: "NOTHING", FINISHED: "FINISHED", HALF_FINISHED: "HALF_FINISHED"}[got]
        if self.rgv.has != NOTHING and not (self.rgv.has == HALF_FINISHED and cnc.possible_run == RUN2): raise Exception("rgv has something to clean or cannot do it")
        if cnc.possible_run == RUN2 and self.rgv.has != HALF_FINISHED: cnc.status = IDLE  # if not has a HALF_FINISHED, just get the FINISHED one
        else: cnc.status = cnc.possible_run  # change the state to run
        deltaT = self.parameter.rgv[(idx-1) % 2]
        feedwith = "NEW" if self.rgv.has == NOTHING else "HALF_FINSHED"
        if cnc.possible_run == RUN2 and feedwith == "NEW": feedwith = "NOTHING"  # cannot feed NEW to this machine
        self.log.append("%d+%d: feed %d with %s, and got %s" % (self.time, deltaT, idx, feedwith, gotstr))
        if self.verbose: print(self.log[-1])
        self.rgv.has = got
        self.time += deltaT
        cnc.start = self.time

    def clean(self):
        if self.rgv.has != FINISHED: raise Exception("nothing to clean or half-finished cannot be cleaned")
        deltaT = self.parameter.clean
        self.log.append("%d+%d: clean finised work" % (self.time, deltaT))
        if self.verbose: print(self.log[-1])
        self.rgv.has = NOTHING
        self.time += deltaT
        self.count += 1

    def wait(self, deltaT):
        self.log.append("%d+%d: waiting" % (self.time, deltaT))
        if self.verbose: print(self.log[-1])
        self.time += deltaT

    def __str__(self):
        s = ""
        s += "now time is %d\n" % self.time
        def addstatus(idx):
            if self.cnc[idx-1].status == IDLE: st = "o "
            elif self.cnc[idx-1].status == RUN: st = "r "
            elif self.cnc[idx-1].status == RUN1: st = "1 "
            elif self.cnc[idx-1].status == RUN2: st = "2 "
            else: raise Exception("status unknown")
            return st
        for idx in [2, 4, 6, 8]: s += addstatus(idx)  # upper CNCs
        s += "\n"
        s += "".join(["  " for i in range(self.rgv.position)] + ["x\n"])
        for idx in [1, 3, 5, 7]: s += addstatus(idx)  # lower CNCs
        s += "\n"
        s += "finished %d objects\n" % self.count
        return s

    def Cnc(self, idx):
        return self.cnc[idx-1]
    
    def copy(self):
        return copy.deepcopy(self)
    
    def save(self, filename="tmp.txt", folder="Data"):  # save current state to a file, with verbose log behind
        with open(os.path.join(folder, filename), 'w') as f:
            f.write("trace for simulation at %s\n" % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            f.write("\n[now state]\n")
            f.write(str(self))
            f.write("\n[log]\n")
            for s in self.log:
                f.write(s + '\n')

    def copy(self):
        return copy.deepcopy(self)

    def save(self, filename="tmp.txt", folder="Data"):  # save current state to a file, with verbose log behind
        with open(os.path.join(folder, filename), 'w') as f:
            f.write("trace for simulation at %s\n" % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            f.write("\n[now state]\n")
            f.write(str(self))
            f.write("\n[log]\n")
            for s in self.log:
                f.write(s + '\n')

if __name__ == '__main__':
    main()