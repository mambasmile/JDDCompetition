#coding=utf-8

from __init__ import *

"""取时间里面的月"""
class convertTime:

    @staticmethod
    def extractMonth(symbol,filepath,outpath):
        i = 0
        with open(outpath,'w') as e:
            with open(filepath,'r') as e1:
                for line in e1:
                    if i == 0:
                        i+=1
                        e.write(line)
                        continue
                    data = line.strip().split(',')
                    if symbol == 1:
                        month = datetime.strptime(data[1],'%Y-%m-%d %H:%M:%S').month
                    elif symbol == 0:
                        month = datetime.strptime(data[1],'%Y-%m-%d').month
                    data[1] = str(month)
                    e.write(",".join(data)+'\n')

if __name__ == '__main__':
    convertTime.extractMonth(1,fileConfig.CovertedloanFile,fileConfig.timeCovertedloanFile)