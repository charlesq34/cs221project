import sys, collections, math, re
import cPickle as pickle
from  word2vec import *
import numpy as np

## DIM = 30 for b1 and b2: 90% correct
## DIM = 20 for b0 and b1: 70% correct
DIM = 20  # how many word to extract into vectors
#TRAINING_SET_RATIO = 0.6  # 40% hold out rate
#TESTING_SEGMENTS = 10
#
#
#r11 = ["french restaurant", "good restaurant"]
#r12 = ["nice food", "french fries is lovely"]
#
#r21 = ["high speed", "clean and cheap"]
#r22 = [ "nice and good"]
#
#r11 = ["a a", "b  b", "b b c", "c"]
#r12 = ["a", "b a", "a c"]
#
#r21 = ["high speed", "clean and cheap"]
#r22 = [ "nice and good"]
#
#b0 = pickle.load(open('business0.dict', 'rb'))  # French
#b1 = pickle.load(open('business1.dict', 'rb'))  # chinese
#b2 = pickle.load(open('business2.dict', 'rb'))  # auto
#
#
#FrenchData = {"shop1":[review.split() for review in r11], "shop2":[review.split() for review in r12]}
#AutoData = {"Auto1":[review.split() for review in r21], "Auto2":[review.split() for review in r22]}
#wordVec = load("vectors.bin", 'bin')  # this load is from word2vec package
#
## {'shop2': [['nice', 'food'], ['french', 'fries']], 'shop1': [['french', 'restaurant'], ['good', 'restaurant']]}


wordVec = load("vectors.bin", 'bin')  # this load is from word2vec package

def computeFeatureVec(data):
#     featureVec =
    N = 0
    totalCounter = collections.Counter()

    for shopKey in data:
#         print "\n", shopKey
        reviewList = data[shopKey]  # each shop corresponds to a document
        N += 1  # number of documents
        flatReview = [word for review in reviewList for word in review]
#         print flatReview
        c = collections.Counter(flatReview)
        maxCnt = max(dict(c).values())
#         for key in totalCounter:
#             c[key] = 0.5 + 0.5 * c[key] / maxCnt
        totalCounter += c

#     print "totalCounter is", totalCounter
    for key in totalCounter:
        if totalCounter[key] < 10 or len(key) < 4:
            totalCounter[key] = 0
            continue
        cnt = 0
        for shopKey in data:
            if key in [a.lower() for a in  re.split(r'[ \']', shopKey[1])]:
                totalCounter[key] = 0
            reviewList = data[shopKey]
            flatReview = [word for review in reviewList for word in review]
            if key in flatReview:
                cnt += 1
#         print key, cnt
        totalCounter[key] *= math.log(N / cnt)

    d = dict(totalCounter)
    sortedDict = sorted(d.items(), key=lambda t: t[1], reverse=True)
#     print "TFIDF counter is ", sortedDict

    featureVec = []
    words = []
    i = 0
    cnt = 0
    foodVec = wordVec.get_vector('food')
    while(cnt < DIM):
        featureWord = sortedDict[i][0]
        i += 1
        if featureWord in wordVec.vocab:
            cnt += 1
#             print featureWord
            vec = wordVec.get_vector(featureWord)
            dist_with_food = np.sqrt(np.sum((vec - foodVec) ** 2))
            featureVec.append((dist_with_food, vec))
            words.append((dist_with_food, featureWord))

    featureVec = sorted(featureVec)
    words = sorted(words)
    for word in words:
        print word

    returnVec = np.array([])
    for x in featureVec:
        returnVec = np.append(returnVec, x[1])
    return returnVec


## Training for category 1
#b1_list = b1.items()
#size = len(b1_list)
#training_size = int(TRAINING_SET_RATIO * round(size))
#trainingSet1 = dict(b1_list[0:training_size])
#testingSet1 = b1_list[training_size:size]
#testingSet1List = zip(*[iter(testingSet1)] * int(round((size - training_size) / TESTING_SEGMENTS)))
#print "size of test=%d" % len(testingSet1List)
#featureVec1 = computeFeatureVec(trainingSet1)
#
## Training for category 2
#b2_list = b0.items()
#size = len(b2_list)
#training_size = int(TRAINING_SET_RATIO * round(size))
#trainingSet2 = dict(b2_list[0:training_size])
#testingSet2 = b2_list[training_size:size]
#testingSet2List = zip(*[iter(testingSet2)] * int(round((size - training_size) / TESTING_SEGMENTS)))
#print "size of test=%d" % len(testingSet2List)
#featureVec2 = computeFeatureVec(trainingSet2)
## print featureVec2.size
#
#
## Testing:
#wrong = 0
#correct = 0
#print "testing the Category 1:"
#for testing1 in testingSet1List:
#    featureVec = computeFeatureVec(dict(testing1))
#    dist1 = np.sqrt(np.sum((featureVec - featureVec1) ** 2))
#    dist2 = np.sqrt(np.sum((featureVec - featureVec2) ** 2))
#    if dist1 < dist2:
#        print "this is a Category 1, correct"
#        correct += 1
#    else:
#        print "this is a Category 2, wrong"
#        wrong += 1
#
#
#print "testing the Category 2:"
#for testing2 in testingSet2List:
#    featureVec = computeFeatureVec(dict(testing2))
#    dist1 = np.sqrt(np.sum((featureVec - featureVec1) ** 2))
#    dist2 = np.sqrt(np.sum((featureVec - featureVec2) ** 2))
#    if dist1 < dist2:
#        print "this is a Category 1, wrong"
#        wrong += 1
#    else:
#        print "this is a Category 2, correct"
#        correct += 1
#
#print "#correct =%d" % correct
#print "#wrong =%d" % wrong
#print "error rate=%f" % (float(correct) / (correct + wrong))
