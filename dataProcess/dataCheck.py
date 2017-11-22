#coding=utf-8

from __init__ import *

"""提取用户的激活时间"""
def extractUserActivateMonth():
    i = 0
    with open(unicode(r'../dataFile/t_user提取用户的激活时间.csv', 'utf-8'),'w') as e1:
        with open(fileConfig.userFile,'r') as e:
            for line in e:
                if i == 0:
                    i+=1
                    e1.write(line)
                    continue
                data = line.strip().split(',')
                month = datetime.strptime(data[-2], '%Y-%m-%d').month
                res = [data[0],data[1],data[2],str(month),data[-1]]
                e1.write(','.join(res)+'\n')


if __name__ == '__main__':

    extractUserActivateMonth()
