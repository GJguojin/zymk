'''
Created on 2018年11月23日

@author: Administrator
'''
#coding=utf-8

import requests
from urllib import parse
import urllib.request #获取网址模块
from bs4 import BeautifulSoup
from selenium import webdriver
import os

class Zymk:
    #知音漫客列表url
    url =''
    #漫画存储位置
    outPath=''
    
    #下载数量 0表示全部
    limit=0

    __title=''
    
    '''
            获取章节页面
    '''
    def getHtml(self):
        papg = urllib.request.urlopen(self.url) #打开图片的网址
        html = papg.read()  #用read方法读成网页源代码，格式为字节对象
        html = html.decode('UTF-8') #定义编码格式解码字符串(字节转换为字符串)
        return html
    
    
    def getChapterList(self):
        soup = BeautifulSoup(self.getHtml(), 'html.parser')
        #print(soup.prettify())
        browser = webdriver.Firefox()
        #browser.minimize_window()
        count =0
        try:
            for chapter in soup.find(id='chapterList'):
                #print(chapter)
                self.title = chapter.find('a').get('title')
                imgUrl = self.url+chapter.find('a').get('href')
                if self.title.isdigit() == False:
                    self.title = self.title.replace(self.title.split("话")[0],('%03d' %int(self.title.split("话")[0])),1)
                #print(title)
                #print(imgUrl)
                browser.get(imgUrl)
                browser.implicitly_wait(10)
                self.downloadImage(browser.page_source)
                
                count =count+1
                if self.limit != 0 and count >= self.limit:
                    break
        finally:
            browser.close()
           
    '''
            下载图片
    '''        
    def downloadImage(self,pageSource):
        #print(pageSource)
        soup = BeautifulSoup(pageSource, 'html.parser')
        img = "https:"+soup.find("img", "comicimg").get('src')
        self.storeImage(img)
    
    '''
            储存图片
    '''
    def storeImage(self,url):
        url = parse.unquote(url)
        print(url)
        count=1
        res = self.sendRequest(self.handleUrl(url,count))
        if res.status_code != 200:
            print("链接不存在:"+url)
          
        if not os.path.exists(self.outPath):
            os.makedirs(self.outPath)   
            
        while res.status_code == 200:
            path = self.outPath+self.title+'_'+('%02d' %count)+'.jpg'
            print(path)
            f = open(path,'ab') #存储图片，多媒体文件需要参数b（二进制文件）
            f.write(res.content) #多媒体存储content
            f.close()
            count = count+1
            res=self.sendRequest(self.handleUrl(url,count))
            
    def handleUrl(self,url,count):
        urlStrs = url.split('/')
        imgName = urlStrs[len(urlStrs)-1]
        return url.replace(imgName,imgName.replace(imgName.split(".")[0],str(count)))
        
    def sendRequest(self,url):
        return requests.get(url)
    
    def dealUrl(self,url):
        if not url.endswith("/"):
            url = url+"/" 
        return url
    '''
            构造方法
    ''' 
    def __init__(self,url,outPath):
        self.url = self.dealUrl(url)
        self.outPath= self.dealUrl(outPath)
        
        
zymk = Zymk('https://www.zymk.cn/1/','D:/漫画/斗破苍穹/')
zymk.limit =2
zymk.getChapterList()
