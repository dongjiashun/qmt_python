# encoding:gbk
'''
�����������趨�ý��׵Ĺ�Ʊ���ӣ�Ȼ�����ָ����CCIָ�����жϳ���ͳ���
���г���ͳ�������ʱ�����������趨�õĹ�Ʊ����
'''
import pandas as pd
import numpy as np
import talib


def init(ContextInfo):
    # hs300�ɷֹ���sh��sz�г�������ͨ��ֵ����ǰ3ֻ��Ʊ
    ContextInfo.trade_code_list = ['601398.SH', '601857.SH', '601288.SH', '000333.SZ', '002415.SZ', '000002.SZ']
    ContextInfo.set_universe(ContextInfo.trade_code_list)
    ContextInfo.accID = '6000000058'
    ContextInfo.buy = True
    ContextInfo.sell = False


def handlebar(ContextInfo):
    if not ContextInfo.is_last_bar():
        return
    Result = ContextInfo.get_full_tick(['601398.SH', '601857.SH', '601288.SH', '000333.SZ', '002415.SZ', '000002.SZ'])
    df = pd.DataFrame(Result)
    df2 = df.T
    df2.to_csv('24-02-05.csv', mode='a', header=None)
    print('д��ɹ�!')



