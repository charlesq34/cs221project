# coding: utf-8
import json
import re
import random
import cPickle as pickle
import os.path
import nltk
import string


# owner: rqi
# This file defines a class to extract useful data from Yelp data set.
# Please put yelp data set in ../data/
# Yelp Dataset: https://www.yelp.com/dataset_challenge/dataset

class YelpDataExtractor():
    def __init__(self, businessFile, reviewFile):
        self.businessFile = businessFile
        self.reviewFile = reviewFile
        self.businessCategoryDict = {} # cat -> list of bIDs
        self.businessDict = {} # bID -> list of business
        self.reviews = {} # bID -> list of reviews

    # Load a list of all business names and ID tuple
    # Note: this function also LOG business infos.
    def loadAllBusiness(self):
        for line in open(self.businessFile):
            b = json.loads(line)
            bID = b['business_id']

            for cat in b['categories']:
                if cat not in self.businessCategoryDict:
                    self.businessCategoryDict[cat] = []
                else:
                    self.businessCategoryDict[cat].append(bID)

            self.businessDict[bID] = b

    def loadAllReviews(self):
        for line in open(self.reviewFile):
            r = json.loads(line)
            bID = r['business_id']

            if bID not in self.reviews:
                self.reviews[bID] = [r]
            else:
                self.reviews[bID].append(r)

    # Add all reviews related with a business to that business' dict.
    # Note: len(self.reviews[bID]) may not be the same as b['review_count']
    def addReviewsToBusiness(self):
        for bID in self.businessDict:
            b = self.businessDict[bID]
            if bID in self.reviews:
                b['reviews'] = self.reviews[bID]
                b['review_count'] = len(self.reviews[bID])


    def getBusinessIDsByCategory(self, cat):
        if cat in self.businessCategoryDict:
            return self.businessCategoryDict[cat]
        else:
            return null


    def getBusinessByID(self, bID):
        return self.businessDict[bID]

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

