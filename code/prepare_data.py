# coding: utf-8
from yelpDataExtractor import *
import codecs

# owner: rqi
# This file prepares data for our system.

#
# Print out all categories
#
def printCategories(yelp):
    for cat in yelp.businessTypes:
        print len(yelp.businessTypes[cat]), cat

# Print out all businessID and businessNames
def printBusinessNames(yelp):
    for bID, bName in businessList:
        if re.search(r'[Ff]rench', bName):
            print bID, bName

#
# Used when we were writing the proposal
# UNUSED.
def generateProposalData(yelp):
    cats= [['French', 'Restaurants'], ['Chinese', 'Restaurants'], ['Auto Parts & Supplies']]
    busis = [yelp.getBusinessByCategory(c) for c in cats]
    print 'after get business...'
    
    # Mapping from tuple (businessID, name, (categories)) to [reviews]
    targetCnt = 100 # 100 shops
    lowReview = 5
    upReview = 20
    for k in range(len(busis)):
        business = busis[k]
        reviewDict = {}
        cnt = 0
        for i in range(len(business)):
            b = business[i]
            reviews = yelp.getReviewTextByBusinessID(b[0])
            if len(reviews) > lowReview:# more than 5 reviews
                cnt += 1
                reviewDict[b] = [text2words(r['text']) for r in reviews[0:min(upReview,len(reviews)-1)]]
            if cnt >= targetCnt: break
        pickle.dump(reviewDict, open('business'+str(k)+'.dict', 'wb'))

#
# Generate tiny data set
# only generate data of 10 categories, 
#
def generateTinySet(yelp):
    businessList = []
    top10cats = ['Restaurants', 'Shopping', 'Food', 'Beauty & Spas', \
            'Nightlife', 'Bars', 'Health & Medical', 'Automotive', \
            'Home Services', 'Fashion']
    busiPerCat = 100
    busiSet = set()
    for cat in top10cats:
        cnt = 0
        for bID in yelp.getBusinessIDsByCategory(cat):
            if bID not in busiSet:
                b = yelp.getBusinessByID(bID)
                if b['review_count'] > 10:
                    businessList.append(b)
                    busiSet.add(bID)
                    cnt += 1
            if cnt == busiPerCat: break
    pickle.dump(businessList, open('top10cat_business.list', 'wb'))


def generateEmbeddingTrainingData(yelp):
    f = codecs.open("embedding_train_data.txt", "w", "utf-8-sig")
    for bID in yelp.reviews:
        print bID
        rList = yelp.reviews[bID]
        for r in rList:
            text = r['text']
            words = nltk.word_tokenize(text)
            for w in words:
                f.write(w+' ')
            f.write('\n')
    f.close()


if __name__ == "__main__":
    reviewFile = '../data/yelp_academic_dataset_review.json'
    businessFile = '../data/yelp_academic_dataset_business.json'
    yelp = YelpDataExtractor(businessFile, reviewFile)
    
    yelp.loadAllBusiness()
    yelp.loadAllReviews()
    yelp.addReviewsToBusiness()
    generateEmbeddingTrainingData(yelp)

    # generateTinySet(yelp)
   # printCategories(yelp)
