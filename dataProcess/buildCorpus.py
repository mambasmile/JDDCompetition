#coding=utf-8

from datetime import datetime
import pandas as pd
import json
from fileConfig import fileConfig
from convertMoney import convertMoney


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

"""得到训练集的value"""
def fillUserLoadSum():
    loadSum = pd.read_csv(fileConfig.CovertedloanSumFile)
    userDF = pd.read_csv(fileConfig.userFile)
    resDF = pd.merge(userDF[['uid']],loadSum[['uid','loan_sum']],how='left')
    resDF = resDF.fillna(0.0)
    resDF.to_csv('../corpus/value.csv',index=False)

"""合并数据集"""
def mergeDF():
    convertDFMoney = convertMoney()

    basicFile = 'secondCorpus'
    userDF = pd.read_csv(unicode(r'../dataFile/t_user提取用户的激活时间.csv','utf-8'))
    trainOrder = pd.read_csv(unicode(r'../'+basicFile+'/train_order.csv','utf-8'))
    testOrder = pd.read_csv(unicode(r'../'+basicFile+'/test_order.csv','utf-8'))
    trainClick = pd.read_csv(unicode(r'../corpus/train_click.csv','utf-8'))
    testClick = pd.read_csv(unicode(r'../corpus/test_click.csv','utf-8'))

    convertuserDF = convertDFMoney.convertDF(userDF,['limit'])
    # convertTrainOrder = convertDFMoney.convertDF(trainOrder,['newPrice','oldPrice'])
    # convertTestOrder = convertDFMoney.convertDF(testOrder,['newPrice','oldPrice'])

    trainUserMonthLoad = pd.read_csv('../'+basicFile+'/train_userMonthLoad.csv')
    testUserMonthLoad = pd.read_csv('../'+basicFile+'/test_userMonthLoad.csv')

    trainDF = pd.merge(convertuserDF,trainOrder,on='uid')
    trainDF = pd.merge(trainDF,trainClick,on='uid')
    trainDF = pd.merge(trainDF,trainUserMonthLoad,on='uid')

    testDF = pd.merge(convertuserDF,testOrder,on='uid')
    testDF = pd.merge(testDF,testClick,on='uid')
    testDF = pd.merge(testDF,testUserMonthLoad,on='uid')

    trainDF.to_csv('../'+basicFile+'/train.csv',index=False)
    testDF.to_csv('../'+basicFile+'/test.csv',index=False)

if __name__ == '__main__':

    # clickCorpus(trainCorpus=True)
    # mergeDF()
    fillUserLoadSum()