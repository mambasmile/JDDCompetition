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
"""将文件中所有的金额数据转换为实际数据"""
class convertMoney:
    def convertMoney(self, money):
        try:
            money = np.power(5,money)-1
            return money
        except e:
            print money

    def save2File(self, data, path):
        data.to_csv(path,index = False)
    """将实际金额转换为指数金额"""
    def convertSubmissonMoney(self,realMoney):
        convertedMoney = np.log(realMoney+1)/np.log(5)
        return convertedMoney
    def run(self):
        orderFile = pd.read_csv(fileConfig.orderFile)
        loanFile = pd.read_csv(fileConfig.loanFile)
        loanSumFile = pd.read_csv(fileConfig.loanSumFile)
        userFile = pd.read_csv(fileConfig.userFile)


        orderFile.discount = self.convertMoney(orderFile.discount)
        orderFile.price = self.convertMoney(orderFile.price)
        userFile.limit = self.convertMoney(userFile.limit)

        loanFile.loan_amount = self.convertMoney(loanFile.loan_amount)
        loanSumFile.loan_sum = self.convertMoney(loanSumFile.loan_sum)

        self.save2File(loanFile, fileConfig.CovertedloanFile)
        self.save2File(loanSumFile, fileConfig.CovertedloanSumFile)
        self.save2File(orderFile, fileConfig.CovertedorderFile)
        self.save2File(userFile, fileConfig.CoverteduserFile)

convert = convertMoney()
convert.run()
