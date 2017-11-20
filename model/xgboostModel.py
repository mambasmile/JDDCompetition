#coding=utf-8

import pandas as pd
import numpy as np
import xgboost as xgb
from xgboost.sklearn import XGBClassifier
from xgboost.sklearn import XGBRegressor
from sklearn.preprocessing import scale,StandardScaler
from sklearn.preprocessing import PolynomialFeatures

from sklearn import cross_validation, metrics   #Additional     scklearn functions
from sklearn.grid_search import GridSearchCV   #Perforing grid search
from sklearn.cross_validation import StratifiedKFold
from sklearn.metrics import fbeta_score, make_scorer

import random
import json

all_submit_path = ''
classifyLabel = '../trainFile/submission.csv'
regressorValue = '../modelResult/submission.csv'

class xgboostModel():

    def modelTest(self,xgbClassify, trainDF, features, label,):
        pos_train_idLs = trainDF[trainDF[label]==1].id.tolist()
        neg_train_idLs = trainDF[trainDF[label]==0].id.tolist()

        pos_index = np.random.permutation(pos_train_idLs)
        neg_index = np.random.permutation(neg_train_idLs)

        pos_loc1 = int(pos_index.__len__()*0.2)
        pos_loc2 = int(pos_index.__len__()*0.4)
        pos_loc3 = int(pos_index.__len__()*0.6)
        pos_loc4 = int(pos_index.__len__()*0.8)

        neg_loc1 = int(neg_index.__len__()*0.2)
        neg_loc2 = int(neg_index.__len__()*0.4)
        neg_loc3 = int(neg_index.__len__()*0.6)
        neg_loc4 = int(neg_index.__len__()*0.8)

        first_pos_trainDF = trainDF[trainDF.id.isin(pos_index[:pos_loc1])]
        first_neg_trainDF = trainDF[trainDF.id.isin(neg_index[:neg_loc1])]
        first_subdf = pd.concat([first_pos_trainDF, first_neg_trainDF])

        second_pos_trainDF = trainDF[trainDF.id.isin(pos_index[pos_loc1:pos_loc2])]
        second_neg_trainDF = trainDF[trainDF.id.isin(neg_index[neg_loc1:neg_loc2])]
        second_subdf = pd.concat([second_pos_trainDF, second_neg_trainDF])

        third_pos_trainDF = trainDF[trainDF.id.isin(pos_index[pos_loc2:pos_loc3])]
        third_neg_trainDF = trainDF[trainDF.id.isin(neg_index[neg_loc2:neg_loc3])]
        third_subdf = pd.concat([third_pos_trainDF, third_neg_trainDF])

        fourth_pos_trainDF = trainDF[trainDF.id.isin(pos_index[pos_loc3:pos_loc4])]
        fourth_neg_trainDF = trainDF[trainDF.id.isin(neg_index[neg_loc3:neg_loc4])]
        fourth_subdf = pd.concat([fourth_pos_trainDF, fourth_neg_trainDF])

        fifth_pos_trainDF = trainDF[trainDF.id.isin(pos_index[pos_loc4:])]
        fifth_neg_trainDF = trainDF[trainDF.id.isin(neg_index[neg_loc4:])]
        fifth_subdf = pd.concat([fifth_pos_trainDF,fifth_neg_trainDF])


        """train--------------------"""
        target_testDF = fifth_subdf


        """first train"""
        res_trainDF = pd.concat([first_subdf, second_subdf, third_subdf])
        res_testDF = fourth_subdf
        xgbClassify.fit(res_trainDF[features], res_trainDF[label], eval_metric='auc')
        dtestDF_predprob = xgbClassify.predict_proba(res_testDF[features])[:, 1]
        firstmetric = metrics.roc_auc_score(res_testDF[label], dtestDF_predprob)
        pd.Series(xgbClassify.booster().get_fscore()).sort_values(ascending=False).to_csv(
            '../trainFile/分类特征权重{0}.csv'.format(0))

        targetDF_predprob = xgbClassify.predict_proba(target_testDF[features])[:, 1]
        targetmetric1 = metrics.roc_auc_score(target_testDF[label], targetDF_predprob)
        print('first metric:    ',firstmetric)
        print('targetmetric1:    ',targetmetric1)

        """second train"""
        res_trainDF = pd.concat([second_subdf,third_subdf,fourth_subdf])
        res_testDF = first_subdf

        xgbClassify.fit(res_trainDF[features], res_trainDF[label], eval_metric='auc')
        dtestDF_predprob = xgbClassify.predict_proba(res_testDF[features])[:, 1]
        secondmetric = metrics.roc_auc_score(res_testDF[label], dtestDF_predprob)
        pd.Series(xgbClassify.booster().get_fscore()).sort_values(ascending=False).to_csv(
            '../trainFile/分类特征权重{0}.csv'.format(1))

        targetDF_predprob = xgbClassify.predict_proba(target_testDF[features])[:, 1]
        targetmetric2 = metrics.roc_auc_score(target_testDF[label], targetDF_predprob)
        print('second metric:    ', secondmetric)
        print('targetmetric2:    ', targetmetric2)

        """third train"""
        res_trainDF = pd.concat([first_subdf,third_subdf,fourth_subdf])
        res_testDF = second_subdf

        xgbClassify.fit(res_trainDF[features], res_trainDF[label], eval_metric='auc')
        dtestDF_predprob = xgbClassify.predict_proba(res_testDF[features])[:, 1]
        thirdmetric = metrics.roc_auc_score(res_testDF[label], dtestDF_predprob)
        pd.Series(xgbClassify.booster().get_fscore()).sort_values(ascending=False).to_csv(
            '../trainFile/分类特征权重{0}.csv'.format(2))

        targetDF_predprob = xgbClassify.predict_proba(target_testDF[features])[:, 1]
        targetmetric3 = metrics.roc_auc_score(target_testDF[label], targetDF_predprob)
        print('third metric:    ', thirdmetric)
        print('targetmetric3:    ', targetmetric3)

        """fourth train"""
        res_trainDF = pd.concat([fifth_subdf,first_subdf,second_subdf,fourth_subdf])
        res_testDF = third_subdf

        xgbClassify.fit(res_trainDF[features], res_trainDF[label], eval_metric='auc')
        dtestDF_predprob = xgbClassify.predict_proba(res_testDF[features])[:, 1]
        fourthmetric = metrics.roc_auc_score(res_testDF[label], dtestDF_predprob)
        pd.Series(xgbClassify.booster().get_fscore()).sort_values(ascending=False).to_csv(
            '../trainFile/分类特征权重{0}.csv'.format(3))

        targetDF_predprob = xgbClassify.predict_proba(target_testDF[features])[:, 1]
        targetmetric4 = metrics.roc_auc_score(target_testDF[label], targetDF_predprob)
        print('fourth metric:    ', fourthmetric)
        print('targetmetric4:    ', targetmetric4)

        # print firstmetric
        # print secondmetric
        # print thirdmetric
        # print fourthmetric

        print("AUC Score (Train): %f" % ((firstmetric+secondmetric+thirdmetric+fourthmetric)/4.0))
        print("AUC Score (Test): %f" % ((targetmetric1+targetmetric2+targetmetric3+targetmetric4)/4.0))

    def modelfit(self, xgbClassify, xgbRegressor, trainDF, testDF, features, label,value,classifySymbol=True,regressorSymbol=True,
                 useTrainCV=True, cv_folds=5, early_stopping_rounds=50,i=0):
        if useTrainCV:
            xgb_param = xgbClassify.get_xgb_params()
            xgtrain = xgb.DMatrix(trainDF[features].values, label=trainDF[label].values)
            cvresult = xgb.cv(xgb_param, xgtrain, num_boost_round=xgbClassify.get_params()['n_estimators'], nfold=cv_folds,
                              metrics='mae', early_stopping_rounds=early_stopping_rounds)
            xgbClassify.set_params(n_estimators=cvresult.shape[0])

        # Fit the algorithm on the data
        # processTrainDF = StandardScaler().fit_transform(trainDF[numericFeature])
        # processTestDF = StandardScaler().fit_transform(testDF[numericFeature])

        processTrainDF = trainDF[features]
        processTestDF = testDF[features]

        if classifySymbol:

            xgbClassify.fit(processTrainDF, trainDF[label], eval_metric='auc')
            dtrain_predprob = xgbClassify.predict_proba(processTrainDF)[:, 1]

            # predict test set:
            dtest_predprob = xgbClassify.predict_proba(processTestDF)[:, 1]
            submission_prob = pd.DataFrame(data={"id": testDF.id, "predict": dtest_predprob})

            pd.Series(xgbClassify.booster().get_fscore()).sort_values(ascending=False).to_csv(
                '../modelResult/分类特征权重{0}.csv'.format(i))

        if regressorSymbol:
            xgbRegressor.fit(processTrainDF, trainDF[value], eval_metric='mae')

            """
            predict future dep prob and print the auc and accuracy 
            """
            # Predict training set:
            dtrain_preValue = xgbRegressor.predict(processTrainDF)
            # dtrain_preValue = np.expm1(dtrain_preValue)

            dtest_preValue = xgbRegressor.predict(processTestDF)
            # dtest_preValue = np.expm1(dtest_preValue)
            print(dtest_preValue.size)
            submission_value = pd.DataFrame(data={"uid": testDF.uid, "value": dtest_preValue})
            pd.Series(xgbRegressor.booster().get_fscore()).sort_values(ascending=False).to_csv(
                '../modelResult/回归特征权重{0}.csv'.format(i))

        if classifySymbol and regressorSymbol:
            submission = pd.merge(left=submission_prob, right=submission_value, on='fuid_md5')
            submission.to_csv(all_submit_path, sep=' ', columns=None, index_label="", index=False)
            # Print model report:
            print("\nModel Report")
            print("Accuracy : %.4g" % metrics.mean_absolute_error(trainDF[value].values, dtrain_preValue))
            print("AUC Score (Train): %f" % metrics.roc_auc_score(trainDF[label], dtrain_predprob))

        elif classifySymbol:
            submission_prob.to_csv(classifyLabel, columns=['id','predict'], index_label="", index=False)
            print("AUC Score (Train): %f" % metrics.roc_auc_score(trainDF[label], dtrain_predprob))


        elif regressorSymbol:
            submission_value.to_csv(regressorValue, index=False)
            print("Accuracy : %.4g" % metrics.mean_absolute_error(trainDF[value].values, dtrain_preValue))


        """
        predict the future 6 month spend money
        """
        # # Predict training set:
        # dtrain_predictions = alg.predict(dtrain[predictors])
        # #predict test set:
        # dtest_predictions = alg.predict(test_data[predictors])
        # #store to file
        # submission = pd.DataFrame(data={"Id": test_data.fuid_md5, "prob": dtest_predictions})
        # submission.to_csv(future_6_month,index=False)
        # # Print model report:
        # print "\nModel Report"
        # print "MAE (Train): %f" % metrics.mean_absolute_error(dtrain[target], dtrain_predictions)

        # pd.Series(xgbClassify.booster().get_fscore()).sort_values(ascending=False).to_csv('../test_file/特征权重{0}.csv'.format(i))

        # feat_imp = pd.Series(xgbClassify.booster().get_fscore()).sort_values(ascending=False)
        # feat_imp.plot(kind='bar', title='Feature Importances')
        # plt.ylabel('Feature Importance Score')
        # plt.show()



    # symbol=0 表示分类，symbol=1表示回归
    def run(self, symbol,xgbClassify, xgbRegressor, train_data, features, label, value, i=0):
        # Choose all predictors except target & IDcols

        xgb1 = XGBClassifier(
            learning_rate=0.1,
            n_estimators=100,
            max_depth=6,
            min_child_weight=3,
            gamma=0,
            subsample=0.8,
            colsample_bytree=0.8,
            objective='binary:logistic',
            nthread=4,
            scale_pos_weight=1,
            seed=27)
        xgb2 = XGBRegressor(

            learning_rate=0.1,
            n_estimators=140,
            max_depth=7,
            min_child_weight=1,
            gamma=0,
            subsample=0.8,
            colsample_bytree=0.8,
            objective='reg:linear',
            nthread=4,
            scale_pos_weight=1,
            seed=27
        )
        # self.modelfit(xgb1, train_data, predictors)
        # self.modelfit(xgb2, train_data, predictors)
        #

        if symbol == 1:
            # """
            # choose the premeter for xgbregressor
            # """
            param_test1 = {
             # 'max_depth':list(range(3,11,1)),
             # 'min_child_weight':list(range(1,6,1),)
             # 'n_estimators':range(100,1000,100)
            }
            gsearch1 = GridSearchCV(estimator=xgbRegressor,param_grid = param_test1,     scoring='neg_mean_squared_error',n_jobs=4,iid=False, cv=5)
            gsearch1.fit(train_data[features], train_data[value])
            print("xgbregressor:",gsearch1.grid_scores_, gsearch1.best_params_,     gsearch1.best_score_)
            pd.Series(xgbRegressor.booster().get_fscore()).sort_values(ascending=False).to_csv(
                '../modelResult/回归特征权重{0}.csv'.format(i))

        elif symbol == 0:
            #
            #
            # """
            # choose the premeter for xgbclassifier
            # """
            param_test1 = {
             # 'n_estimators':range(200,400,20),
             # 'min_child_weight':[4,5,6],
             # 'max_depth': [3,4,5,6],
             # 'max_depth': range(1,11,1),
             # "learning_rate": [i/100.0 for i in range(1, 6, 1)]
             # 'gamma': [i / 10.0 for i in range(0, 5)]
            # 'subsample': [i / 10.0 for i in range(6, 10)],
            # 'colsample_bytree': [i / 10.0 for i in range(6, 10)],
            # 'reg_alpha': [0, 0.001, 0.005, 0.01, 0.05]
            #     'learning_rate':[i / 100.0 for i in range(5, 20,1)]
            #     'reg_lambda' : [1,2,3,4]
            }

            RF_param_test = {
                # 'n_estimators': range(600, 710, 10),
                # 'max_depth':range(5,15,1),
                # 'min_samples_leaf':range(1,9,1)
            }

            gsearch1 = GridSearchCV(estimator = xgbClassify,
             param_grid = param_test1,     scoring='roc_auc',n_jobs=4,iid=False, cv=5)
            # ploy = PolynomialFeatures(2)
            # gsearch1.fit(ploy.fit_transform(train_data[features].values), train_data[label].values)

            # y_train = train_data[label].copy()
            # train_data.pop(label)


            gsearch1.fit(train_data[features], train_data[label])
            print("xgbclassifier:",gsearch1.grid_scores_, gsearch1.best_params_,     gsearch1.best_score_)
            pd.Series(xgbClassify.booster().get_fscore()).sort_values(ascending=False).to_csv(
                '../trainFile/分类特征权重{0}.csv'.format(i))
            # print xgbClassify.booster().get_fscore()

            # feat_imp = pd.Series(xgbClassify.booster().get_fscore()).sort_values(ascending=False)
            # tmpLs = []

            # for key in feat_imp:
            #     tmpLs.append(columns[int(key)])
            # tmpDataFrame = pd.DataFrame(feat_imp)
            # tmpDataFrame['feature'] = tmpLs
            # tmpDataFrame.to_csv('data.csv',index=True)
            # feat_imp.plot(kind='bar', title='Feature Importances')
            # plt.ylabel('Feature Importance Score')
            # plt.show()

    def runMetric(self,xgbClassify,training_matrix, y_train,testing_matrix, y_test):
        param_test1 = {
            # 'n_estimators':range(200,400,20),
            # 'min_child_weight':[4,5,6],
            # 'max_depth': [3,4,5,6],
            # 'max_depth': range(1,11,1),
            # "learning_rate": [i/100.0 for i in range(1, 6, 1)]
            # 'gamma': [i / 10.0 for i in range(0, 5)]
            # 'subsample': [i / 10.0 for i in range(6, 10)],
            # 'colsample_bytree': [i / 10.0 for i in range(6, 10)],
            # 'reg_alpha': [0, 0.001, 0.005, 0.01, 0.05]
            #     'learning_rate':[i / 100.0 for i in range(5, 20,1)]
            #     'reg_lambda' : [1,2,3,4]
        }
        gsearch1 = GridSearchCV(estimator=xgbClassify,
                                param_grid=param_test1, scoring='roc_auc', n_jobs=4, iid=False, cv=5)
        gsearch1.fit(training_matrix, y_train)
        print("xgbclassifier:", gsearch1.grid_scores_, gsearch1.best_params_, gsearch1.best_score_)

    def submission(self):
        """
        merge two submission part
        :return:
        """
        prob = pd.read_csv(classifyLabel)
        money = pd.read_csv(regressorValue)
        all_submit_data = pd.merge(prob,money,on="Id")
        all_submit_data.to_csv(all_submit_path,sep=' ',columns=None,index_label="", index=False)


if __name__ == '__main__':
    xgbClassify = xgb.XGBClassifier(
        learning_rate=0.111,
        n_estimators=125,
        max_depth=3,
        min_child_weight=4,
        gamma=0,
        subsample=0.6,
        colsample_bytree=0.9,
        objective='binary:logistic',
        nthread=4,
        scale_pos_weight=10,
        seed=27,
        )
    xgbRegressor = xgb.XGBRegressor(learning_rate=0.1,
            n_estimators=140,
            max_depth=3,
            min_child_weight=2,
            gamma=0,
            subsample=0.8,
            colsample_bytree=0.8,
            objective='reg:linear',
            nthread=4,
            scale_pos_weight=1,
            seed=27)


    trainDF = pd.read_csv(r'C:\Users\13277\PycharmProjects\JDDCompetition\corpus/train.csv')
    testDF = pd.read_csv(r'C:\Users\13277\PycharmProjects\JDDCompetition\corpus/test.csv')
    featureLs = trainDF.columns.tolist()
    featureLs.remove('uid')

    valueDF = pd.read_csv(r'C:\Users\13277\PycharmProjects\JDDCompetition\corpus/value.csv')
    trainDF = pd.merge(trainDF,valueDF,on='uid')
    value = 'loan_sum'


    xgbRegressorModel = xgboostModel()
    # xgbRegressorModel.run(1,None, xgbRegressor, trainDF, featureLs, None, value, i=0)

    xgbRegressorModel.modelfit(None, xgbRegressor, trainDF, testDF, featureLs, None, value, classifySymbol=False,
             regressorSymbol=True,
             useTrainCV=False, cv_folds=5, early_stopping_rounds=50, i=0)
    # print(trainDF.count())
    # print(testDF.count())


