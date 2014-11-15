import baseline
import cPickle as pickle

# owner: rqi
# This file tests our extractor by measuring its performace on
# capturing sample similarities in terms of category, score etc.

############################################
# Read in training and test data..
b0 = pickle.load(open('business0.dict', 'rb'))  # French
b1 = pickle.load(open('business1.dict', 'rb'))  # chinese
b2 = pickle.load(open('business2.dict', 'rb'))  # auto

FrenchData = {"shop1":[review.split() for review in r11], "shop2":[review.split() for review in r12]}
AutoData = {"Auto1":[review.split() for review in r21], "Auto2":[review.split() for review in r22]}
wordVec = load("vectors.bin", 'bin')  # this load is from word2vec package

b1_list = b1.items()
size = len(b1_list)
training_size = int(TRAINING_SET_RATIO * round(size))
trainingSet1 = dict(b1_list[0:training_size])
testingSet1 = b1_list[training_size:size]
testingSet1List = zip(*[iter(testingSet1)] * int(round((size - training_size) / TESTING_SEGMENTS)))
print "size of test=%d" % len(testingSet1List)

b2_list = b0.items()
size = len(b2_list)
training_size = int(TRAINING_SET_RATIO * round(size))
trainingSet2 = dict(b2_list[0:training_size])
testingSet2 = b2_list[training_size:size]
testingSet2List = zip(*[iter(testingSet2)] * int(round((size - training_size) / TESTING_SEGMENTS)))
print "size of test=%d" % len(testingSet2List)


##########################################
# Train the model
trainingData = (trainingSet1, trainingSet2)
baselineExtractor = baseline()
baseline.train(trainingData)


##########################################
# Test the model
for testing1 in testingSet1List:
    ret = baseline.extract(testing1)
    if ret == 1:
        print "this is a Category 1, correct"
    else:
        print "this is a Category 2, wrong"
    

for testing2 in testingSet2List:
    ret = baseline.extract(testing2)
    if ret == 1:
        print "this is a Category 1, wrong"
    else:
        print "this is a Category 2, correct"


#cost = 0.0
#for d1 in testData:
#    for d2 in testData:
#        if d1 == d2: continue
#        s1 = baseline.extractSignature(d1)
#        s2 = baseline.extractSignature(d2)
#        cost += evalCategory(s1, s2)

print cost
