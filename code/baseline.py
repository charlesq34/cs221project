from signatureExtractor import *
from engine import computeFeatureVec
import util
import numpy

class Baseline(SignatureExtractor):
    
    def train(self, trainingData):
        pass

    def extract(self, x):
    	data = [util.text2words(r['text']) for r in x['reviews']]

        featureVec = computeFeatureVec(data)
        return featureVec

    def distance(self, s1, s2):
    	return numpy.sqrt(numpy.sum((s1-s2)**2))