### Created by Anadi Jaggia
import numpy as np
from scipy import stats

class RTLearner(object):

    def __init__(self, leaf_size = 1):
        self.leaf_size = leaf_size

    def addEvidence(self, Xtrain, Ytrain):
        
        def build_tree(data):
            
            if data.shape[0] <= self.leaf_size:
                mode = stats.mode(data[:, -1], axis=None)
                return np.array([[-9999.0, mode[0], np.nan, np.nan]])

            elif np.all(data[:, -1] == data[0, -1]):
                return np.array([[-9999.0, data[0,-1], np.nan, np.nan]])

            else:

                factor = np.random.randint(0, high=data.shape[1] - 1)
                
                splitval = np.nanmedian(data[:, factor])

                if data[data[:, factor] <= splitval].size == 0 or \
                   data[data[:, factor] > splitval].size == 0:
                    try:
                        splitval = np.nanmean(data[:, factor])
                    except:
                        print(np.nanmean(data[:, factor]))

                if data[data[:, factor] <= splitval].size == 0 or \
                   data[data[:, factor] > splitval].size == 0:
                    mode = stats.mode(data[:, -1], axis=None)
                    return np.array([[-9999.0, mode[0], np.nan, np.nan]])

                lefttree = build_tree(data[data[:, factor] <= splitval])
                righttree = build_tree(data[data[:, factor] > splitval])

                root = np.array([[factor, splitval, 1, lefttree.shape[0] + 1]])

                return np.concatenate((root, lefttree, righttree), axis=0)

        data = np.concatenate((Xtrain, np.reshape(Ytrain, (Ytrain.shape[0], 1))), axis=1)
        self.tree = build_tree(data)


    def query(self, Xtest):

        n = Xtest.shape[0]
        
        Y = np.zeros(shape=(1, n))
        
        for j in range(0, n):

            i = 0
            while self.tree[i, 0] != -9999.0:
                if Xtest[j, int(self.tree[i,0])] <= self.tree[i, 1]:
                    i += int(self.tree[i,2])
                else:
                    i += int(self.tree[i,3])

            Y[0,j] = self.tree[i, 1]

        return Y
