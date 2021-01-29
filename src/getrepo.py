"""
    todo :
        1.generate a url with language size page and token
        2.get size with json file configuration
        3.compute invertal time between two requests 5000?
        4.check if the limit happend
"""
import pandas as pd
import json
import requests
import urllib.parse as parse
from bs4 import BeautifulSoup
import copy
import time
import sys
import re
def paratourl(size,language):
    return parse.quote("size:{}".format(size))+"+"+parse.quote("language:{}".format(language))
def getrepocount(domtree,url):
    tag = domtree.find_all("a","UnderlineNav-item flex-shrink-0 selected")
    if len(tag)==1:
        tmp = BeautifulSoup(str(tag[0]),"lxml")
        print(tag[0])
        try:
            t = int(tmp.span.string)
        except ValueError as ve:
            logfile = open("log.txt","a+")
            logfile.write(domtree.text)
            logfile.write(url)
            logfile.close()
            if "K" in tmp.span.string or "M" in tmp.span.string:
                t = 1001
            else :
                return -1
        if t>1000:
            return 10
        elif t%10==0:
            return t//10
        else:
            return t//10+1
    return -1
class advsearch:
    countzzz = 0
    searchurl = "https://github.com/search"
    params = {"type":"Repositories","ref":"advsearch"}
    def getrepo(self,size,language):
        stat = 0
        wholepage = -1
        page  = 2
        repos = list()
        requests.session().keep_alive = False
        urlparam = "?q="+paratourl(size,language)
        param = self.params
        while True:
            if self.countzzz==1000:
                time.sleep(300)
                self.countzzz=0
            self.countzzz = self.countzzz+1
            try:
                headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}
                req = requests.get(self.searchurl+urlparam,params=param,timeout=500,headers = headers)
                print(req.url)
                print("now page = {} and wholepage = {} stat = {}".format(page,wholepage,stat))
            except requests.RequestException as iden:
                print(iden)
                time.sleep(12)
                continue
            html = req.text
            soup = BeautifulSoup(html,"lxml")
            tag = soup.find_all("a","v-align-middle")
            if len(tag)==0:
                time.sleep(12)
                continue
            else:
                for i in tag:
                    repos.append(i.get_text())
                time.sleep(6)
                if stat ==0:
                    wholepage = getrepocount(soup,req.url)
                    if wholepage==-1:
                        continue
                    else:
                        stat = 1
                    pass
                else:
                    if(wholepage>=page):
                        param.update({"p":page})
                        page = page+1
                    else:
                        if wholepage>0:
                            param.pop("p")
                        stat = 0
                        break
        return repos
search = advsearch()
f = open("massage.json","r")
massage = json.load(f)
f.close()
f = open("Javarepo.json","a+")
reposize = massage['size']
repos = []
for size in reposize:
    begin = size['begin']
    end = size['end']
    section = size['len']
    while begin<=end:
        repos = repos + search.getrepo("{}..{}".format(begin,begin+section),"Java")
        begin = begin+section
        if len(repos)>=5000:
            json.dump(repos,f)
            f.flush()
            repos.clear()
json.dump(repos,f)
f.close()