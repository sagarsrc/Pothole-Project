"""
___author___ = "HexaByte"
"""


import pandas as pd
import numpy as np
import os


class LoadData(object):
	"""Class for loading data LoadData."""
	def __init__(self):
		pass

	def loadData(self,folder_name='plain_road_potholes'):
		"""
		Method for loading Data from folder
		args:
			folder_name : name of folder in data folder
		return:
			DataFrame of all csv files
		"""

		try:
			path = '../data/'+folder_name+'/'
			os.chdir(path)
		except Exception as e:
			if e:
				path = './data/'+folder_name+'/'
				os.chdir(path)


		print(path)

		l_ = os.listdir()
		print(l_)
		df = pd.DataFrame(columns=['Time','Gx','Gy','Gz','Ax','Ay','Az'])
		for i in l_:
			temp = pd.read_csv(i)
			# print(temp)
			df = pd.concat([df,temp],axis=0)

		try:
			os.chdir('../../LoadData/')
		except Exception as e:
			if e:
				os.chdir('../../')


		a = np.arange(0.,df.shape[0],0.001)
		a = a[0:df.shape[0]]
		df['Time']=a

		return df
