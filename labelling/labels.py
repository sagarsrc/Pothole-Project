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
			sNeg, sPos = min(0,sNeg+diff[i]),max(0,sPos+diff[i])
			
			# print(-1*sNeg,",",sPos,",",thold)
			
			# if sum negative greater than -ve threshold sample point
			if sNeg<-thold:
				sNeg = 0;
				Events.append(i)

			# if sum positive greater than +ve threshold sample point
			elif sPos>thold:
				sPos = 0;
				Events.append(i)

		vals = []
		for i in Events:
			t = df[df.index==i]
			vals.append(t[col_name].values[0])

		
		df_res = pd.DataFrame({
			'event':Events,
			'value':vals
			})
		return df_res