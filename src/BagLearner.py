### Created by Anadi Jaggia
import numpy as np
from engine import RandomForest as rt
from scipy import stats

class BagLearner(object):

    def __init__(self, learner = rt.RFLearner,
                 kwargs = {},
                 boost=False, bags = 20):

        self.learners = []
        for i in range(0,bags):
            self.learners.append(learner(**kwargs))


    def addEvidence(self, Xtrain, Ytrain):

        n = Xtrain.shape[0]

        for learner in self.learners:

            XtrainBag = np.zeros(shape=(n, Xtrain.shape[1]))
            YtrainBag = np.zeros(n)

            for j in range(0, n):

                r = np.random.randint(0, high=n)
                XtrainBag[j,:] = Xtrain[r,:]
                YtrainBag[j] = Ytrain[r]

            learner.addEvidence(XtrainBag, YtrainBag)


    def query(self, Xtest):

        YBags = np.zeros(shape=(Xtest.shape[0], len(self.learners)))

        for j in range(0,len(self.learners)):
            YBags[:, j] = self.learners[j].query(Xtest)

        mode = stats.mode(YBags, axis=1)
        Y = mode[0]

        return Y





