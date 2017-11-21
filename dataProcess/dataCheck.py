#coding=utf-8

import pandas as pd
from datetime import datetime
import json
from fileConfig import fileConfig

"""分析11月的借款总金额"""
def analysis11MonthLoad():
    userDF = pd.read_csv(fileConfig.userFile)
    userIDLs = userDF.uid.tolist()

    loan_sum = pd.read_csv(fileConfig.loanSumFile)

    userLoanSumLs = []
    userLoanLs = []
    useridLs = []

    fq = {8:3,9:2,10:1}

    # loan_sum = pd.read_csv(unicode(r'D:\京东金融\t_loan_sum.csv','utf-8'))
    loan = pd.read_csv(fileConfig.loanFile)
    print

    for uid in userIDLs:
        timeLs = loan[loan['uid'] == uid].loan_time.tolist()

        if timeLs.__len__() == 0:
            continue
        useridLs.append(uid)
        monthLs = [datetime.strptime(x, '%Y-%m-%d %H:%M:%S').month for x in timeLs] ##借款时间
        loan_money = loan[loan['uid'] == uid].loan_amount.tolist()  ##借款金额
        loan_num = loan[loan['uid'] == uid].plannum.tolist()  ##借款金额

        count = 0
        for i in xrange(monthLs.__len__()):
            if monthLs[i] == 11:
                count +=loan_money[i]
            # elif monthLs[i] in fq:
            #     if loan_num[i] > fq[monthLs[i]]:
            #         count +=loan_money[i]/loan_num[i]

        loan_sumMoney = loan_sum[loan_sum['uid'] == uid]['loan_sum'].values
        if loan_sumMoney.__len__() == 0:
            userLoanSumLs.append(0)
        else:
            userLoanSumLs.append(loan_sumMoney[0])
        userLoanLs.append(count)

    ###记录用户11月借款总金额和11月的借款记录
    resDict = pd.DataFrame({'uid':useridLs,'loan11':userLoanSumLs,'loanSum':userLoanLs})
    resDict.to_csv('../dataFile/load_loadSum.csv',index=False)

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


"""提取用户的激活时间"""
def extractUserActivateMonth():
    i = 0
    with open(unicode(r'../dataFile/t_user提取用户的激活时间.csv', 'utf-8'),'w') as e1:
        with open(fileConfig.userFile,'r') as e:
            for line in e:
                if i == 0:
                    i+=1
                    continue
                data = line.strip().split(',')
                month = datetime.strptime(data[-2], '%Y-%m-%d').month
                res = [data[0],data[1],data[2],str(month),data[-1]]
                e1.write(','.join(res)+'\n')

"""寻找在8月份以后激活的用户"""
def findUser():
    i = 0
    resDict = {}
    with open(unicode(r'../dataFile/t_user提取用户的激活时间.csv', 'utf-8'), 'r') as e1:
        for line in e1:
            if i == 0:
                i+=1
                continue
            data = line.strip().split(',')
            if int(data[-2]) >=8:
                resDict[data[0]] = [data[-2],data[-1]]
    print resDict.__len__()

"""根据分期数求用户每个月的借款金额"""
def computeUserLoadPerMonth():
    with open(unicode('../dataFile/用户每个月的借款记录条数(分期到月)', 'utf-8'), 'w') as e1:
        with open(unicode('../dataFile/用户每个月的借款记录条数', 'utf-8'), 'r') as e:
            for line in e:
                resLs=[]
                resDict = {}
                data = json.loads(line)
                resLs.append(data[0])
                monthLs = ['8','9','10','11']
                for monthkey in monthLs:
                    perLoad = 0.0  ##每个月的借款
                    if monthkey in data[-1]:
                        for ls in data[-1][monthkey]:
                            if int(ls[-1]) == 1:
                                if monthkey not in resDict:
                                    resDict[monthkey] = []
                                resDict[monthkey].append(ls)
                            else:
                                money = float(ls[0])
                                payNum = int(ls[-1])
                                tmpDict = computeMonthLoad(int(monthkey),money,payNum)
                                for key in tmpDict:
                                    strKey = str(key)
                                    if strKey not in resDict:
                                        resDict[strKey] = []
                                    resDict[strKey].append([tmpDict[key],1])
                resLs.append(resDict)
                e1.write(json.dumps(resLs)+'\n')

"""给定月份，借款金额以及分期数求用户每个月的借款金额"""
def computeMonthLoad(month,loadMoney,plannum):
    perMoney = loadMoney/plannum
    resDict = {}
    for i in xrange(plannum):
        resDict[i+month] = perMoney
    return resDict

"""计算用户每个月的总借款金额"""
def computeSumMonthLoad():
    with open(unicode('../dataFile/用户每个月的借款(借款总金额)', 'utf-8'), 'w') as e:
        with open(unicode('../dataFile/用户每个月的借款记录条数(分期到月)', 'utf-8'), 'r') as e1:
            for line in e1:
                data = json.loads(line)
                id = data[0]
                if id == '26308':
                    print data
                resDict = {}
                for key in data[-1]:
                    count = 0
                    for ls in data[-1][key]:
                        count+=float(ls[0])
                    resDict[key] = count
                e.write(json.dumps([id,resDict])+'\n')

if __name__ == '__main__':
    # analysis11MonthLoad()
    # observeLoadPerMonth()
    # extractUserActivateMonth()
    # findUser()
    # computeUserLoadPerMonth()
    computeSumMonthLoad()