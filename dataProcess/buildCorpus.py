#coding=utf-8

from datetime import datetime
import pandas as pd
import json
from fileConfig import fileConfig
from convertMoney import convertMoney

"""分析用户每个月的消费情况(不考虑分期数)"""
def buildUserMonth_Load(trainCorpus=True):
    userDF = pd.read_csv(fileConfig.userFile)
    userIDLs = userDF.uid.tolist()

    with open(unicode('../dataFile/用户每个月的借款(借款总金额)', 'utf-8'), 'r') as e:
        firstMonth = []
        secondMonth = []
        thirdMonth = []
        userLs = []
        if trainCorpus:
            monthLs = ['8', '9', '10']
        else:
            monthLs = ['9', '10', '11']
        for line in e:
            data = json.loads(line)
            userLs.append(int(data[0]))
            userIDLs.remove(int(data[0]))
            if monthLs[0] in data[-1]:
                firstMonth.append(float(data[-1][monthLs[0]]))
            else:
                firstMonth.append(0)
            if monthLs[1] in data[-1]:
                secondMonth.append(float(data[-1][monthLs[1]]))
            else:
                secondMonth.append(0)
            if monthLs[2] in data[-1]:
                thirdMonth.append(float(data[-1][monthLs[2]]))
            else:
                thirdMonth.append(0)
        for id in userIDLs:
            userLs.append(id)
            firstMonth.append(0)
            secondMonth.append(0)
            thirdMonth.append(0)
    resDF = pd.DataFrame({'uid': userLs,
                          'firstMonthLoad': firstMonth,
                          'secondMonthLoad': secondMonth,
                          'thirdMonthLoad': thirdMonth})
    if trainCorpus:
        resDF.to_csv('../corpus/train_userMonthLoad.csv', index=False)
    else:
        resDF.to_csv('../corpus/test_userMonthLoad.csv', index=False)


"""分析用户每个月的消费情况(考虑分期数)"""
def buildUserMonthLoad(trainCorpus=True):
    userDF = pd.read_csv(fileConfig.userFile)
    userIDLs = userDF.uid.tolist()

    with open(unicode('../dataFile/用户每个月的借款(借款总金额)', 'utf-8'), 'r') as e:
        firstMonth = []
        secondMonth = []
        thirdMonth = []
        userLs = []
        if trainCorpus:
            monthLs = ['8', '9', '10']
        else:
            monthLs = ['9', '10', '11']
        for line in e:
            data = json.loads(line)
            userLs.append(int(data[0]))
            userIDLs.remove(int(data[0]))
            if monthLs[0] in data[-1]:
                firstMonth.append(float(data[-1][monthLs[0]]))
            else:
                firstMonth.append(0)
            if monthLs[1] in data[-1]:
                secondMonth.append(float(data[-1][monthLs[1]]))
            else:
                secondMonth.append(0)
            if monthLs[2] in data[-1]:
                thirdMonth.append(float(data[-1][monthLs[2]]))
            else:
                thirdMonth.append(0)
        for id in userIDLs:
            userLs.append(id)
            firstMonth.append(0)
            secondMonth.append(0)
            thirdMonth.append(0)
    resDF = pd.DataFrame({'uid':userLs,
                          'firstMonthLoad':firstMonth,
                          'secondMonthLoad':secondMonth,
                          'thirdMonthLoad':thirdMonth})
    if trainCorpus:
        resDF.to_csv('../corpus/train_userMonthLoad.csv',index=False)
    else:
        resDF.to_csv('../corpus/test_userMonthLoad.csv',index=False)

"""建立用户csv"""
def buildUser():
    userDF = pd.read_csv(unicode('../dataFile/t_user提取用户的激活时间.csv','utf-8'))
    sexMapping = {01:0,02:1}
    userDF.sex = userDF.sex.map(sexMapping)
    userDF.to_csv('../corpus/user.csv',index=False)

"""建立loan_sum.csv"""
def buildLoanSum():
    loan_sum = pd.read_csv(fileConfig.CovertedloanSumFile)
    uidLs = loan_sum.uid.tolist()
    loanSumLs = loan_sum.loan_sum.tolist()
    userDF = pd.read_csv(fileConfig.userFile)
    allUidLs = userDF.uid.tolist()
    for id in allUidLs:
        if id not in uidLs:
            uidLs.append(id)
            loanSumLs.append(0.0)
    resDF = pd.DataFrame({'uid':uidLs,
                          'loan_sum':loanSumLs})
    resDF.to_csv('../corpus/loan_sum.csv',index=False)

"""分析用户的order文件，将用户每个月的消费记录抽取出来"""
def analysisOrder(trainCorpus=True):
    basicFile = 'secondCorpus'
    userDF = pd.read_csv(fileConfig.userFile)
    userIDLs = userDF.uid.tolist()
    i = 0
    resDict = {}
    with open(fileConfig.CovertedorderFile, 'r') as e:
        """新产生的行"""
        firstMonthNum = [] ##8月份的订单数目
        secondMonthNum = [] ##9月份的订单数目
        thirdMonthNum = [] ##10月份的订单数目

        uid = []
        cate_idNum = [] ##订单种类数目
        oldPrice = [] ##8，9，10月的订单总价
        newPrice = [] ##8，9，10月的实际消费额
        if trainCorpus:
            monthLs = [8,9,10]
        else:
            monthLs = [9,10,11]
        for line in e:
            if i == 0:
                i += 1
                continue
            data = line.strip().split(',')
            i+=1
            try:
                month = datetime.strptime(data[1], '%Y-%m-%d').month
            except ValueError as e:
                print i,data,e

            if (month > monthLs[-1]) or (month < monthLs[0]):
                continue
            if data[0] not in resDict:
                resDict[data[0]] = {'time':[],'oldPrice':0.0,'newPrice':0.0,'cate_idLs':[]}
            resDict[data[0]]['time'].append(month)
            # print data[0],data[2]
            try:
                price = float(data[2])
            except ValueError as e:
                print data
            discount = float(data[-1])
            resDict[data[0]]['oldPrice'] += price
            resDict[data[0]]['newPrice'] += (price - discount)
            resDict[data[0]]['cate_idLs'].append(data[-2])

    for key in resDict:
        try:
            userIDLs.remove(int(key))
        except ValueError as e:
            print key,resDict[key]
        uid.append(key)
        fisrtNum,secondNum,thirdNum,fourthNum = computeMonthNum(monthLs,resDict[key]['time'])
        firstMonthNum.append(fisrtNum)
        secondMonthNum.append(secondNum)
        thirdMonthNum.append(thirdNum)

        oldPrice.append(resDict[key]['oldPrice'])
        newPrice.append(resDict[key]['newPrice'])
        cate_idNum.append(resDict[key]['cate_idLs'].__len__())
    for id in userIDLs:
        uid.append(str(id))
        firstMonthNum.append(0)
        secondMonthNum.append(0)
        thirdMonthNum.append(0)
        oldPrice.append(0.0)
        newPrice.append(0.0)
        cate_idNum.append(0)
    resDF = pd.DataFrame({'uid':uid,
                          'firstMonthNum':firstMonthNum,
                          'secondMonthNum':secondMonthNum,
                          'thirdMonthNum':thirdMonthNum,
                          'oldPrice':oldPrice,
                          'newPrice':newPrice,
                          'cate_idNum':cate_idNum,
                          })
    if trainCorpus:
        resDF.to_csv('../'+basicFile+'/train_order.csv',index=False)
    else:
        resDF.to_csv('../'+basicFile+'/test_order.csv', index=False)

"""工具包"""
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
    # buildUser()
    # buildLoanSum()
    # analysisOrder(trainCorpus=False)
    # buildUserMonthLoad(trainCorpus=False)
    # clickCorpus(trainCorpus=True)
    # mergeDF()
    fillUserLoadSum()