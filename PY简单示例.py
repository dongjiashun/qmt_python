#coding:gbk
#! /usr/bin/python 

def init(ContextInfo):
	#init��ʼ�趨����,���趨��ֱ��pass
	pass

def handlebar(ContextInfo):
	#handlebar ���K�ߵ������к���
        
	#��ǰK�ߵĶ�Ӧ���±��0��ʼ
	index = ContextInfo.barpos
	
	#��ǰK�߶�Ӧ��ʱ�䣺����
	realtime = ContextInfo.get_bar_timetag(index)

	#��ǰ����
	period = ContextInfo.period
	
	#��ǰ��ͼ��Ȩ��ʽ
	dividend_type = ContextInfo.dividend_type
	
	#ȡ��ǰK��ͼ��Ӧ�ĺ�Լ��ǰK�ߵĵ�ǰ��ͼ��Ȩ��ʽ�µ����̼�
	close = ContextInfo.get_market_data(['close'],period=period,dividend_type=dividend_type)
	
	#��ͼ�ϻ���close������ͼ
	ContextInfo.paint('close',close,-1,0)

