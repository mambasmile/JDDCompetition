#coding=utf-8

class fileConfig:

    basicFile = r'D:\京东金融'

    orderFile = unicode(basicFile+r'/t_order.csv', 'utf-8')
    tmp_orderFile = unicode(basicFile+'\t_order1.csv', 'utf-8')

    userFile = unicode(basicFile+r'\t_user.csv', 'utf-8')
    loanSumFile = unicode(basicFile+r'\t_loan_sum.csv', 'utf-8')
    clickFile = unicode(basicFile+r'\t_click.csv', 'utf-8')
    loanFile = unicode(basicFile+r'\t_loan.csv', 'utf-8')

    CovertedloanFile = unicode(basicFile+r'\Coverted_loan.csv', 'utf-8')
    CovertedloanSumFile = unicode(basicFile+r'\Coverted_loan_Sum.csv', 'utf-8')
    CovertedorderFile = unicode(basicFile+r'\Coverted_order1.csv', 'utf-8')
    CoverteduserFile = unicode(basicFile+r'\Coverted_user.csv', 'utf-8')

    CoverteduserCorpusFile = unicode(r'../corpus/Coverted_user.csv', 'utf-8')

    timeCovertedloanFile = unicode(basicFile+r'\timeCoverted_loan.csv', 'utf-8')

