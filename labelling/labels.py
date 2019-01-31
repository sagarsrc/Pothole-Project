'''
__author__ = "HexaByte"
'''

import pandas as pd
import numpy as np

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



	def set_vertical_limits(self,df):
		"""
		Get vertical limits for downsampled dataframe
		args:
			df : downsampled dataframe with columns(event,value)
		return:
			vlimits : DataFrame starting point of vertical barrier as event column
		"""
		ev = df.copy(deep=True)
		dif = ev['event'].diff()
		dif = dif[1:]
		mean_window_size = dif.mean()

		print("Window size : ",mean_window_size)
		
		s = 0
		l = []
		for x,i in enumerate(dif,1):
			# print(x,i)
			s+=i
			if s >= mean_window_size:
				l.append(x)
				s=0
		 #print(l)
		return ev.iloc[l]



		
	def set_horizontal_limits(self,df):
		"""
		Get horizontal limits for downsampled dataframe
		args:
			df : downsampled dataframe with columns(event,value)
		return:
			hlimits : tuples of (h_up,h_dn)
		"""
		hlimits_val = df['value'].mean()
		print("hlimit_val (mean of all 'value' in downsampled points) = ",hlimits_val)

		print("zero =",df.loc[0,'value'])

		# set h_up and h_dn
		h_up = df.loc[0,'value']+hlimits_val
		h_dn = np.absolute(df.loc[0,'value']-hlimits_val)

		# tuple hlimits
		hlimits = (h_up,h_dn)
		print("h_up,h_dn = ",hlimits)
		
		return hlimits




	def get_thold_pts(self,df,hlimits):
		"""
		Get dataframe of all points which have crossed threshold h_up and h_dn
		args:
			df : DataFrame with event and value columns (Downsampled dataframe)
			hlimits : tuple (h_up,h_dn)
		return:
			thold_pts : dataframe 
		"""
		h_up,h_dn = hlimits
		h_up_points = df[df['value']>h_up]
		h_dn_points = df[df['value']<h_dn]
		thold_pts =h_up_points.append(h_dn_points,ignore_index=False)
		
		return thold_pts



	def get_mean_thold(self,df,thold_pts):
		"""
		Get mean threshold percentage to identify window to label
		args:
			df: downsampled dataframe
			thold_pts : dataframe of all points which have crossed threshold h_up and h_dn
		returns:
			mean threshold percentage
		"""
		ix = thold_pts.index.values
		
		l = []
		
		for i in range(ix.shape[0]-1):
			# print(ix[i],ix[i+1])
			temp_vals = df.iloc[ix[i]:ix[i+1],:]
			# print(temp_vals)

			# print(temp_vals.isin(thold_pts))
			win_tf = temp_vals.isin(thold_pts)

			# print(win_tf['value'].value_counts())
			try:
				f,t = win_tf['value'].value_counts(sort=False)
			except:
				t = 0
			v = (t/(t+f))*100

			l.append(v)

		mean_thold_percent = np.array(l).mean()
		print("Mean threshold % ",mean_thold_percent)
		return mean_thold_percent




	def get_labels(self,df,thold_pts,label=1):
		"""
		get labels for downsampled data
		args:
			df : dataframe of downsampled points
			thold_pts : dataframe of points which have crossed h_up,h_dn
		returns:
			labels to downsampled dataframe
		"""
		
		labels_df = pd.DataFrame(columns=['event','value','label'])
		s = 0
		# call get_mean_thold
		mean_thold_percent = self.get_mean_thold(df,thold_pts)
		
		ix = thold_pts.index.values

		for i in range(ix.shape[0]-1):
			# print(ix[i],ix[i+1])
			temp_vals = df.iloc[ix[i]:ix[i+1],:]

			win_tf = temp_vals.isin(thold_pts)

			try:
				f,t = win_tf['value'].value_counts(sort=False)
			except:
				t = 0
			v = (t/(t+f))*100

			if v>mean_thold_percent:
				# s+=temp_vals.shape[0]
				# print("True",s)
				ev = temp_vals['event']
				vl = temp_vals['value']
				lb = np.ones(temp_vals.shape[0])

				temp_df = pd.DataFrame({
					'event':ev,
					'value':vl,
					'label':lb
				})

				labels_df = pd.concat([labels_df,temp_df])

		labels_df.head()       

		df['label'] = np.zeros(df.shape[0])
		df.head()

		df.iloc[labels_df.index,-1] = label
		return df
