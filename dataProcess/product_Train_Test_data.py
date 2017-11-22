#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/21 22:05
# @Author  : sunday
# @Site    : 
# @File    : produce_Train_Test_data.py
# @Software: PyCharm

from __init__ import *

"""生成特征"""
def produce_features_file():
    fillUserLoadSum()
    clickCorpus(True)
    clickCorpus(False)
    analysisUserLoadPerMonth(True)
    analysisUserLoadPerMonth(False)
    analysisOrder(True)
    analysisOrder(False)

"""合并数据集"""
def mergeDF():
    convertDFMoney = convertMoney()

    basicFile = 'corpus'
    userDF = pd.read_csv(unicode(r'../dataFile/t_user提取用户的激活时间.csv','utf-8'))
    trainOrder = pd.read_csv(unicode(r'../'+basicFile+'/train_order.csv','utf-8'))
    testOrder = pd.read_csv(unicode(r'../'+basicFile+'/test_order.csv','utf-8'))
    trainClick = pd.read_csv(unicode(r'../'+basicFile+'/train_click.csv','utf-8'))
    testClick = pd.read_csv(unicode(r'../'+basicFile+'/test_click.csv','utf-8'))

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

    mergeDF()
    # produce_features_file()