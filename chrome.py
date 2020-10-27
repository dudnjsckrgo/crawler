import sys
import os
import pickle
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import shutil
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import re
from urllib.request import urlopen
from selenium import webdriver
from urllib.request import urlopen
from dataclasses import dataclass ,asdict ,field
from collections import defaultdict 
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
# import pyautogui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By   
@dataclass
class ChromeDriver:
    # driver :object = webdriver.Chrome('C:/chromedriver/chromedriver.exe')
    first_url : str = 'http://m.hackers.co.kr/?c=s_toeic/toeic_board/B_TOEIC_data&source=http://www.hackers.co.kr'
    sub_url: str = '&p='
    soup : object = None
    parser : str = 'html.parser'
    page : int = 131
    filename ="urls"
    url :str ="http://m.hackers.co.kr/?c=s_toeic/toeic_board/B_TOEIC_data&p=3&uid=771347"
    context: str ="crawler/data/"
    context2: str = "crawler/data2/"
    context3: str = "E:/data2/"
    root_url: str ='http://m.hackers.co.kr'
    mydict : object =None
    new_folder_name : str = 'data3'
    count :int =902
    countPdf: int =0
    countZip: int = 0
    spyder: object = webdriver.Chrome('./chromedriver')
    
class ChromeListener:
    def __init__(self):
        self.driver = ChromeDriver()
        self.bs4Sel = Bs4Sel()
        
    def searching_data(self,i=0):
        driver= self.driver
        if i==0 :
            driver= Bs4Sel.bs4_get_url(driver)
        if i !=0 :
            driver= Bs4Sel.bs4_get_url(driver,i)
        
        second_target = {'tag': 'article'}
        confirm_target = {'tag': 'img','class':'imgpos'}
        imgposs = Bs4Sel.bs4_get_docs(driver,confirm_target)
        urls=[]
        for imgpos in imgposs:
            text=Bs4Sel.bs4_find_parents(imgpos,'article','onclick')
            if text == None:
                return 
            text=text.lstrip("goHref('")
            text=text.rstrip("');")
            text= driver.root_url + text
            urls.append(text)
        print(urls)
        filename = driver.filename + str(i).zfill(2)
        context=driver.context
        Bs4Sel.savePickle(urls,context, filename)
    
    def searching_data_2(self,**kargs):
        for key, value in kargs.items():
            if key =='i':
                i = value
            if key== 'url':
                url = value
                
        driver= self.driver
        if len(kargs)==2:
            driver.first_url= url
        driver=Bs4Sel.bs4_get_url(driver)
        target= {'tag':'article',"class":"text_area"}
        tag=Bs4Sel.bs4_get_doc(driver,target)
        # print("tag.name:",tag.name)
        tags= tag.select('div:nth-last-child(1)')
        # print("selet:" ,tags)
        # print(type(tags))
        urls = []
        
        # driver.mydict = defaultdict()
        # mydict = driver.mydict
        for tag in tags:
            try:
                if not tag.a:
                    continue
                if tag.a.attrs['href'] =="https://www.hackers.co.kr/?c=s_toeic/toeic_board/B_TOEIC_QA":
                    continue
                
                tags=tag.find_all('a')
                # print("tags: ",tags)
        
                for tag in tags:
                    text=tag.text.strip()
                    
                    sub_url= tag.attrs['href'] 
                    # print("#"*30+text)
                    # print("+"*50,tag)
                    # print("+"*50,tag.name)
                
                    full_url=driver.root_url + sub_url
                    # urls.append((text,full_url))
                    
                    
                    if text.find('.zip') != -1:
                        
                        driver.countZip += 1
                        print(f"zip파일이 {driver.countZip}개 생략")
                        continue
                    if text.find('.pdf') != -1: 
                        driver.countPdf += 1
                        print(f"pdf파일이 {driver.countPdf}개 생략")
                        continue
                    obj = re.compile(r'\.[a-z]{3,5}$')
                    # print(obj.search(text))
                    match =obj.search(text)
                    mytype=match.group()
                    mytype = mytype.lstrip('.')
                    # print(match.group())
                    driver.new_folder_name = mytype 
                    title =text.rstrip(match.group())
                    Bs4Sel.create_folder(driver)
                    # mydict[mytype]={}
                    # mydict[mytype][title]=full_url
                    Bs4Sel.saveFile(driver,full_url,mytype,title)
            except Exception as err:
                print(err)        
                    # print(full_url)
        
            
 
                
        filename = driver.filename + str(driver.count).zfill(2)
        driver.count += 1
        context=driver.context2
        # Bs4Sel.savePickle(mydict,context, filename)
        
    def loopfun(self):
        driver = self.driver
        for i in range(51,driver.page):
            self.searching_data(i)
            
    def loopfun2(self):
        driver = self.driver
        for i in range(52,driver.page):
            filename= driver.filename + str(i).zfill(2)
            context= driver.context
            try:
                mylist=Bs4Sel.loadPickle(context,filename)
            except:
                continue
            # print(mylist)
            set(mylist)
            print(set(mylist))
            for j, url in enumerate(set(mylist)):
                self.searching_data_2(i=j,url=url)
                # break #차후에 제거
    def sel_searching_data(self):
        driver =self.driver.spyder
        bs4Sel=self.bs4Sel
        bs4Sel.sel_get_url(driver,'https://en.dict.naver.com/#/main')
        css='#ac_input'
        bs4Sel.sel_wait_by_css(driver,css)
        element=bs4Sel.sel_get_element_by_css(driver,css)
        text='for'
        bs4Sel.sel_input_text(driver,element,text)
        css='#searchPage_entry > div > div:nth-child(1) > div > a > strong'
        bs4Sel.sel_wait_by_css(driver,css)
        print("done")
        element=bs4Sel.sel_get_element_by_css(driver, css)
        bs4Sel.sel_click(driver,element)
        css='em.part_speech'
        bs4Sel.sel_wait_by_css(driver, css)
        proNs=bs4Sel.sel_get_elements_by_css(driver,css)

        for proN in proNs:
            proN = proN.get_attribute('innerHTML')
            proN = proN.strip('\n\t')
            print(proN)
        css='span.mean'
        meanings= bs4Sel.sel_get_elements_by_css(driver, css)
        css='#content > div.article._article.is-closed > div.section.section_mean._section_mean._data_index_1 > div > div.mean_tray > ul > li > div.mean_desc > span'
        nums=bs4Sel.sel_get_elements_by_css(driver,css)
        idx=0
        for num, mean in zip(nums, meanings):
            mean = mean.get_attribute('innerHTML')
            mean = mean.strip()
            mean1=re.sub(r'(\<.*?\>)', '', mean)
            numtxt = num.get_attribute('innerHTML')
            numtxt = numtxt.strip()
            if numtxt == '1.':
                proN = proNs[idx].get_attribute('innerHTML')
                idx+=1
                proN = proN.strip('\n\t')
                print(proN)
            print(numtxt, mean1)
        css='div.mean_desc'
    
        
        

        
        

class Bs4Sel:
    def __init(self):
        self.driver = ChromeDriver()
    @staticmethod
    def sel_get_element_by_css(driver,css): 
     
        element=driver.find_element_by_css_selector(css)
        return element
    @staticmethod
    def sel_get_elements_by_css(driver,css): 
     
        elements=driver.find_elements_by_css_selector(css)
        return elements
    @staticmethod
    def sel_get_url(driver,url):
      
        driver.get(url)
        
    @staticmethod
    def sel_wait_by_css(driver,css):
   
        delay =1000
        WebDriverWait(driver,delay).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, css)))
        
    @staticmethod
    def sel_input_text(driver,element,text):
     
        ActionChains(driver).move_to_element(element).click(element).send_keys(text, Keys.ENTER).perform()
    @staticmethod
    def sel_click(driver,element):
        ActionChains(driver).move_to_element(element).click(element).perform()
    # def sel_find_css()
    @staticmethod
    def bs4_get_url(driver, *args):
        if len(args)==0:
            url = driver.first_url
        if len(args)==1:
            url = driver.first_url+ driver.sub_url+ str(args[0])
        response = urlopen(url)
        driver.soup = BeautifulSoup(response, driver.parser)
        print(driver.soup)
        return driver
    @staticmethod
    def bs4_get_docs(driver,kargs):
        for key, value in kargs.items():
            if key =='tag':
                tag= value
            if key != 'tag':
                attrs =key
                # print(attrs)
                value =value
                # print(value)
        if len(kargs) == 2:
            targets = driver.soup.find_all(tag, attrs={attrs: value})
            print("2: ",type(targets))
        if len(kargs) == 1:
            targets = driver.soup.find_all(tag)
            print("1: ",type(targets))
        # for target in targets:
            # print("-"*30)
            # print(target)
            # print("-"*30)
        return targets
    @staticmethod
    def bs4_get_doc(driver,kargs):
        for key, value in kargs.items():
            if key =='tag':
                tag= value
            if key != 'tag':
                attrs =key
                # print(attrs)
                value =value
                # print(value)
        if len(kargs) == 2:
            target = driver.soup.find(tag, attrs={attrs: value})
            # print("2: ",type(target))
        if len(kargs) == 1:
            target = driver.soup.find(tag)
            # print("1: ",type(target))
      
        return target
    
    @staticmethod
    def bs4_find_parents(target,myparent,attrs):
        try:
            while target.name != myparent:
                target=target.parent
                # print(target.name)
            text=target.attrs[attrs]
            print(text)
            print(type(text))
            return text
        except:
            return
            
    
    @staticmethod
    def savePickle(mylist,context,filename):
        path = context +filename + '.pickle'
        print(type(mylist))
       
        with open(file=path,mode="wb") as fw:
            pickle.dump(mylist,fw)
            print(f'{filename}  피클 저장완료!!!!')
        # if type(mylist)=='dict': 
        #     with open(file=path,mode="wb") as fw:
        #         pickle.dump(mylist,fw, protocol=pickle.HIGHEST_PROTOCOL)
        #         print(f'{filename} 딕셔너리 피클 저장완료!!!!')
    @staticmethod
    def loadPickle(context,filename):
        path = context +filename+'.pickle'
        # print(path)
        with open(file=path,mode='rb') as fw:
            mylist=pickle.load(fw)
            print(f"{path} loading 완료!!!!!")
        return mylist
    @staticmethod
    def saveFile(driver,url,mytype,title):
        file = urlopen(url)
        filename = driver.context3 + mytype + '/' + title + '.'+mytype
        # print(mysrc)
        # print(filename)

        with open(filename, mode='wb') as fw:
            fw.write(file.read()) # 바이트 형태로 저장
            print(f'{filename} 저장완료!!!!!!!!!!!!')

           
    @staticmethod
    def create_folder(driver)->object:
        # shutil : shell utility : 고수준 파일 연산. 표준 라이브러리
        folderName= driver.new_folder_name
        context = driver.context3
        folder = context+folderName +'/' # 유닉스 기반은 '/'이 구분자
        try:
            if not os.path.exists(folder):
                os.mkdir(folder)

        except FileExistsError as err:
            print(err)
        return folder
    
if __name__ == "__main__":
    api = ChromeListener()
    # api.searching_data()
    # api.loopfun()
    api.sel_searching_data()

