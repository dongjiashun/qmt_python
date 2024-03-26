# encoding:gbk
'''
�����������趨�ý��׵Ĺ�Ʊ���ӣ�Ȼ�����ָ����CCIָ�����жϳ���ͳ���
���г���ͳ�������ʱ�����������趨�õĹ�Ʊ����
'''
import pandas as pd
import numpy as np
import talib
import time

######################PD ��ʽ����###########################
pd.set_option('expand_frame_repr', False)  # ������
pd.set_option('display.max_rows', 5000)  # �����ʾ���ݵ�����
pd.set_option('display.unicode.ambiguous_as_wide', True)  # �����ֶζ���
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.float_format', lambda x: '%.2f' % x)


##########################################################


# ####################��������˵��###########################
# real   1:ʵ��    	0��ģ���ʺ�
# log    1:��ӡ�ռ�   	0������ӡ�ռ�
# scale  ��λ����   ��������Ϊ  1/scale  ��ֵԽ�󣬿���ԽС
# buy_num   ����һ֧��Ʊ���Ƿ�ּ�������
###########################################################

class Tool():
    def __init__(self, ContextInfo):
        self.g = ContextInfo
        print('�Զ��幤����')

    def log(self, *args):
        # log Ϊ�û��������
        if log:
            print(*args)

    def readStockInfo(self, st):
        # ��ȡ���ɵĻ�����Ϣ
        start_time = self.g.get_open_date(st)
        # detail CreateDate:�������� ,FloatVolumn����ͨ�ɱ�,TotalVolumn���ܹɱ�
        detail = self.g.get_instrumentdetail(st)
        data = {}
        data['code'] = st
        data['start_time'] = str(detail['CreateDate'])
        data['FloatVolumn'] = np.int64(detail['FloatVolumn'])
        data['TotalVolumn'] = np.int64(detail['TotalVolumn'])
        series = pd.Series(data)
        self.g.stockinfo[st] = series

    # return series
    def readMyStock(self, bkname):
        # ��ȡ��ѡ���б�
        self.g.trade_code_list = self.g.get_stock_list_in_sector(bkname)
        self.g.set_universe(self.g.trade_code_list)
        self.g.stock_count = len(self.g.trade_code_list)

    def readStockData(self, columns=['close', 'open', 'high', 'low', 'volume', 'settle'], per='1d', size=10):
        # ��ȡ��Ʊ��������
        self.g.df = self.g.get_market_data(columns, stock_code=self.g.trade_code_list, skip_paused=True, period=per, dividend_type='front', count=size)

    def readStockDataTick(self):
        # ��ȡ�б��еĹ�Ʊ���̿�����
        self.g.df_tick = self.g.get_full_tick(self.g.trade_code_list)
        self.log(type(self.g.df_tick))

    def doRead(self, bkname):
        self.readMyStock(bkname)
        if self.g.stock_count == 0:
            print('��ǰ���û�����ݣ�����ӹ�Ʊ������б��У�')
            self.g.df_type = 0
            return
        # ��ȡ��Ʊ���̿�����
        self.readStockDataTick()
        # ��ȡ��Ʊ����������
        self.readStockData()
        self.log('��������:', type(self.g.df))
        if isinstance(self.g.df, pd.DataFrame):
            self.log('DF ���ݸ�ʽΪDataFrame')
            self.g.df_type = 1
            return
        elif isinstance(self.g.df, pd.Panel):
            self.log('DF ���ݸ�ʽΪPanel')
            self.g.df_type = 2
            return
        else:
            self.g.df_type = 0
            return

    def formatDf(self, st, df):
        # �������ݵĸ�ʽ��
        df_infos = self.g.stockinfo
        if st not in df_infos.columns:
            self.readStockInfo(st)
        if st not in df_infos.columns:
            return
        stock_info = self.g.stockinfo[st]
        self.log('info:', stock_info)

        # �����ǵ�ͣ��
        bd = 0.1
        code = int(st.split('.')[0])
        nc = code // 100000
        if nc == 3:
            bd = 0.2
        elif nc == 6:
            nc = code // 10000
            if nc == 68:
                bd = 0.2
        # bdֵΪ��Ʊ���ǵ�������  ��ҵ�塢�ƴ���Ϊ0.2  �����Ϊ0.1

        # ��ʽ������
        df['old_close'] = df['close'].shift(1)
        # ��������			���̼����
        df['open_offset'] = (df['open'] - df['old_close']) * 100 / df['old_close']
        # �����ǰ���̼�			�Ƿ�ӽ���ͣ
        df['now_offset'] = (df['close'] - df['old_close']) * 100 / df['old_close']
        # ���ÿ���			��ͣ��
        df['top'] = df['old_close'] * (1 + bd)
        df['top'] = df['top'].apply(lambda x: round(x, 2))
        # ���ÿ���			��ͣ��
        df['fail'] = df['old_close'] * (1 - bd)
        df['fail'] = df['fail'].apply(lambda x: round(x, 2))
        # ����				�Ƿ�������ͣ��
        df['istop'] = df['top'] == df['high']
        # ����				�Ƿ񴥼���ͣ��
        df['isfail'] = df['low'] == df['fail']
        # ��ǰ�����Ƿ�			��ͣ
        df['istopnow'] = df['top'] == df['close']
        # ��ǰ���̼���			��ͣ
        df['isfailnow'] = df['low'] == df['close']
        # ��ǰ				K�߻�����
        df['hand'] = df['volume'] / stock_info['FloatVolumn'] * 10000
        # ��ǰK��				�Ƿ����  -		�ɼ�һֱ�ڿ��̼��Ϸ�����
        df['isred'] = df['low'] >= df['open']
        # ��ǰK��				�Ƿ�Ϊ����
        df['issun'] = df['close'] >= df['open']
        return df

    def modelDb(self, st, df):
        # �жϵ�ǰ��Ʊ�Ƿ���ϴ������ ģ���㷨 ������������ True ���� False
        # ȡ���ù�Ʊ���̿�����
        # self.log(st,df)
        ndata = df.iloc[-1]
        self.log('����ʵʱ����', ndata)
        ndata = pd.Series(ndata)
        ndata['buy'] = False

        tick = self.g.df_tick[st]
        sellPrice = tick['askPrice']
        count = 0
        for i in range(0, 5):
            if sellPrice[i] == ndata['top']:
                count = i + 1
                break
        self.log('count=', count)
        if count == 0:
            return ndata
        if count <= offset and ndata['istop']:
            ndata['buy'] = True
            ndata['buy_price'] = sellPrice[count]
        return ndata


def init(ContextInfo):
    # hs300�ɷֹ���sh��sz�г�������ͨ��ֵ����ǰ3ֻ��Ʊ
    ContextInfo.trade_code_list = []
    ContextInfo.set_universe(ContextInfo.trade_code_list)
    ContextInfo.stock_count = 0

    ContextInfo.accID = '410038217334'
    ContextInfo.buy = True
    ContextInfo.sell = False
    # ��Ʊ��ʵʱ��������
    ContextInfo.df = None
    ContextInfo.df_type = 0
    # ��Ʊ��ʵʱ�̿�����
    ContextInfo.df_tick = None
    # ContextInfo.colums=['close','open','high','low','volume','settle']
    ContextInfo.tick = 0
    # ��Ʊ�б��и��ɵĻ�����Ϣ
    ContextInfo.stockinfo = pd.DataFrame()
    # �Զ��幤����
    ContextInfo.tool = Tool(ContextInfo)


# ���ö�ʱ����ִ���Զ�������  5nSecond,,500nMilliSecond
# ContextInfo.run_time("myHandlebar","5nSecond","2019-10-14 13:20:00","SH")


def myHandlebar(g):
    # tool = g.tool
    # tool.doRead('�ҵ���ѡ')
    return


# �Զ���Ľ��׺���
# ContextInfo.tick = ContextInfo.tick + 1
# print(ContextInfo.tick)
# readData(ContextInfo)

def handlebar(g):
    tool = g.tool
    # g.tool.formatFloat(1)
    if g.is_last_bar():
        # Ϊ�������ݵĸ�ʽ��df_type   0:������  1��DataFrame  2:Panel
        df = None
        tool.doRead('�ҵ���ѡ')
        if g.df_type == 0:
            return
        if g.df_type == 1:
            df = g.df
            st = g.trade_code_list[0]
            df = tool.formatDf(st, df)
            ndata = tool.modelDb(st, df)
            isbuy(g, st, ndata)
        elif g.df_type == 2:
            for st in g.trade_code_list:
                df = g.df[st]
                df = tool.formatDf(st, df)
                ndata = tool.modelDb(st, df)
                isbuy(g, st, ndata)


def isbuy(g, st, ndata):
    # �Ƿ�ִ�й�Ʊ�������
    print(ndata)
    if ndata['buy']:
        print('��Ʊ���֣�', st, ndata)
    pass



















