#coding=utf-8
from __init__ import *

"""
    训练集：8月，9月，10月点击次数；三个月点击总次数，三个月点击页面种类次数
    测试集：9月，10月，11月点击次数；三个月点击总次数，三个月点击页面种类次数
     
    输入：trainCorpus：True生成训练集 |trainCorpus：Flase生成测试集
    输出：train_click.csv |test_click.csv
"""

def clickCorpus(trainCorpus):

    userDF = pd.read_csv(fileConfig.userFile)
    userIDLs = userDF.uid.tolist()
    i = 0
    resDict = {}
    with open(fileConfig.clickFile, 'r') as e:
        """新产生的行"""
        firstMonthNum = []  ##8月份的点击次数
        secondMonthNum = []  ##9月份的点击次数
        thirdMonthNum = []  ##10月份的点击次数

        uid = []
        pidCount = []  ##点击页面的总次数
        pidNum = []  ##页面种类数目

        if trainCorpus:
            monthLs = [8, 9, 10]
        else:
            monthLs = [9, 10, 11]
        for line in e:
            if i == 0:
                i += 1
                continue
            data = line.strip().split(',')
            i += 1
            try:
                month = datetime.strptime(data[1], '%Y-%m-%d %H:%M:%S').month
            except ValueError as e:
                print i, data, e

            if (month > monthLs[-1]) or (month < monthLs[0]):
                continue
            if data[0] not in resDict:
                resDict[data[0]] = {'time': [],'pidLs': []}
            resDict[data[0]]['time'].append(month)
            # print data[0],data[2]
            try:
                price = float(data[2])
            except ValueError as e:
                print data
            pLoc = data[-2]+'_'+data[-1]
            resDict[data[0]]['pidLs'].append(pLoc)

    for key in resDict:
        try:
            userIDLs.remove(int(key))
        except ValueError as e:
            print key, resDict[key]
        uid.append(key)
        fisrtNum, secondNum, thirdNum, fourthNum = computeMonthNum(monthLs, resDict[key]['time'])
        firstMonthNum.append(fisrtNum)
        secondMonthNum.append(secondNum)
        thirdMonthNum.append(thirdNum)

        pidCount.append(resDict[key]['pidLs'].__len__())
        pidNum.append(set(resDict[key]['pidLs']).__len__())

    for id in userIDLs:
        uid.append(str(id))
        firstMonthNum.append(0)
        secondMonthNum.append(0)
        thirdMonthNum.append(0)
        pidCount.append(0)
        pidNum.append(0)

    resDF = pd.DataFrame({'uid': uid,
                          'firstMonthNum': firstMonthNum,
                          'secondMonthNum': secondMonthNum,
                          'thirdMonthNum': thirdMonthNum,
                          'pidCount': pidCount,
                          'pidNum': pidNum,
                          })
    if trainCorpus:
        resDF.to_csv('../corpus/train_click.csv', index=False)
    else:
        resDF.to_csv('../corpus/test_click.csv', index=False)

"""
将loan_sum.csv文件当中没出现用户当月消费金额填充为0
输出：value.csv

"""
def fillUserLoadSum():
    loadSum = pd.read_csv(fileConfig.CovertedloanSumFile)
    userDF = pd.read_csv(fileConfig.userFile)
    resDF = pd.merge(userDF[['uid']],loadSum[['uid','loan_sum']],how='left')
    resDF = resDF.fillna(0.0)
    resDF.to_csv('../corpus/value.csv',index=False)



"""统计每个月出现的次数"""
def computeMonthNum(monthLs,time):
    monthLs1 = 0
    monthLs2 = 0
    monthLs3 = 0
    monthLs4 = 0
    for val in time:
        for i in xrange(monthLs.__len__()):
            if int(val) == monthLs[i]:
                if i == 0:
                    monthLs1 +=1
                elif i == 1:
                    monthLs2 +=1
                elif i ==2:
                    monthLs3 +=1
                else:
                    monthLs4 +=1
    return monthLs1,monthLs2,monthLs3,monthLs4
