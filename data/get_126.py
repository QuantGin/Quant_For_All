import requests
import json
import sys
from mylog import mylog
logger=mylog(sys.argv[0].split('/')[-1]).get_logger()
# url='http://api.money.126.net/data/feed/0600446,0600570,1300033,1000997,0601519'
import threading
def get_126_depth(stk_list):
    if isinstance(stk_list,str):
        stk_list=[stk_list]
    stk_list1=[]
    for key in stk_list:
        key=key.split('.')[0]
        if key[0]=='6':
            key='0'+key
        else:
            key='1'+key
        stk_list1.append(key)
    stk_list=stk_list1

    url='https://api.money.126.net/data/feed/'
    for stk in stk_list:
        url+=stk+','
    r=requests.get(url)
    return [value for key,value in json.loads(r.text.split('(')[1].split(')')[0]).items()]

def get_all_126_depth(stk_list):
    def _run(stk_list2,l):
        try:
            l+=get_126_depth(stk_list2)
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
# import time
# begin=time.time()
# get_all_126_depth(get_stk_list())
# time.time()-begin