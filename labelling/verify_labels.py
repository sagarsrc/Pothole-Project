'''
__author__ = "HexaByte"
'''

import pandas as pd


# plotly modules
from plotly import tools
from plotly.offline import download_plotlyjs,init_notebook_mode,iplot,plot
import plotly.graph_objs as go
init_notebook_mode(connected=True)


class VerifyLabels(object):
	"""Class for Verifying Labels and samples"""
	def __init__(self):
		pass

	
	def verify_samples(self,df,col_name,sample_index):
		"""
		Verify downsampled points
		args:
			df : pandas DataFrame with columns (Timestamp,Gx,Gy,Gz,Ax,Ay,Az)
			col_name : column which needs to be verified
			sample_index : index values of samples (int __NOT datetime__)
		returns:
			plot of samples and downsampled points
		"""
		t = df['Time']
		y_whole = df[col_name]
		# print(t)
		Signal = go.Scatter(
			x= t,
			y= y_whole,
			name='signal',
			mode='lines'
		)
		
		result = t.searchsorted(value = sample_index)
		# print(result)
		
		# print(df.iloc[result])
		
		sample_df = df.iloc[result]
		
		Samples = go.Scatter(
			x = sample_df['Time'],
			y= sample_df[col_name],
			name='samples',
			mode='markers'
		)


		data = [Signal,Samples]
		fig = go.Figure(data=data)

		return iplot(fig)
