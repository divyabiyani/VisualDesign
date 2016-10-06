from bs4 import BeautifulSoup
from JavaScriptRendering import Render
import requests
import collections
import webbrowser

class VisualDesignScrape:
	def __init__(self):
		url='https://input.mozilla.org/en-US/?product=Firefox'
		r=Render(url)
		result=r.frame.toHtml()
		data= str(result.toAscii())
		self.soup= BeautifulSoup(data)

	def extractVersionPercentage(self):
		versionPer={}
		ulList=self.soup.find_all('ul')
		for ul in ulList:
			if ul.get('name')=='version':
				version=ul
				break
		liList=version.find_all('li')

		for li in liList:
			spanList=li.find_all('span')
			versionPer.update({spanList[1].text:spanList[2].text})
		odVersionPer=collections.OrderedDict(sorted(versionPer.items()))
		return odVersionPer

v=VisualDesignScrape()
dict=v.extractVersionPercentage()
data="per='["
for i in dict:
	data=data + '{"label":"' + i + '",'
	data=data + '"value":' + dict[i][0:len(dict[i])-1] + '},'

if len(data)>1:
	data=data[:len(data)-1]
data=data + "]'"

f=open("./json/doubtsRegardingVersion.json","w")
f.write(data)
webbrowser.open("./style/index.html")

