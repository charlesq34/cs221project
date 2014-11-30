import sys, collections, math, re
import cPickle as pickle
from  word2vec import *
import numpy as np

# # DIM = 30 for b1 and b2: 90% correct
# # DIM = 20 for b0 and b1: 70% correct
DIM = 50  # how many word to extract into vectors
DIM_vec = 10
# TRAINING_SET_RATIO = 0.6  # 40% hold out rate
# TESTING_SEGMENTS = 10
#
# b0 = pickle.load(open('business0.dict', 'rb'))  # French
# b1 = pickle.load(open('business1.dict', 'rb'))  # chinese
# b2 = pickle.load(open('business2.dict', 'rb'))  # auto
#
# wordVec = load("vectors.bin", 'bin')  # this load is from word2vec package
wordVec = load("vectorsstnn_review.bin", 'bin')  # this load is from word2vec package
#
# # {'shop2': [['nice', 'food'], ['french', 'fries']], 'shop1': [['french', 'restaurant'], ['good', 'restaurant']]}


# wordVec = load("vectors.bin", 'bin')  # this load is from word2vec package

def computeFeatureVec_single_biz(reviewList):
    N = 0
    flatReview = [word for review in reviewList for word in review]
    # TF
    totalCounter = collections.Counter(flatReview)
    # IDF
    N = len(reviewList)
    for key in totalCounter:
        if totalCounter[key] < 2 or len(key) < 4 or key in ['food', 'good', 'I', 'the', 'it', 'service', 'food', 'staff', 'restaurant', 'atmosphere', 'people']:
            totalCounter[key] = 0
            continue
        cnt = 0
        for review in reviewList:
            if key in review:
                cnt += 1
        totalCounter[key] *= math.log(N / cnt)
    # sort
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
        try:
            featureWord = str(featureWord)
        except:
            continue
        blackList = ['food', 'good', 'I', 'the', 'it', 'service', 'food', 'staff', 'restaurant', 'atmosphere', 'people', 'great', 'large', 'small', 'tasty', 'drink']
        if featureWord in wordVec.vocab and featureWord not in blackList:
            cnt += 1
#           print featureWord
            vec = wordVec.get_vector(featureWord)
            dist_with_food = np.sqrt(np.sum((vec - foodVec) ** 2))
            featureVec.append((dist_with_food, vec))
            words.append((dist_with_food, featureWord))

#   featureVec = sorted(featureVec)
    words = sorted(words)

    returnVec = []
    for i in range(DIM_vec) :
        print words[i]
        returnVec.append(featureVec[i][1])
    return returnVec





'''

def computeFeatureVec(data):
    N = 0
    totalCounter = collections.Counter()
    for shopKey in data:
        print "\n", shopKey
        reviewList = data[shopKey]  # each shop corresponds to a document
        N += 1  # number of documents
        flatReview = [word for review in reviewList for word in review]
#         print flatReview
        c = collections.Counter(flatReview)
#         maxCnt = max(dict(c).values())
#         for key in totalCounter:
#             c[key] = 0.5 + 0.5 * c[key] / maxCnt
        totalCounter += c

#     print "totalCounter is", totalCounter
    for key in totalCounter:
        if totalCounter[key] < 10 or len(key) < 4 or key in ['food', 'good']:
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
    print "TFIDF counter is ", sortedDict

    featureVec = []
    words = []
    i = 0
    cnt = 0
    foodVec = wordVec.get_vector('food')
    while(cnt < DIM):
        featureWord = sortedDict[i][0]
        i += 1
        print featureWord
        if featureWord in wordVec.vocab:
            cnt += 1
            print featureWord
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





'''










