import sys
from mylog import mylog
logger=mylog(sys.argv[0].split('/')[-1]).get_logger()
import requests
import threading

def get_trade(stk,n=10):
    stk=to_shsz(stk)
    # url='http://vip.stock.finance.sina.com.cn/quotes_service/view/CN_TransListV2.php?num=50&symbol=sh600000'
    url='https://vip.stock.finance.sina.com.cn/quotes_service/view/CN_TransListV2.php?num='+str(n)+'&symbol='+stk
    r=requests.get(url)
    s=r.text
    if s.find('var trade_item_list = new Array()')==-1:
        raise(ValueError())
    s=s.replace("'",'')
    s=s.replace('var trade_item_list = new Array();\n','')
    s=s.split('\n var trade_INVOL_OUTVOL')[0]
    l=[]
    for key in s.split('\n'):
        if key.find('new Array')!=-1:
            dic={'code':press_code(stk)}
            dic['time'],dic['amount'],dic['price'],dic['side']=key.split('(')[-1].split(')')[0].split(', ')
            l.append(dic)
    return l
# get_trade('sh600000'),get_trade('600100.XSHG')

def get_depth(stk_list):
    stk=''
    if isinstance(stk_list,list):
        for key in stk_list:
            stk+=to_shsz(key)+','
    else:
        stk=to_shsz(stk_list)
    r=requests.get('https://hq.sinajs.cn/list='+stk)
    ss=r.text
#     print(ss)
    if ss.find('hq_str_')==-1:
        raise(ValueError(ss))
    l0=[]
    for s in ss.split('var '):
        if len(s)>0 and s.find('""')==-1:
            code=s.split('=')[0].split('_')[-1]
            l=s.split(',')[10:32]
            l.reverse()
            fields=['a5_v', 'a5_p', 'a4_v', 'a4_p', 'a3_v', 'a3_p',
                    'a2_v', 'a2_p', 'a1_v', 'a1_p', 'b1_v', 'b1_p',
                    'b2_v', 'b2_p', 'b3_v', 'b3_p', 'b4_v', 'b4_p',
                    'b5_v', 'b5_p']
            dic={'code':press_code(code)}
            for key in fields:
                dic[key]=l.pop()
            dic['datetime']=l[1]+' '+l[0]
            l0.append(dic)
    return l0
# len(get_depth(get_stk_list()[:893]))
def get_all_depth(stk_list):
    def _run(stk_list2,l):
        try:
            l+=get_depth(stk_list2)
        except:
            logger.error(traceback.format_exc())
            return []
    l=[]
    jobs=[]
    stk_list1=stk_list
    while len(stk_list1)>0:
        stk_list2=stk_list1[:800]
        stk_list1=stk_list1[800:]
        job=threading.Thread(target=_run,args=(stk_list2,l))
        job.start()
        jobs.append(job)
    for job in jobs:
        job.join()
    return l