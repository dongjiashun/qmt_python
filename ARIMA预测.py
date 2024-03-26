#encoding:gbk
# close_5 �ǽ�������̼ۣ�close_predict5������ǰԤ��Ľ�������̼ۣ�Ԥ��ʧ����ȡ����ǰ�����̼�

import pandas as pd
import numpy as np
import statsmodels.api as sm
import warnings


def init(ContextInfo):
	print('init��ʼ�趨����,���趨��ֱ��pass')
	warnings.filterwarnings('ignore')
	pass

def handlebar(ContextInfo):
	#handlebar ���K�ߵ������к���

	#��ǰK�ߵĶ�Ӧ���±��0��ʼ
	index = ContextInfo.barpos
	print(index)
	if index < 250:
		return
	#��ǰK�߶�Ӧ��ʱ�䣺����
	realtime = ContextInfo.get_bar_timetag(index)
	
	#����ǰ����
	date_5 = timetag_to_datetime(ContextInfo.get_bar_timetag(index-5),"%Y%m%d")
	#��ǰ����
	period = ContextInfo.period
	
	#��ǰ��ͼ��Ȩ��ʽ
	dividend_type = ContextInfo.dividend_type
	
	#ȡ��ǰK��ͼ��Ӧ�ĺ�Լ��ǰK�ߵĵ�ǰ��ͼ��Ȩ��ʽ�µ����̼�
	close = ContextInfo.get_market_data(['close'],period=period,dividend_type=dividend_type,count=240)

	
	try: 
		closedata = np.array(close.diff(periods=3)["close"]) # ���̼۵�ADF����
		if ContextInfo.is_last_bar():
			closedata_0 = closedata[3:-4]
			closedataModel_ARIMA = sm.tsa.ARMA(closedata_0,(4,3)).fit()
			predicts_ARIMA = closedataModel_ARIMA.predict(232, 241, dynamic = True)
			print("Ԥ�������ļ۸�",predicts_ARIMA[0]+close["close"][-1],predicts_ARIMA[1]+close["close"][-1], \
			predicts_ARIMA[2]+close["close"][-1],predicts_ARIMA[3]+close["close"][-1],\
			predicts_ARIMA[4]+close["close"][-1])
		closedata_5 = closedata[3:-4]
		#print len(closedata)
		#adftest = sm.tsa.stattools.adfuller(closedata)
		
		#if adftest[1] > 0.001:
			#return
		#result = sm.tsa.arma_order_select_ic(closedata,max_ar=6,max_ma=4,ic='aic')['aic_min_order']
		#print result

		closedataModel_ARIMA = sm.tsa.ARMA(closedata_5,(4,3)).fit()
		#print closedataModel_ARIMA.fittedvalues
		
		predicts_ARIMA = closedataModel_ARIMA.predict(232, 241, dynamic = True)
		#print predicts_ARIMA[4]
		ContextInfo.paint("close_5", close["close"][-1],-1,0)
		ContextInfo.paint("close_predict5", predicts_ARIMA[4]+close["close"][-5],-1,0)
		
		
		predicts_ARIMA = closedataModel_ARIMA.predict(232, 241, dynamic = True)
	except:
		ContextInfo.paint("close_5", close["close"][-1],-1,0)
		ContextInfo.paint("close_predict5", close["close"][-5],-1,0)
		print("Ԥ��ʧ��")
