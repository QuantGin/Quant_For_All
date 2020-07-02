from selenium.common.exceptions import * 
import requests
import time
import os
import traceback
class joinquant:
    def __init__(self,d):
        self.d=d

    def login(self,username,password):
        d=self.d
        d.get('https://www.joinquant.com/research')
        d1=d.find_element_by_class_name('phone')
        d1.clear()
        d1.send_keys(username)
        d1=d.find_element_by_class_name('jq-login__password')
        d1.clear()
        d1.send_keys(password)
        self.wait()
        d.find_element_by_class_name('login-submit').click()
        for i in range(60):
            try:
                d.switch_to.default_content()
                d.switch_to.frame("research")
                d.find_element_by_class_name('fa-folder')
                if d.current_url=='https://www.joinquant.com/default/research/index?target=self&amp;url=/default/research/redirect':
                    self._get_cookie()
                    print('Login was successful!')
                    self.wait(3)
                    return 1
            except Exception as e:
                pass
            self.wait()
        return 0
    def wait(self,n=1):
        time.sleep(1*n)
    def _get_cookie(self):
        d=self.d
        cookie =[item["name"] + ":" + item["value"] for item in d.get_cookies()]
        cookiestr = ';'.join(item for item in cookie)
        cook_map = {}
        for item in cookie :
            str = item.split(':')
            cook_map[str[0]] = str[1]
        cookies = requests.utils.cookiejar_from_dict(cook_map, cookiejar=None, overwrite=True)
        self.cookies=cookies
    def _research(self):
        d=self.d
        d.switch_to.default_content()
        d.execute_script("document.getElementById('kk_nav').style.display='none'")
        d.switch_to.frame("research")
    def download(self,url,file_dir):
        file=file_dir+url.split('/')[-1]
        if os.path.exists(file):
            print('Download',file)
            return 1
        else:
            print('Downloading',file)
            self._get_cookie()
            r=requests.get(url,cookies=self.cookies)
            fout=open(file,'wb')
            fout.write(r.content)
            fout.close
            return 1
    #输出当前路径
    @property
    def pwd(self):
        d=self.d
        self._research()
        d1=d.find_element_by_class_name('breadcrumb')
        s=d1.find_elements_by_xpath(".//*")[-2].get_attribute('innerHTML')
        print(s.split('"')[1].split('/tree')[-1])
        return s.split('"')[1].split('/tree')[-1]
    @property
    def ls(self):
        d=self.d
        self._research()
        d1=d.find_element_by_id('notebook_list')
        l=[key.get_attribute('innerHTML') for key in d1.find_elements_by_class_name('item_name')]
        ll=[]
        for key in l:
            if key!='..':
                ll.append(key)
        print(ll[:3],ll[-3:])
        return ll
    def _clear(self):
        d=self.d
        self._research()
        for i in range(3):
            try:
                d.find_element_by_class_name('modal-content').find_element_by_class_name('btn,btn-default,btn-sm,btn-primary').click()
                break
            except:
                pass
    def click(self,name):
        d=self.d
        self._research()
        d1=d.find_element_by_id('notebook_list')
        d1.find_element_by_link_text(name).click()
        print(name,'clicked')
    def home(self):
        d=self.d
        self._research()
        for i in range(3):
            self._research()
            try:
                for ii in range(10):
                    self._research()
                    d.find_element_by_class_name('fa-folder').click()
                    self.wait()
                    if self.pwd=='':
                        print('cd /')
                        return 1
            except:
                d.get('https://www.joinquant.com/research')
                self.wait()
        return 0
    def cd(self,s_dir):
        d=self.d
        for ii in range(3):
            try:
                self.home()
                _dir=''
                if len(s_dir)>0:
                    for s in s_dir.split('/'):
                        if len(s)>0:
                            _dir+='/'+s
                            for i in range(10):
                                try:
                                    self.click(s)
                                except:pass
                                if self.pwd==_dir:
                                    break
                                self.wait()
                    if _dir==self.pwd:
                        print('cd',_dir)
                        return 1
            except:pass
            self.wait(3)
        return 0
    def get_url(self,name):
        d=self.d
        self._research()
        d2=d.find_element_by_id('notebook_list')
        for d1 in d2.find_elements_by_class_name('item_link'):
            _name=d1.find_element_by_class_name('item_name').get_attribute('innerHTML')
            if _name==name:
                url=d1.get_attribute('href')
                return url
    def select(self,name):
        d=self.d
        self._research()
        d2=d.find_element_by_id('notebook_list')
        for d1 in d2.find_elements_by_class_name('col-md-12')[:]:
            _name=d1.find_element_by_class_name('item_name').get_attribute('innerHTML')
            if _name==name:
                d1.find_element_by_class_name('item_icon,file_icon,icon-fixed-width').click()
                print(name,'selected')
                break
    def click_delete(self):
        d=self.d
        self._research()
        for i in range(10):
            try:
                d.find_element_by_class_name('fa-trash').click()
                break
            except:self.wait(1)
        for i in range(10):
            try:
                d.find_element_by_class_name('modal-content').find_element_by_class_name('btn-danger').click()
            except:self.wait(1)
        self._clear()
        self.wait(1)
    def _download_delete(self,s_dir,file_dir):
        d=self.d
        self.cd(s_dir)
        self.wait(10)
        l=self.ls
        while len(l)>0:
            for name in l[:20]:
                url=self.get_url(name).replace('/edit/','/files/')
                name0=url.split('.')[-1]
                if not name0 in ['ipynb','py'] and url.find('.')!=0 and url.find(s_dir)!=-1:
                    if self.download(url,file_dir):
                        self.select(name)
                        
            self.click_delete()
            l=self.ls
        return 1
    def download_delete(self,s_dir,file_dir):
        while 1:
            try:
                if self._download_delete(s_dir,file_dir):
                    return 1
            except ElementClickInterceptedException:pass
            except StaleElementReferenceException:pass
            except ElementNotInteractableException:pass
            except NoSuchElementException:pass
    def _stop_run(self):
        self._clear()
        #停止并运行
        d=self.d
        self._research()
        d.find_element_by_class_name('fa-stop,fa').click()
        self.wait(5)
        d.find_element_by_link_text('单元格').click()
        self.wait()
        d.find_element_by_link_text('运行所有').click()
        self.wait()
    def _click_run(self):
        self._clear()
        d=self.d
        self._research()
        self.wait()
        d.find_element_by_link_text('单元格').click()
        self.wait()
        d.find_element_by_link_text('运行所有').click()
        self.wait()
    def run(self,name):
        d=self.d
        self._research()
        self.click(name)
        self.wait()
        d.switch_to.window(d.window_handles[-1])
        self._research()
        self._stop_run()
        for i in range(60):
            self.wait()
            d1=d.find_elements_by_class_name('output_subarea,output_text,output_result')
            if len(d1)<1:
                continue
            d1=d1[0]
            html=d1.get_attribute('innerHTML')
            if  html.find('!!success!!')!=-1:
                d.close()
                self.wait()
                d.switch_to.window(d.window_handles[0])
                self.wait()
                return 1
            errors=d.find_elements_by_class_name('output_subarea,output_text,output_error')
            for error in errors:
                if error.get_attribute('innerHTML').find('Traceback')!=-1:
                    error=error.get_attribute('innerHTML')
                    raise(ValueError(error))
    def keep_running(self,name):
        d=self.d
        self._research()
        self.click(name)
        self.wait()
        d.switch_to.window(d.window_handles[-1])
        self._research()
        while 1:
            try:
                self._click_run()
            except:
                print(traceback.format_exc())
            print('click')
            self.wait(10)
if __name__ == "__main__":
    #配置虚拟浏览器
    from selenium import webdriver
    from selenium.common.exceptions import * 
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-popup-blocking")
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')
    d = webdriver.Chrome(options=chrome_options)
    jq=joinquant(d)
    # 登录
    jq.login('username','password')
    # 进入指定路径
    jq.cd('price_daily')
    # 列出路径下文件
    print(jq.ls)
    # 保持指定notebook运行
    self.keep_running('XXX.ipynb')
    # 下载并在网站上删除指定路径下的所有文件XXX
    jq.download_delete('XXX','../XXX/XXX/')