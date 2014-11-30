from baseline import *
import cPickle as pickle
from  word2vec import *
import numpy as np
import engine

# owner: rqi
# This file tests our extractor by measuring its performace on
# capturing sample similarities in terms of category, score etc.

############################################
# Read in training and test data..
# DIM = 20  # how many word to extract into vectors
# TRAINING_SET_RATIO = 0.6  # 40% hold out rate
# TESTING_SEGMENTS = 10

'''
b0 = pickle.load(open('business0.dict', 'rb'))  # French
b1 = pickle.load(open('business1.dict', 'rb'))  # chinese
b2 = pickle.load(open('business2.dict', 'rb'))  # auto
'''
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



trainingData = pickle.load(open('tiny_train.dat', 'rb'))  # business list
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
#     print "b1Cats=%s" % (b1Cats)
#     print "b2Cats=%s" % (b2Cats)
#     print "distance=%s" % (dist)
    sameCatCnt = 0
    for c1 in b1Cats:
        for c2 in b2Cats:
            if c1 == c2:
                sameCatCnt += 1
	catSimilarity = 2 * sameCatCnt / float(len(b1Cats) + len(b2Cats))  # between 0~1
	return (catSimilarity - 0.5) * dist

N = 100
testingData = trainingData[1:N]
cost_ave = 0.0
cost_min = 0.0
cost_max = 0.0

feature = {}
i = 0

wordVec = load("vectorsstnn_review.bin", 'bin')
print 'please input your query:'
userinput = sys.stdin.readline()
words = userinput.split()
queryVec = []

for word in words:
    if word in wordVec.vocab:
        vec = wordVec.get_vector(word)
        queryVec.append(vec)


minDist1 = float('inf')
minDist2 = float('inf')
for b in testingData:
    i += 1
    print "%d out of %d" % (i, len(testingData))
    feature[b['business_id']] = baselineExtractor.extract(b)
    s1 = feature[b['business_id']]
    dist_min = baselineExtractor.distance(s1, queryVec, 'min')
    dist_ave = baselineExtractor.distance(s1, queryVec, 'ave')
    print dist_min
    print dist_ave
    if dist_min < minDist1:
        minDist1 = dist_min
        bestMatch1 = b
    if dist_ave < minDist2:
        minDist2 = dist_ave
        bestMatch2 = b

print "min best match name = %s" % (bestMatch1['name'])
baselineExtractor.extract(bestMatch1)
print "best match categories = %s" % (bestMatch1['categories'])
print "best match stars = %s" % (bestMatch1['stars'])


print "ave best match name = %s" % (bestMatch2['name'])
baselineExtractor.extract(bestMatch2)
print "best match categories = %s" % (bestMatch2['categories'])
print "best match stars = %s" % (bestMatch2['stars'])





for b1 in testingData:
    for b2 in testingData:
        if b1 == b2: continue
        s1 = feature[b1['business_id']]
        s2 = feature[b2['business_id']]
        dist_ave = baselineExtractor.distance(s1, s2, 'ave')
        dist_min = baselineExtractor.distance(s1, s2, 'min')
        dist_max = baselineExtractor.distance(s1, s2, 'max')
        cost_ave += evaluate(b1, b2, dist_ave)
        cost_min += evaluate(b1, b2, dist_min)
        cost_max += evaluate(b1, b2, dist_max)

print "cost using ave distance=%f" % (cost_ave / (N - 1) / (N - 1))
print "cost using min distance=%f" % (cost_min / (N - 1) / (N - 1))
print "cost using max distance=%f" % (cost_max / (N - 1) / (N - 1))
