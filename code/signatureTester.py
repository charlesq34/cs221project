from baseline import *
import cPickle as pickle
from  word2vec import *
import numpy as np

# owner: rqi
# This file tests our extractor by measuring its performace on
# capturing sample similarities in terms of category, score etc.

############################################
# Read in training and test data..
# DIM = 20  # how many word to extract into vectors
# TRAINING_SET_RATIO = 0.6  # 40% hold out rate
# TESTING_SEGMENTS = 10

b0 = pickle.load(open('business0.dict', 'rb'))  # French
b1 = pickle.load(open('business1.dict', 'rb'))  # chinese
b2 = pickle.load(open('business2.dict', 'rb'))  # auto

# b1_list = b1.items()
# size = len(b1_list)
# training_size = int(TRAINING_SET_RATIO * round(size))
# trainingSet1 = dict(b1_list[0:training_size])
# testingSet1 = b1_list[training_size:size]
# testingSet1List = zip(*[iter(testingSet1)] * int(round((size - training_size) / TESTING_SEGMENTS)))
# print "size of test=%d" % len(testingSet1List)

# b2_list = b0.items()
# size = len(b2_list)
# training_size = int(TRAINING_SET_RATIO * round(size))
# trainingSet2 = dict(b2_list[0:training_size])
# testingSet2 = b2_list[training_size:size]
# testingSet2List = zip(*[iter(testingSet2)] * int(round((size - training_size) / TESTING_SEGMENTS)))
# print "size of test=%d" % len(testingSet2List)


##########################################
# Train the model
# featureVec1 = computeFeatureVec(trainingSet1)
# featureVec2 = computeFeatureVec(trainingSet2)

trainingData = pickle.load(open('tiny_train.dat', 'rb')) # business list
baselineExtractor = Baseline()
baselineExtractor.train(trainingData)


##########################################
# Test the model
# for testing1 in testingSet1List:
#     vec = baselineExtractor.extract(testing1)
#     dist1 = np.sqrt(np.sum((vec - featureVec1) ** 2))
#     dist2 = np.sqrt(np.sum((vec - featureVec2) ** 2))
#     if dist1 < dist2:
#         print "this is a Category 1, correct"
#     else:
#         print "this is a Category 2, wrong"


# Evaluation value: smaller the better!
def evaluate(b1, b2, dist):
	b1Cats = b1['categories']
	b2Cats = b2['categories']
	sameCatCnt = 0
	for c1 in b1Cats:
		for c2 in b2Cats:
			if c1 == c2:
				sameCatCnt += 1
	catSimilarity = 2 * sameCatCnt / float(len(b1Cats) + len(b2Cats)) # between 0~1

	return (catSimilarity - 0.5) * dist


testingData = trainingData
cost = 0.0
for b1 in testingData:
   for b2 in testingData:
       if b1 == b2: continue
       s1 = baseline.extract(b1)
       s2 = baseline.extract(b2)
       dist = baselineExtractor.distance(s1, s2)
       cost += evaluate(b1, b2, dist)

#print cost