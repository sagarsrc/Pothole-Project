"""
__author__ = "HexaByte"
"""

from plotly import tools
from plotly.offline import download_plotlyjs,init_notebook_mode,iplot,plot
import plotly.graph_objs as go
init_notebook_mode(connected=True)



class Graph(object):
	"""Plot various Graphs"""
	def __init__(self):
		pass

	

	def plot_g_a(self,df):
		"""
		Plot Gyroscope and Accelerometer data
		args:
			df : pandas DataFrame with columns (Timestamp,Gx,Gy,Gz,Ax,Ay,Az)
		returns:
			iplot
		"""
		t = df['Timestamp']
		gx,gy,gz = df['Gx'],df['Gy'],df['Gz']
		ax,ay,az = df['Ax'],df['Ay'],df['Az']
		
		# gyro plot
		gx = go.Scatter(
			x= t,
			y= gx,
			name='gx'
		)
		gy = go.Scatter(
			x= t,
			y= gy,
			name='gy'
		)
		gz = go.Scatter(
			x= t,
			y= gz,
			name='gz'
		)

		# acc plot
		ax = go.Scatter(
				x= t,
				y= ax,
				name='ax'
			)
		ay = go.Scatter(
			x= t,
			y= ay,
			name='ay'
		)
		az = go.Scatter(
			x= t,
			y= az,
			name='az'
		)
		
		fig = tools.make_subplots(rows=3,cols=2,shared_xaxes=True)
		
		fig.append_trace(gx, 1, 1)
		fig.append_trace(gy, 2, 1)
		fig.append_trace(gz, 3, 1)
		
		fig.append_trace(ax, 1, 2)
		fig.append_trace(ay, 2, 2)
		fig.append_trace(az, 3, 2)
		
		fig['layout'].update(height=600, width=800,
						 title='Gyroscope and Accelerometer data plot')
		
		return iplot(fig)
			
