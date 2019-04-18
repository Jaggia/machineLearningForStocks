### Created by Anadi Jaggia
import pandas as pd
from scipy import stats
from sklearn.ensemble import RandomForestClassifier


class RTLearner(object):

    def __init__(self, leaf_size = 1):
        self.leaf_size = leaf_size
        self.learner = RandomForestClassifier(n_estimators=100, max_depth=3)


    def addEvidence(self, Xtrain, Ytrain):
        Ytrain = Ytrain.reshape((Ytrain.shape[0],))
        print(Xtrain.shape)
        print(Ytrain.shape)

        self.learner.fit(Xtrain, Ytrain)
        print("Feature Importances : ")
        print(self.learner.feature_importances_)


    # index is for building dates associated with decisions
    def query(self, Xtest, symbol, index, visualize=False):
        Y = self.learner.predict(Xtest)

        currPos = 0.0
        df_trades = pd.DataFrame(currPos,
                                 index=index,
                                 columns=[symbol])

        # buy a 1000 shares lol
        for i in range(df_trades.shape[0]):
            df_trades[symbol].iloc[i] = Y[i] * 1000.0 - currPos
            currPos += df_trades[symbol].iloc[i]

        # print(Y)
        if visualize:
            pass
            self.visualizeVals()
        return df_trades
