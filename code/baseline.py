from signatureExtractor import *
from engine import computeFeatureVec_single_biz
import util
import numpy as np

class Baseline(SignatureExtractor):

    def train(self, trainingData):
        pass

    def extract(self, x):
        data = [util.text2words(r['text']) for r in x['reviews']]
        featureVec = computeFeatureVec_single_biz(data)
        return featureVec

    def distance(self, s1, s2, op='ave'):
        if op == 'min':
            return getMinDistance(s1, s2)
        if op == 'max':
            return getMaxDistance(s1, s2)
        if op == 'ave':
            return getAveDistance(s1, s2)
        if op == 'mean_vec':
            return getMeanVecDistance(s1, s2)

def getMeanVecDistance(vecList1, vecList2):
    meanVec1 = vecList1[0]
    meanVec2 = vecList2[0]
    for i in range(len(vecList1)):
        meanVec1 = np.add(meanVec1, vecList1[i])
    meanVec1 = np.divide(meanVec1, len(vecList1))
    for i in range(len(vecList2)):
        meanVec2 = np.add(meanVec2, vecList2[i])
    meanVec2 = np.divide(meanVec2, len(vecList2))
    return np.sqrt(np.sum((meanVec1 - meanVec2) ** 2))

def getMinDistance(vecList1, vecList2):
    minDis = float('inf')
    for vec_1 in vecList1:
        for vec_2 in vecList2:
            dist = np.sqrt(np.sum((vec_1 - vec_2) ** 2))
            if dist < minDis:
                minDis = dist
    return minDis

def getMaxDistance(vecList1, vecList2):
    maxDis = float('-inf')
    for vec_1 in vecList1:
        for vec_2 in vecList2:
            dist = np.sqrt(np.sum((vec_1 - vec_2) ** 2))
            if dist > maxDis:
                maxDis = dist
    return maxDis

def getAveDistance(vecList1, vecList2):
    totalDis = 0
    for vec_1 in vecList1:
        for vec_2 in vecList2:
            dist = np.sqrt(np.sum((vec_1 - vec_2) ** 2))
            totalDis += dist
    return totalDis / len(vecList1) / len(vecList2)