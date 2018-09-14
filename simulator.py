"""
simulate the behavior of every CNC and RGV
providing API with whether an action satisfy the constrains
"""

def main():
    s = Simulator(Parameter1, verbose=True)
    s.move2(1)
    s.move2(3)
    s.feed(8)
    s.wait(1000)
    s.feed(8)
    s.clean()


    print(s)

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

class Parameter2:
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

    def move2(self, position):  # position in [0,1,2,3]
        lastpos = self.rgv.position
        distance = abs(lastpos - position)
        deltaT = self.parameter.mov[distance]
        self.rgv.position = position
        if self.verbose: print("%d+%d: rgv move from %d to %d" % (self.time, deltaT, lastpos, position))
        self.time += deltaT  # check by default, if out of range, raise exception
    
    def feed(self, idx):
        pos = (idx-1) // 2
        if self.rgv.position != pos: raise Exception("not in this position")
        cnc = self.cnc[idx-1]
        if cnc.finish_time() > self.time : raise Exception("work not finished")
        got = NOTHING if cnc.status == IDLE else (FINISHED if cnc.status != "RUN1" else HALF_FINISHED)
        gotstr = {NOTHING: "NOTHING", FINISHED: "FINISHED", HALF_FINISHED: "HALF_FINISHED"}[got]
        if self.rgv.has != NOTHING and not (self.rgv.has == HALF_FINISHED and cnc.possible_run == RUN2): raise Exception("rgv has something to clean or cannot do it")
        self.rgv.has = got
        cnc.status = cnc.possible_run  # change the state to run
        deltaT = self.parameter.rgv[(idx-1) % 2]
        if self.verbose: print("%d+%d: feed %d with %s, and got %s" % (self.time, deltaT, idx, "NEW" if self.rgv.has == NOTHING else "HALF_FINSHED", gotstr))
        self.time += deltaT
        cnc.start = self.time
    
    def clean(self):
        if self.rgv.has != FINISHED: raise Exception("nothing to clean or half-finished cannot be cleaned")
        deltaT = self.parameter.clean
        if self.verbose: print("%d+%d: clean finised work" % (self.time, deltaT))
        self.time += deltaT
    
    def wait(self, deltaT):
        if self.verbose: print("%d+%d: waiting" % (self.time, deltaT))
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
        return s

if __name__ == '__main__':
    main()
