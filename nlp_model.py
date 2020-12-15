#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 13:32:28 2018

@author: deola
"""


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.utils import shuffle
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import pickle


data=pd.read_excel("/home/deola/Documents/Gustav/Gustav1.xlsx")
#data=shuffle(data)

data=pd.DataFrame(data)
#print data
data.to_excel("/home/deola/Documents/Gustav/Gustav2.xlsx", index=False)

X_train, X_test, y_train, y_test = train_test_split(data["name"], data["Display Name"], random_state = 27, test_size=0.20)
#y_train=np.array(y_train)
vect = CountVectorizer(analyzer="char",
                             lowercase=True,
                             max_features=None,
                             ngram_range=(1, 3))
                             
X_train_counts= vect.fit_transform(data['name'])
X_train_count = vect.transform(X_train)
X_test_count =  vect.transform(X_test)
#print(X_train_count)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_count)
X_test_tfidf = tfidf_transformer.fit_transform(X_test_count)
#print(X_train_tfidf)
model= MultinomialNB(alpha=0.9, fit_prior=True)
model.fit(X_train_tfidf, y_train)



pickle.dump(model, open("/home/deola/Documents/Gustav/vector.pickel", "wb"))

nameModel = pickle.load(open("/home/deola/Documents/Gustav/vector.pickel", "rb"))

sample=vect.transform(X_test)

pred=nameModel.predict(sample)
print [a for a in pred]
print y_test
print(precision_score(pred, y_test))
#print(f1_score(pred, y_test))
print(recall_score(pred, y_test))
