# 用法：
# mylog('test').get_logger
import logging
import logging.handlers  

import datetime
import os
class mylog():
    def __init__(self,name='main',level=logging.DEBUG):
        try:
            os.mkdir('./log')
        except:pass
        self.logger=logging.getLogger(name)
        self.logger.setLevel(level)
        if not self.logger.handlers:
            self.logger.propagate = False
            fh = logging.handlers.TimedRotatingFileHandler('./log/'+name+'.log',when="D", interval=1, backupCount=7)  
            ch = logging.StreamHandler() 
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  
            fh.setFormatter(formatter)  
            ch.setFormatter(formatter)  
            self.logger.addHandler(fh)  
            self.logger.addHandler(ch)
    def get_logger(self):
        return self.logger

################################################################################
# 故障处理装饰器
# 重试5次，最大一次等待约17分钟
# ！！！如果所有重试失败会抛出最后一次的错误！！！
# 用法：
# @my_capture
# def fun():
#     print(kkp)
#     return 1
# fun()
#-------------------------------------------------------------------------------
import traceback
import time
def my_capture(fun):
    def _cap(*args, **kwargs):
        max_retry=5
        t=1
        for i in range(max_retry+1):
            try:
                results=fun(*args, **kwargs)
                return results
            except Exception as e:
                try:
                    name=fun.__name__
                except:
                    name='No Name '
                logger=mylog(name).get_logger()
                if i==max_retry:
                    logger.critical(traceback.format_exc())
                    raise(e)
                else:
                    logger.error(traceback.format_exc())
            logger.error('Retry afret '+str(4**i)+' S')
            time.sleep(4**i)
    return _cap
################################################################################
