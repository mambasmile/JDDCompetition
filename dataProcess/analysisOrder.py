#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/22 10:58
# @Author  : sunday
# @Site    : 
# @File    : analysisOrder.py
# @Software: PyCharm
from __init__ import *


"""
分析用户的order文件，将用户每个月的消费记录抽取出来
统计每个月的的订单数
输入 trainCorpus：True |trainCorpus ：False
输出 train_order.csv |test_order.csv
"""

def analysisOrder(trainCorpus=True):
    basicFile = 'corpus'
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

