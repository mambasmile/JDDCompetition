#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/21 14:50
# @Author  : sunday
# @Site    :
# @File    : convertMoney.py
# @Software: PyCharm
from datetime import datetime
import pandas as pd
import json
import numpy as np
from fileConfig import fileConfig
from math import log

"""将文件中所有的金额数据转换为实际数据"""
class convertMoney:
    def convertMoney(self, money):
        try:
            money = np.power(5,money)-1
            return money
        except:
            print money

    def reverseConvertMoney(self,file,outpath):
        i = 0
        with open(outpath,'w') as e:
            with open(file,'r') as e1:
                for line in e1:
                    if i==0:
                        i+=1
                        continue
                    data = line.strip().split(',')
                    value = float(data[-1])+1
                    if value <= 0:
                        money = 0
                    else:
                        money = log(value,5)
                    e.write(data[0]+','+str(money)+'\n')

    def save2File(self, data, path):
        data.to_csv(path,index = False)



    def run(self):
        orderFile = pd.read_csv(fileConfig.tmp_orderFile)
        loanFile = pd.read_csv(fileConfig.loanFile)
        loanSumFile = pd.read_csv(fileConfig.loanSumFile)
        userFile = pd.read_csv(fileConfig.userFile)

        # print self.convertOrder(orderFile.price)
        orderFile.discount = self.convertMoney(orderFile.discount)
        orderFile.price = self.convertMoney(orderFile.price)
        userFile.limit = self.convertMoney(userFile.limit)

        loanFile.loan_amount = self.convertMoney(loanFile.loan_amount)
        loanSumFile.loan_sum = self.convertMoney(loanSumFile.loan_sum)

        self.save2File(loanFile, fileConfig.CovertedloanFile)
        self.save2File(loanSumFile, fileConfig.CovertedloanSumFile)
        self.save2File(orderFile, fileConfig.CovertedorderFile)
        self.save2File(userFile, fileConfig.CoverteduserFile)

    def convertDF(self,df,featureLs):
        for feature in featureLs:
            df[feature] = self.convertMoney(df[feature])
        return df

if __name__ == '__main__':
    convert = convertMoney()
    # convert.run()

    """结果恢复"""
    convert.reverseConvertMoney(r'C:\Users\13277\PycharmProjects\xgbModel\modelResult\submission.csv',
                                r'C:\Users\13277\PycharmProjects\xgbModel\modelResult\submissionFinal.csv')
