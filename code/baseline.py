from signatureExtractor import *
from engine import computeFeatureVec


class Baseline(SignatureExtractor):
    
    def train(self, trainingData):
        pass

    def extract(self, x):
        featureVec = computeFeatureVec(dict(x))
        return featureVec
