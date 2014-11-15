from signatureExtractor import *
from engine import computeFeatureVec


class Baseline(signatureExtractor):
    
    def train(trainingData):
        trainingSet1, trainingSet2 = trainingData
        self.featureVec1 = computeFeatureVec(trainingSet1)
        self.featureVec2 = computeFeatureVec(trainingSet2)

    def extract(x):
        featureVec = computeFeatureVec(dict(x))
        dist1 = np.sqrt(np.sum((featureVec - self.featureVec1) ** 2))
        dist2 = np.sqrt(np.sum((featureVec - self.featureVec2) ** 2))
        return dist1 < dist2
