# coding: utf-8
import json
import re
import random
import cPickle as pickle
import os.path
import nltk
import string

# Put yelp data set in ../data/
# Yelp Dataset: https://www.yelp.com/dataset_challenge/dataset

class YelpDataExtractor():
    def __init__(self, businessFile, reviewFile):
        self.businessFile = businessFile
        self.reviewFile = reviewFile
        self.businessTypes = set()
        self.business = []
        self.reviews = {}

    # Load a list of all business names and ID tuple
    # Note: this function also LOG business infos.
    def loadAllBusiness(self):
        if False: #os.path.isfile('yelp_busi.dict'):
            self.business = pickle.load( open('yelp_busi.dict','rb'))
        else:
            businessList = []
            for line in open(self.businessFile):
                b = json.loads(line)
                businessList.append((b['business_id'], b['name']))
                for cat in b['categories']:
                    if cat not in self.businessTypes:
                        self.businessTypes.add(cat)
                self.business.append(b)
            #pickle.dump(self.business, open('yelp_busi.dict','wb'))

    def loadAllReviews(self):
        if False: #os.path.isfile('yelp_review.dict'):
            self.reviews = pickle.load( open('yelp_review.dict','rb'))
        else:
            for line in open(self.reviewFile):
                r = json.loads(line)
                bID = r['business_id'] 
                if bID not in self.reviews:
                    self.reviews[bID] = [r]
                else:
                    self.reviews[bID].append(r)
            #pickle.dump(self.reviews, open('yelp_review.dict','wb'))

    # Return a list of business ID and businessName tuples
    # where business belong to specified category
    def getBusinessByCategory(self, categories):
        businessList = []
        for b in self.business:
            cats = b['categories']
            catMatchNum = sum([int(categories[i] in cats) for i in range(len(categories))])
            if catMatchNum == len(categories):
                businessList.append((b['business_id'],\
                    b['name'], tuple(categories)))
        return businessList

    # Return a list of reviews, each is a dict of review
    def getReviewTextByBusinessID(self, businessID):
        return self.reviews[businessID]

# Input a text string, output a list of words from the text
def text2words(text):
    words = nltk.word_tokenize(text)
    words = [w.lower() for w in words if w not in string.punctuation]
    return [w for w in words if w not in nltk.corpus.stopwords.words('english')]

if __name__ == "__main__":
    reviewFile = '../data/yelp_academic_dataset_review.json'
    businessFile = '../data/yelp_academic_dataset_business.json'
    yelp = YelpDataExtractor(businessFile, reviewFile)
    
    #businessID = 'vcNAWiLM4dR7D2nwwJ7nCA'
    #reviews = yelp.getReviewsByBusinessID(businessID, 10)
    
    yelp.loadAllBusiness()
    yelp.loadAllReviews()
    print 'loading finishes...'
    
    #for bID, bName in businessList:
    #    if re.search(r'[Ff]rench', bName):
    #        print bID, bName
    
    cat1 = ['French', 'Restaurants']
    cat2 = ['Auto Parts & Supplies']
    business1 = yelp.getBusinessByCategory(cat1)
    business2 = yelp.getBusinessByCategory(cat2)
    print 'after get business...'

    # sampleSize = 20 # get 20 business for each cat
    # businessSample1 = random.sample(business1, sampleSize)
    # businessSample2 = random.sample(business2, sampleSize)
    # for k in range(20):
    #     print businessSample1[k]
    # for k in range(20):
    #     print businessSample2[k]
    
    
    # Mapping from tuple (businessID, name, (categories)) to [reviews]
    reviewDict1 = {}
    cnt = 0
    targetCnt = 20 # 10 shops
    for i in range(len(business1)):
        b = business1[i]
        print b
        reviews = yelp.getReviewTextByBusinessID(b[0])
        if len(reviews) > 5:# more than 5 reviews
            cnt += 1
            reviewDict1[b] = [text2words(r['text']) for r in reviews[0:min(19,len(reviews)-1)]]
            print b, len(reviewDict1[b])
        if cnt >= targetCnt: break
    pickle.dump(reviewDict1, open('business1.dict', 'wb'))
    
    cnt = 0
    reviewDict2 = {}
    for i in range(len(business2)):
        b = business2[i]
        print b
        reviews = yelp.getReviewTextByBusinessID(b[0])
        if len(reviews) > 5:# more than 5 reviews
            cnt += 1
            reviewDict2[b] = [text2words(r['text']) for r in reviews[0:min(19,len(reviews)-1)]]
            print b, len(reviewDict2[b])
        if cnt >= targetCnt: break
    pickle.dump(reviewDict2, open('business2.dict', 'wb'))
    
    
    #print len(reviewDict1)
    #test = pickle.load( open('business1.dict', 'rb') )
    #print len(test)

