import xlsxwriter

from simulator import *
import choose1
import choose2
import choose31
import choose32

def main():
    # solve problem 1
    if False:
        w = Writer("Case_1_result")
        def func(r, parameter):
            s = choose1.main(parameter)
            w.add_worksheet("第%d组" % (r+1), ['加工物料序号', '加工CNC编号', '上料开始时间', '下料开始时间'])
            for r,obj in enumerate(s.finished_objs()):
                w.write_row(r+2, [obj.num, obj.cnc, obj.start, obj.end])
        w.loop(func)

    # solve problem 2
    if False:
        w = Writer("Case_2_result")
        def func(r, parameter):
            s = choose2.main(parameter)
            w.add_worksheet("第%d组" % (r+1), ['加工物料序号', '工序1的CNC编号', '上料开始时间', '下料开始时间', '工序2的CNC编号', '上料开始时间', '下料开始时间'])
            for r,obj in enumerate(s.finished_objs()):
                w.write_row(r+2, [obj.num, obj.cnc, obj.start, obj.end, obj.cnc2, obj.start2, obj.end2])
        w.loop(func)

    # solve problem 31
    if False:
        w = Writer("Case_31_result")
        def func(grp, parameter):
            s = choose31.main(parameter)
            w.add_worksheet("第%d组" % (grp+1), ['加工物料序号', '加工CNC编号', '上料开始时间', '下料开始时间'])
            for r,obj in enumerate(s.finished_objs()):
                w.write_row(r+2, [obj.num, obj.cnc, obj.start, obj.end])
            w.add_worksheet("第%d组的故障" % (grp+1), ['故障时的物料序号', '故障CNC编号', '故障开始时间', '故障结束时间'])
            for r,err in enumerate(s.errs): w.write_row(r+2, err)
        w.loop(func)
    
    # solve proble 32
    if True:
        w = Writer("Case_32_result")
        def func(grp, parameter):
            s = choose32.main(parameter)
            w.add_worksheet("第%d组" % (grp+1), ['加工物料序号', '工序1的CNC编号', '上料开始时间', '下料开始时间', '工序2的CNC编号', '上料开始时间', '下料开始时间'])
            for r,obj in enumerate(s.finished_objs()):
                w.write_row(r+2, [obj.num, obj.cnc, obj.start, obj.end, obj.cnc2, obj.start2, obj.end2])
            w.add_worksheet("第%d组的故障" % (grp+1), ['故障时的物料序号', '故障CNC编号', '故障开始时间', '故障结束时间'])
            for r,err in enumerate(s.errs): w.write_row(r+2, err)
        w.loop(func)

    # workbook = xlsxwriter.Workbook('Problem/Case_1_result.xlsx')
    # for r, parameter in enumerate((Parameter1, Parameter2, Parameter3)):
    #     worksheet = workbook.add_worksheet("第%d组" % (r+1))
    #     worksheet.set_column('A:D',20)
    #     worksheet.write('A1', '加工物料序号')
    #     worksheet.write('B1', '加工CNC编号')
    #     worksheet.write('C1', '上料开始时间')
    #     worksheet.write('D1', '下料开始时间')
    #     s = choose1.main(parameter)
    #     for r, obj in enumerate(s.finished_objs()):
    #         worksheet.write('A%d' % (r+2), obj.num)
    #         worksheet.write('B%d' % (r+2), obj.cnc)
    #         worksheet.write('C%d' % (r+2), obj.start)
    #         worksheet.write('D%d' % (r+2), obj.end)
    # workbook.close()

    # workbook = xlsxwriter.Workbook('Problem/Case_2_result.xlsx')
    # for r, parameter in enumerate((Parameter1, Parameter2, Parameter3)):
    #     worksheet = workbook.add_worksheet("第%d组" % (r+1))
    #     worksheet.set_column('A:D',20)
    #     worksheet.write('A1', '加工物料序号')
    #     worksheet.write('B1', '工序1的CNC编号')
    #     worksheet.write('C1', '上料开始时间')
    #     worksheet.write('D1', '下料开始时间')
    #     worksheet.write('E1', '工序2的CNC编号')
    #     worksheet.write('F1', '上料开始时间')
    #     worksheet.write('G1', '下料开始时间')
    #     s = choose2.main(parameter)
    #     for r, obj in enumerate(s.finished_objs()):
    #         worksheet.write('A%d' % (r+2), obj.num)
    #         worksheet.write('B%d' % (r+2), obj.cnc)
    #         worksheet.write('C%d' % (r+2), obj.start)
    #         worksheet.write('D%d' % (r+2), obj.end)
    #         worksheet.write('E%d' % (r+2), obj.cnc2)
    #         worksheet.write('F%d' % (r+2), obj.start2)
    #         worksheet.write('G%d' % (r+2), obj.end2)
    # workbook.close()

class Writer:
    def __init__(self, filename):
        self.workbook = xlsxwriter.Workbook('Problem/%s.xlsx' % filename)

    def __del__(self):
        self.workbook.close()
    
    def loop(self, func):
        for r, parameter in enumerate((Parameter1, Parameter2, Parameter3)):
            func(r, parameter)
    
    def add_worksheet(self, name, titles=[]):
        self.worksheet = self.workbook.add_worksheet(name)
        self.worksheet.set_column('A:%s' % chr(ord('A') + len(titles) - 1),20)
        for r, t in enumerate(titles):
            self.worksheet.write('%s1' % chr(ord('A') + r), t)
    
    def write_row(self, row, dat=[]):
        for r, t in enumerate(dat):
            self.worksheet.write('%s%d' % (chr(ord('A') + r), row), t)

if __name__ == "__main__":
    main()
