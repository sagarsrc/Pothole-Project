'''
__author__ = "HexaByte"
'''

import pandas as pd

class Labels(object):
	"""Class for creating Labels"""
	def __init__(self):
		pass


	def cusum_filter(self,df,thold,col_name):
		"""
		Symmetric Cusum filter
		args:
			df: pandas dataframe
			thold: thold to sample point (mean of vector)
			col_name: name of column to be downsampled (eg: Ax, Ay,..Gz etc)
		returns:
			DataFrame of 
			Events (list): index (int) of events marked 
			vals (list) : values (float) of column 
		"""

		print("Threshold : ", thold)
		Events, sNeg, sPos = [], 0, 0

		# calculate consecutive differences
		diff = df[col_name].diff()

		
		for i in range(1,df.shape[0]):
			sNeg, sPos = min(0,sNeg+diff.iloc[i]),max(0,sPos+diff.iloc[i])


			# if sum negative greater than -ve threshold sample point
			if sNeg<-thold:
				sNeg = 0;
				Events.append(df.iloc[i,:]['Time'])
				# print(df.iloc[i,:]['Time'])
			# if sum positive greater than +ve threshold sample point
			elif sPos>thold:
				sPos = 0;
				Events.append(df.iloc[i,:]['Time'])

		# print(Events)
		
		vals = []
		for i in Events:
			t = df[df.Time==i][col_name].values[0]
			# print(t)
			vals.append(t)

		# print(len(vals),len)
		df_res = pd.DataFrame({
			'event':Events,
			'value':vals
			})
		
		return df_res