#coding=utf-8

from __init__ import *
"""
分析用户每个月的消费金额：根据月份统计用户每个月总的消费金额
输入：trainCorpus：True 表示构造训练集 |trainCorpus：False 表示构造测试集
输出：train_userMonthLoad.csv  |test_userMonthLoad.csv
"""
def analysisUserLoadPerMonth(trainCorpus=True):
    userDF = pd.read_csv(fileConfig.userFile)
    if trainCorpus:
        monthLs = [8,9,10]
    else:
        monthLs = [9,10,11]
    firstMonthLoad = []
    secondMonthLoad = []
    thirdMonthLoad = []
    uidLs = []

    userLoadDF = pd.read_csv(fileConfig.timeCovertedloanFile)
    for name,group in userLoadDF.groupby('uid'):
        uidLs.append(name)
        tmpSet = set()
        for subname,subgroup in group.groupby('loan_time'):
            tmpSet.add(subname)
            if subname == monthLs[0]:
                firstMonthLoad.append(sum(subgroup.loan_amount.tolist()))
            elif subname == monthLs[1]:
                secondMonthLoad.append(sum(subgroup.loan_amount.tolist()))
            elif subname == monthLs[2]:
                thirdMonthLoad.append(sum(subgroup.loan_amount.tolist()))
        resLs = list(set(monthLs) - tmpSet)
        for ele in resLs:
            if ele == monthLs[0]:
                firstMonthLoad.append(0.0)
            elif ele == monthLs[1]:
                secondMonthLoad.append(0.0)
            elif ele == monthLs[2]:
                thirdMonthLoad.append(0.0)

    resDF = pd.DataFrame({'uid':uidLs,
                          'firstMonthLoad':firstMonthLoad,
                          'secondMonthLoad':secondMonthLoad,
                          'thirdMonthLoad':thirdMonthLoad,
                          })
    resDF = pd.merge(resDF,userDF[['uid']],on='uid',how='right')
    resDF = resDF.fillna(0.0)
    if trainCorpus:
        resDF.to_csv('../corpus/train_userMonthLoad.csv',index=False)
    else:
        resDF.to_csv('../corpus/test_userMonthLoad.csv', index=False)

