#coding:gbk



def init(ContextInfo):
	pass

def handlebar(ContextInfo):
	d = ContextInfo.barpos
	p = timetag_to_datetime(ContextInfo.get_bar_timetag(d),'%Y%m%d')
	print(p)
	cap_stk = ContextInfo.get_financial_data('CAPITALSTRUCTURE','total_capital',ContextInfo.market,ContextInfo.stockcode,d )
	ContextInfo.paint('�ܹɱ�',cap_stk/100000000,-1,0)
	
	inc_revenue = ContextInfo.get_financial_data('PERSHAREINDEX','inc_revenue',ContextInfo.market,ContextInfo.stockcode,d )
	ContextInfo.paint('��Ӫ����',inc_revenue/100000000,-1,0)
	
	s_fa_bps = ContextInfo.get_financial_data('PERSHAREINDEX','s_fa_bps',ContextInfo.market,ContextInfo.stockcode,d )
	ContextInfo.paint('ÿ�ɾ��ʲ�',s_fa_bps,-1,0)
	






