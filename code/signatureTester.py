from baseline import *
import cPickle as pickle
from  word2vec import *
import numpy as np
import engine

# owner: rqi
# This file tests our extractor by measuring its performace on
# capturing sample similarities in terms of category, score etc.

############################################
# Read in training and test data...
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




##########################################
# Train the model
# featureVec1 = computeFeatureVec(trainingSet1)
# featureVec2 = computeFeatureVec(trainingSet2)

trainingData = pickle.load(open('tiny_train.dat', 'rb'))  # business list
baselineExtractor = Baseline()
baselineExtractor.train(trainingData)


##########################################
# Test the model




N = 100
testingData = trainingData[1:N]
cost_ave = 0.0
cost_min = 0.0
cost_max = 0.0
feature = {}
i = 0
wordVec = load("vectorsstnn_review.bin", 'bin')

for b in testingData:
    i += 1
    print "extracting %d out of %d shops" % (i, len(testingData))
    feature[b['business_id']] = baselineExtractor.extract(b)

##########################################
def findBestMatch(queryVec, queryShop=None):
    minDist1 = float('inf')
    minDist2 = float('inf')

    for b in testingData :
        if b == queryShop: continue
        s1 = feature[b['business_id']]
        dist_min = baselineExtractor.distance(s1, queryVec, 'min')
        dist_ave = baselineExtractor.distance(s1, queryVec, 'ave')
#         print dist_min
#         print dist_ave
        if dist_min < minDist1:
            minDist1 = dist_min
            bestMatch1 = b
        if dist_ave < minDist2:
            minDist2 = dist_ave
            bestMatch2 = b
    print '\n####################### Min Distance Match ###########################'
    print "min best match name = %s" % (bestMatch1['name'])
    print "best match categories = %s" % (bestMatch1['categories'])
    print "best match stars = %s" % (bestMatch1['stars'])
    baselineExtractor.extract(bestMatch1)

    print '\n###################### Ave Distance Match ######################'
    print "ave best match name = %s" % (bestMatch2['name'])
    print "best match categories = %s" % (bestMatch2['categories'])
    print "best match stars = %s" % (bestMatch2['stars'])
    baselineExtractor.extract(bestMatch2)
##########################################


while 1:
    print '############################################################'
    print 'please input what do you want to do: 1 for search, 2 for recommendation, 3 for categorization'
    choice = sys.stdin.readline()
    if choice == '1\n':
        print 'please input the query words:'
        userinput = sys.stdin.readline()
        words = userinput.split()
        queryVec = []

        for word in words:
            if word in wordVec.vocab:
                vec = wordVec.get_vector(word)
                queryVec.append(vec)

        findBestMatch(queryVec)




    if choice == '2\n':
        print 'please input the restaurant number you liked:'
        userinput = sys.stdin.readline()
        th = int(userinput.split()[0])
        queryShop = trainingData[th]
        print "query restaurant name = %s" % (queryShop['name'])
        print "query restaurant categories = %s" % (queryShop['categories'])
        print "query restaurant stars = %s" % (queryShop['stars'])
        queryVec = baselineExtractor.extract(queryShop)

        findBestMatch(queryVec, queryShop)


    if choice == '3\n':
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









