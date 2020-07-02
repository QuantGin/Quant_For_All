import requests
import sys
import threading
from mylog import mylog
logger=mylog(sys.argv[0].split('/')[-1]).get_logger()
def get_tencent_depth(stk_list):
    stk_list1=[]
    url='http://web.sqt.gtimg.cn/utf8/q='
    for key in stk_list:
        key=key.split('.')[0]
        if key[0]=='6':
            key='sh'+key
        else:
            key='sz'+key
        url+=key+','
    r=requests.get(url)
    ll=[]
    l0=r.text.split('\n')
    for s in l0:
        if len(s)>0:
            l=s.split('"')[1].split('~')
            dic={}
            dic['code']=press_code(l[2])
            dic['b1_p']=l[9]
            dic['b1_v']=l[10]
            dic['b2_p']=l[11]
            dic['b2_v']=l[12]
            dic['b3_p']=l[13]
            dic['b3_v']=l[14]
            dic['b4_p']=l[15]
            dic['b4_v']=l[16]
            dic['b5_p']=l[17]
            dic['b5_v']=l[18]

            dic['a1_p']=l[19]
            dic['a1_v']=l[20]
            dic['a2_p']=l[21]
            dic['a2_v']=l[22]
            dic['a3_p']=l[23]
            dic['a3_v']=l[24]
            dic['a4_p']=l[25]
            dic['a4_v']=l[26]
            dic['a5_p']=l[27]
            dic['a5_v']=l[28]
            t=l[30]
            dic['datetime']=t[:4]+'-'+t[4:6]+'-'+t[6:8]+' '+t[8:10]+':'+t[10:12]+':'+t[12:]
            ll.append(dic)
    return ll
def get_all_tencent_depth(stk_list):
    def _run(stk_list2,l):
        try:
            l+=get_tencent_depth(stk_list2)
        except:
            logger.error(traceback.format_exc())
            return []
    l=[]
    jobs=[]
    stk_list1=stk_list
    while len(stk_list1)>0:
        stk_list2=stk_list1[:900]
        stk_list1=stk_list1[900:]
        job=threading.Thread(target=_run,args=(stk_list2,l))
        job.start()
        jobs.append(job)
    for job in jobs:
        job.join()
    return l
# import time
# begin=time.time()
# len(get_all_tencent_depth(get_stk_list()))
# time.time()-begin