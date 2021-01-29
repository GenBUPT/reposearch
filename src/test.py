import pandas as pd
import json
import requests
import urllib.parse as parse
from bs4 import BeautifulSoup
import time
import sys
url = "https://github.com/search?q=size%3A16105..16140+language%3AJava&ref=advsearch&type=Repositories"
req = requests.get(url)
html = req.text
#print(html)
soup = BeautifulSoup(html,"lxml")
print(soup)
tag = soup.find_all("a","UnderlineNav-item flex-shrink-0 selected")
tmp = BeautifulSoup(str(tag[0]),"lxml")
print(tmp.span.string)