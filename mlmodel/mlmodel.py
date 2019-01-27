'''
__author__ = "HexaByte"
'''


import numpy as np
import pandas as pd

from sklearn.externals import joblib


from sklearn.ensemble import RandomForestClassifier



class Models(object):
	"""Class for Machine learning Models"""
	def __init__(self):
		pass

	def randomForest(self, X,y, n_estimators=10, criterion='gini',
			max_depth=None, max_features='auto', min_impurity_decrease=0.0,
			verbose=1,saveModel=False):
		"""
		Method to return trained random forest model

		args:
			X,y: Features and Labels,
			n_estimators=10: n decision trees, 
			criterion='gini' or 'entropy': parameter for quality of split ,

			max_depth=None : maximum depth of the trees, 
			max_features='auto' : max features to consider for best split, 

			min_impurity_decrease=0.0 : A node will be split if this split induces a 
										decrease of the impurity greater than or equal to this value.,

			verbose=1 : control messages while training and testing, set to 0 to turn off messages
			saveModel=False : boolean to save model using joblib (if true saves model in current dir)
		
		"""

		clf = RandomForestClassifier(n_estimators=n_estimators, criterion=criterion,
			max_depth=max_depth, max_features=max_features,
			min_impurity_decrease=min_impurity_decrease,
			verbose=verbose)
			

		clf.fit(X,y)

		if saveModel:
			joblib.dump(clf,"trained_random_forest")

		return clf