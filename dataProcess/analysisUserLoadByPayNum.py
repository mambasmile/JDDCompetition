#coding=utf-8

"""加入对分期的考虑，计算用户的月借款金额
输出：userMonthLoad.csv
列名：uid, 
      user8MonthLoad(用户8月的借款金额),
      user9MonthLoad(用户9月的借款金额), 
	  user10MonthLoad(用户10月的借款金额), 
	  user11MonthLoad(用户11月的借款金额), 
	  user12MonthLoad(用户12月的借款金额),

"""

import pandas as pd
from datetime import datetime
import json
from fileConfig import fileConfig


"""观察load中每个用户的借款记录条数"""
def observeLoadPerMonth():
    i = 0
    resDict = {}
    with open(fileConfig.CovertedloanFile,'r') as e:
        for line in e:
            if i==0:
                i+=1
                continue
            data = line.strip().split(',')
            if data[0] not in resDict:
                resDict[data[0]] = {}
            month = datetime.strptime(data[1], '%Y-%m-%d %H:%M:%S').month
            if month not in resDict[data[0]]:
                resDict[data[0]][month] = []
            resDict[data[0]][month].append((data[-2],data[-1]))
    with open(unicode('../dataFile/用户每个月的借款记录条数','utf-8'),'w') as e:
        for key in resDict:
            e.write(json.dumps([str(key),resDict[key]])+'\n')


"""给定月份，借款金额以及分期数求用户每个月的借款金额"""
def computeMonthLoad(month,loadMoney,plannum):
    perMoney = loadMoney/plannum
    resDict = {}
    for i in xrange(plannum):
        resDict[i+month] = loadMoney-perMoney*i
    return resDict

"""计算用户每个月的总借款金额"""
def computeSumMonthLoad():
    userIDLs = []
    user8MonthLoad = []   ##8月借款金额
    user9MonthLoad = []   ##9月借款金额
    user10MonthLoad = []  ##10月借款金额
    user11MonthLoad = []  ##11月借款金额
    user12MonthLoad = []  ##12月借款金额

    with open(unicode('../dataFile/用户每个月的借款(借款总金额)', 'utf-8'), 'w') as e:
        with open(unicode('../dataFile/用户每个月的借款记录条数(分期到月)', 'utf-8'), 'r') as e1:
            for line in e1:
                data = json.loads(line)
                userId = data[0]
                if userId == '26308':
                    print data
                userIDLs.append(userId)
                resDict = {}
                for key in data[-1]:
                    count = 0
                    for ls in data[-1][key]:
                        count+=float(ls[0])
                    resDict[key] = count
                for month in ['8','9','10','11','12']:
                    if month not in resDict:
                        resDict[month] = 0
                for key in resDict:
                    if key == '8':
                        user8MonthLoad.append(resDict[key])
                    elif key == '9':
                        user9MonthLoad.append(resDict[key])
                    elif key == '10':
                        user10MonthLoad.append(resDict[key])
                    elif key == '11':
                        user11MonthLoad.append(resDict[key])
                    elif key == '12':
                        user12MonthLoad.append(resDict[key])

                e.write(json.dumps([userId,resDict])+'\n')
    resDF = pd.DataFrame({'uid':userIDLs,
                          'user8MonthLoad':user8MonthLoad,
                          'user9MonthLoad':user9MonthLoad,
                          'user10MonthLoad':user10MonthLoad,
                          'user11MonthLoad':user11MonthLoad,
                          'user12MonthLoad':user12MonthLoad,
                          })
    resDF.to_csv('../corpus/userMonthLoad.csv',index=False)

if __name__ == '__main__':
    observeLoadPerMonth()
    computeUserLoadPerMonth()
    computeSumMonthLoad()