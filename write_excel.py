import xlsxwriter

from simulator import *
import choose1
import choose2

def main():
    workbook = xlsxwriter.Workbook('Problem/Case_1_result.xlsx')
    for r, parameter in enumerate((Parameter1, Parameter2, Parameter3)):
        worksheet = workbook.add_worksheet("第%d组" % (r+1))
        worksheet.set_column('A:D',20)
        worksheet.write('A1', '加工物料序号')
        worksheet.write('B1', '加工CNC编号')
        worksheet.write('C1', '上料开始时间')
        worksheet.write('D1', '下料开始时间')
        s = choose1.main(parameter)
        for r, obj in enumerate(s.finished_objs()):
            worksheet.write('A%d' % (r+2), obj.num)
            worksheet.write('B%d' % (r+2), obj.cnc)
            worksheet.write('C%d' % (r+2), obj.start)
            worksheet.write('D%d' % (r+2), obj.end)
    workbook.close()

    workbook = xlsxwriter.Workbook('Problem/Case_2_result.xlsx')
    for r, parameter in enumerate((Parameter1, Parameter2, Parameter3)):
        worksheet = workbook.add_worksheet("第%d组" % (r+1))
        worksheet.set_column('A:D',20)
        worksheet.write('A1', '加工物料序号')
        worksheet.write('B1', '工序1的CNC编号')
        worksheet.write('C1', '上料开始时间')
        worksheet.write('D1', '下料开始时间')
        worksheet.write('E1', '工序2的CNC编号')
        worksheet.write('F1', '上料开始时间')
        worksheet.write('G1', '下料开始时间')
        s = choose2.main(parameter)
        for r, obj in enumerate(s.finished_objs()):
            worksheet.write('A%d' % (r+2), obj.num)
            worksheet.write('B%d' % (r+2), obj.cnc)
            worksheet.write('C%d' % (r+2), obj.start)
            worksheet.write('D%d' % (r+2), obj.end)
            worksheet.write('E%d' % (r+2), obj.cnc2)
            worksheet.write('F%d' % (r+2), obj.start2)
            worksheet.write('G%d' % (r+2), obj.end2)
    workbook.close()

if __name__ == "__main__":
    main()
