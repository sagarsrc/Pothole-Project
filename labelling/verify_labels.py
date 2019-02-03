'''
__author__ = "HexaByte"
'''

import pandas as pd
import numpy as np

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



	def verify_vertical_limits(self,df,col_name, ev_vals_df,sample_index,vlimits):
		"""
		Verify vertical limits
		args:
			df : pandas DataFrame with columns (Timestamp,Gx,Gy,Gz,Ax,Ay,Az)
			col_name : column which needs to be verified
			ev_vals_df : event and value dataframe consisting downsampled 
			sample_index : index values of samples (int __NOT datetime__)
			vlimits : dataframe of vertical limits with event and values
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
		
		vlims_time_index = t.searchsorted(value=vlimits['event'])
		# print(vlims_time_index)
		# print(df.iloc[vlims_time_index])
		vlims_df = df.iloc[vlims_time_index]
		
		limits = go.Bar(
		   
			x = vlims_df['Time'],
			# 60. is height of the barrier
			y = np.array([60.]*vlims_df.shape[0]),
			name='Vertical Barrier',
			
			width=0.0002,
			marker=dict(
				color='rgb(255,0,0)',
			)
			
		)

		data = [Signal,Samples,limits]
		fig = go.Figure(data=data)

		return iplot(fig)


	def verify_horizontal_limits(self,df,col_name, ev_vals_df,sample_index,vlimits,hlimits):
		"""
		Verify horizontal limits
		args:
			df : pandas DataFrame with columns (Timestamp,Gx,Gy,Gz,Ax,Ay,Az)
			col_name : column which needs to be verified
			ev_vals_df : event and value dataframe consisting downsampled 
			sample_index : index values of samples (int __NOT datetime__)
			
			vlimits : dataframe of vertical limits with event and values
			hlimits : (tuple) horizontal limits 

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

		vlims_time_index = t.searchsorted(value=vlimits['event'])
		# print(vlims_time_index)
		# print(df.iloc[vlims_time_index])
		vlims_df = df.iloc[vlims_time_index]

		limits = go.Bar(

			x = vlims_df['Time'],
			# 60. is height of the barrier
			y = np.array([60.]*vlims_df.shape[0]),
			name='Vertical Barrier',

			width=0.0002,
			marker=dict(
				color='rgb(255,0,0)',
			)

		)
		
		hor_bars = go.Scatter(
			x = df['Time'],
			y = np.array([hlimits[0]]*df.shape[0]),
			mode = 'lines',
			name='h_up'
		)
		
		lor_bars = go.Scatter(
			x = df['Time'],
			y = np.array([hlimits[1]]*df.shape[0]),
			mode = 'lines',
			name='h_dn'
		)
		

		data = [Signal,Samples,limits,hor_bars,lor_bars]
		fig = go.Figure(data=data)

		return iplot(fig)



	def verify_labels(self,df,col_name, labelled_ev_vals_df,sample_index,vlimits,hlimits):
		"""
		Verify labels
		args:
			df : pandas DataFrame with columns (Timestamp,Gx,Gy,Gz,Ax,Ay,Az)
			col_name : column which needs to be verified
			ev_vals_df : event and value dataframe consisting downsampled 
			sample_index : downsampled data index values of samples (float __NOT datetime__)

			vlimits : dataframe of vertical limits with event and values
			hlimits : (tuple) horizontal limits 

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
		# sample_df = df.iloc[result]

		a = labelled_ev_vals_df['label'].unique()

		label1X = labelled_ev_vals_df[labelled_ev_vals_df['label']==a[1]]['event']
		label1Y = labelled_ev_vals_df[labelled_ev_vals_df['label']==a[1]]['value']
		
		label0X = labelled_ev_vals_df[labelled_ev_vals_df['label']==a[0]]['event']
		label0Y = labelled_ev_vals_df[labelled_ev_vals_df['label']==a[0]]['value']
		
		
		lb1 = go.Scatter(
			x = label1X,
			y = label1Y,
			name = 'lb1',
			mode = 'markers'
		)
		
		lb0 = go.Scatter(
			x = label0X,
			y = label0Y,
			name = 'lb0',
			mode = 'markers'
		)

		vlims_time_index = t.searchsorted(value=vlimits['event'])
		# print(vlims_time_index)
		# print(df.iloc[vlims_time_index])
		vlims_df = df.iloc[vlims_time_index]

		limits = go.Bar(

			x = vlims_df['Time'],
			# 60. is height of the barrier
			y = np.array([60.]*vlims_df.shape[0]),
			name='Vertical Barrier',

			width=0.0002,
			marker=dict(
				color='rgb(255,0,0)',
			)

		)

		hor_bars = go.Scatter(
			x = df['Time'],
			y = np.array([hlimits[0]]*df.shape[0]),
			mode = 'lines',
			name='h_up'
		)

		lor_bars = go.Scatter(
			x = df['Time'],
			y = np.array([hlimits[1]]*df.shape[0]),
			mode = 'lines',
			name='h_dn'
		)
		
		

		data = [Signal,lb0,lb1,limits,hor_bars,lor_bars]
		fig = go.Figure(data=data)

		return iplot(fig)
