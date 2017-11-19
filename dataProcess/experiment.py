#coding=utf-8

import pandas as pd
useridLs = [1,2,1]
userLoanSumLs = [9,8,10]
userLoanLs = [1,3,2]

resDict = pd.DataFrame({'uid':useridLs,'loanSum':userLoanSumLs,'loan11':userLoanLs})
print resDict
# resDict.to_csv('../datafile/train.csv',index=False)
print resDict.groupby('uid').describe()

print float("5.0705925702")