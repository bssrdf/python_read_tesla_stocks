import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
#from pandas.tseries import _converter
#_converter.register()

import numpy as np
from pandas import Timestamp
from pandas_datareader import data
import matplotlib.dates as mpl_dates
import matplotlib.ticker as mticker
#from mpl_finance import candlestick_ohlc
from mplfinance.original_flavor import candlestick_ohlc
from matplotlib import style
import datetime as dt
style.use('ggplot')
#style.use('fivethirtyeight')
#style.use('dark_background')

MA1=5
MA2=10





def moving_average(values,window):
	weights=np.repeat(1.0,window)/window
	smas=np.convolve(values,weights,'valid')
	return smas


def high_minus_low(highs,lows):
	return highs-lows

"""
highs=[11,12,15,14,13]
lows=[5,6,2,6,7]

h_l=list(map(high_minus_low,highs,lows))

print(h_l)
"""


def graph_data(stock):

	fig=plt.figure(figsize=(9,7),facecolor="#f0f0f0")
	ax1=plt.subplot2grid((6,1),(0,0),rowspan=1,colspan=1)
	plt.title(stock)
	plt.ylabel("H-L")
	ax2=plt.subplot2grid((6,1),(1,0),rowspan=4,colspan=1,sharex=ax1)
	plt.ylabel("Price")
	ax2v=ax2.twinx()
	plt.ylabel("Volume")
	ax3=plt.subplot2grid((6,1),(5,0),rowspan=1,colspan=1,sharex=ax1)
	plt.ylabel("MAVGs")
	
	start_date = '2020-09-01'
	end_date = '2021-01-20'


	panel = data.DataReader(str(stock), 'yahoo',
	start_date, end_date)
	#panel.set_index(panel['Date'],inplace=False)
	pd.options.display.float_format = "{:,.2f}".format
	print(panel.head())
	
	panel.reset_index(inplace=True)
	print(panel.head(40))
	
	df = panel.iloc[-1:]
	print('close at: ', df['Close'])
	print('close date: ',df['Date'])
	
	
	total =len(panel.index)
	print(total)
	print(panel['Close'][total-1])
	print(panel['Date'][total-1])
	
	
	ma1=moving_average(panel['Close'],MA1)
	ma2=moving_average(panel['Close'],MA2)
	
	
	ohlc = panel.loc[:, ['Date', 'Open', 'High', 'Low', 
	'Close']]
	#ohlc['Date'] = pd.to_datetime(ohlc['Date'])
	ohlc['Date'] = ohlc['Date'].apply(mpl_dates.date2num)
	ohlc = ohlc.astype(float)
	
	#panel['Date']=panel['Date'].astype('datetime64[ns]')
	panel['Date'] = panel['Date'].apply(mpl_dates.date2num)
	
	candlestick_ohlc(ax2, ohlc.values, width=0.6,
	colorup='green', colordown='red', alpha=0.8)
	
	#ax1.plot(panel['Date'],panel['Close'])
	#ax1.plot(panel['Date'],panel['Open'])
	
	
	#for label in ax1.xaxis.get_ticklabels():
	#	label.set_rotation(45)
	
	"""
	ax2.annotate("{:.2f}".format(panel['Close'][total-1]),
	(panel['Date'][total-1].to_pydatetime(),
	panel['Close'][total-1]),xytext=(
	panel['Date'][total-1].to_pydatetime(),panel['Close'][total-1]))
	
	"""
	"""
	ax2.annotate('Big news',
	(panel['Date'][2].to_pydatetime(),panel['Close'][5]),
	xytext=(0.8,0.9),textcoords="axes fraction",
	arrowprops=dict(facecolor='grey',color='grey'))
	
	
	font_dict={'family':'serif','color':'darkred',
			'size':15}
	ax2.text(dt.date(2020,10,12), panel['Close'][1], "!!!",
			fontdict=font_dict)

	ax2.text(panel['Date'][2],
	panel['Close'][1], "!!!",fontdict=font_dict)
	"""
	start2=len(ma2)
	#ax2v.plot([],[],color='#0079a3',alpha=0.4,label='Volume')
	ax2v.plot(panel['Date'].values[-start2:],panel['Volume'][-start2:],color='#0079a3',alpha=0.4,label='Volume')
	ax2v.fill_between(panel['Date'].values[-start2:],0,panel['Volume'][-start2:],
	facecolor="#0079a3",alpha=0.3)
	#ax2v.axes.yaxis.set_ticklabels([])
	ax2v.grid(False)
	ax2v.set_ylim(0,3*panel['Volume'].max())
	
	start=len(['Close'][MA1:])
	start1=len(ma1)
			
	print(start1,'***')
	print(start2)
	print(len(panel['Date']),len(ma1))
	print(len(panel['Date']),len(ma2))
	ax3.plot(panel['Date'].values[-start2:],ma1[-start2:],linewidth=1,label=(str(MA1)+'MA'))
	ax3.plot(panel['Date'].values[-start2:],ma2[-start2:],linewidth=1,label=(str(MA2)+'MA'))
	ax3.fill_between(panel['Date'].values[-start2:],ma2[-start2:],
	ma1[-start2:],where=(ma1[-start2:]<ma2[-start2:]),
	facecolor='r',edgecolor='r',alpha=0.5)

	ax3.fill_between(panel['Date'].values[-start2:],ma2[-start2:],
	ma1[-start2:],where=(ma1[-start2:]>ma2[-start2:]),
	facecolor='g',edgecolor='g',alpha=0.5)
	ax3.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5,prune=
	'upper'))
	
	#date_format = mpl_dates.DateFormatter('%d-%m-%Y')
	#ax1.xaxis.set_major_formatter(date_format)
	#ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
	#ax1.grid(True)

	h_l=list(map(high_minus_low,panel['High'],panel['Low']))
	ax1.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5,prune=
	'upper'))
	ax1.plot(panel['Date'].values,np.array(h_l),label='H-L')
	#ax1.plot(mpl_dates.date2num(panel['Date'].values),np.array(h_l),label='H-L')

	date_format = mpl_dates.DateFormatter('%m-%d-%Y')
	ax1.xaxis.set_major_formatter(date_format)
	ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
	ax1.grid(True)

	plt.setp(ax3.get_xticklabels(), rotation=45)
	plt.setp(ax1.get_xticklabels(), visible=False)
	plt.setp(ax2.get_xticklabels(), visible=False)
	
		
	plt.subplots_adjust(left=0.09,bottom=0.17,right=0.94,
	top=0.92,wspace=0.2,hspace=0)
	
	#plt.title(stock)
	
	ax1.legend()
	leg=ax1.legend(loc=9,ncol=2,prop={'size':11})
	leg.get_frame().set_alpha(0.4)
	
	ax2v.legend()
	leg=ax2v.legend(loc=9,ncol=2,prop={'size':11})
	leg.get_frame().set_alpha(0.4)
	
	ax3.legend()
	leg=ax3.legend(loc=9,ncol=2,prop={'size':11})
	leg.get_frame().set_alpha(0.4)
	
	
	plt.show()
	

graph_data('TSLA')

