#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import tool
import os,sys
 
class Spider:
 
    def __init__(self):
        self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'
        self.tool = tool.Tool()
 
    def getPage(self,pageIndex):
        url = self.siteURL + "?page=" + str(pageIndex)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().decode('gbk')
 
    def getContents(self,pageIndex):
        page = self.getPage(pageIndex)
        pattern = re.compile('<div.?class="list-item".*?pic-word.*?<a.?href="(.*?)'+
                             '".*?<img.?src="(.*?)".*?<a.?class="lady-name.*?>(.*?)</a>'+
                             '.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',re.S)
        items = re.findall(pattern,page)
        contents = []
        for item in items:
            contents.append(['http:' + item[0],'http:' + item[1],item[2],item[3],item[4]])
        return contents
 
    def getDetailPage(self,infoURL):
        response = urllib2.urlopen(infoURL)
        return response.read().decode('gbk')
 
    def getBrief(self,page):
        pattern = re.compile('<div.?class="mm-aixiu-content".*?>(.*?)<!--',re.S)
        result = re.search(pattern,page)
	print result
	sys.exit()
	return result.group(1)
 
    def getAllImg(self,page):
        patternImg = re.compile('<img.*?src="(.*?)"',re.S)
        images = re.findall(patternImg,page.group(1))
        return images
 
    def saveImgs(self,images,name):
        number = 1
        print u"Discovery",name,u"total of",len(images),u"photo"
        for imageURL in images:
            splitPath = imageURL.split('.')
            fTail = splitPath.pop()
            if len(fTail) > 3:
                fTail = "jpg"
            fileName = name + "/" + str(number) + "." + fTail
            self.saveImg('http:'+imageURL,fileName)
            number += 1
 
    def saveIcon(self,iconURL,name):
        splitPath = iconURL.split('.')
        fTail = splitPath.pop()
        fileName = name + "/icon." + fTail
        self.saveImg(iconURL,fileName)
 
    def saveBrief(self,content,name):
	content = self.tool.replace(content)
        fileName = name + "/" + name + ".txt"
        print u"Save Person Information:",fileName
	with open(fileName,'w+') as f:
            f.write(content.encode('utf-8'))
 
    def saveImg(self,imageURL,fileName):
        u = urllib.urlopen(imageURL)
        data = u.read()
        print u"Save Image:",fileName
	with open(fileName,'wb+') as f:
	    f.write(data) 

    def mkdir(self,path):
        path = path.strip()
        isExists=os.path.exists(path)
        if not isExists:
            print u"mkdir",path,u'OK'
            os.makedirs(path)
            return True
        else:
            print path,u'Exist'
            return False
 
    def savePageInfo(self,pageIndex):
        contents = self.getContents(pageIndex)
        for item in contents:
            print u"Name:",item[2],u"Age:",item[3],u"City:",item[4]
            print u"Private Person Blog:",item[0]
            detailURL = item[0]
            detailPage = self.getDetailPage(detailURL)
            brief = self.getBrief(detailPage)
            images = self.getAllImg(brief)
            self.mkdir(item[2])
            self.saveBrief(brief,item[2])
            self.saveIcon(item[1],item[2])
            self.saveImgs(images,item[2])
 
    def savePagesInfo(self,start,end):
        for i in range(start,end+1):
            print u"loading",i,u"page"
            self.savePageInfo(i)
 
spider = Spider()
spider.savePagesInfo(1,5)
