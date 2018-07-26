import urllib.request
import urllib.parse
import re
import regex
from bs4 import BeautifulSoup

homeUrl = 'http://www.billwurtz.com/questions/questions.html'
rawFileName = 'recent-questions-raw.txt'

def pageScraper(url):
    resp = urllib.request.urlopen(url)
    respData = resp.read()
    questions = re.findall(r'<h3> <dco>(.*?)</br></br>', str(respData))

    #The file used to store the raw HTML entries. This has to go through another function to strip all remaining tags
    out = open(rawFileName, 'w')

    for q in questions:
        date = re.findall(r'<dco>(.*?)</dco>', q, re.DOTALL)
        if date:
            date, time = date[0].split('&nbsp; \n')
            out.write('[' + date + ' - ' + time + ']' + '\n')

            qnaList = re.findall(r'<qco>(.*?)<h3>', str(q), re.DOTALL)
            qnaList = [item + '\n' for item in qnaList]
            for q in qnaList:
                soup = BeautifulSoup(q, "html.parser")
                out.write(soup.get_text())

            lastSubQuestion = regex.findall(r'(?r)<qco>(.*?)', str(q), re.DOTALL)
            soup = BeautifulSoup(lastSubQuestion[0], "html.parser")
            out.write(soup.get_text() + '\n\n')

    #Last entry always falls in a different pattern, so parsing right-to-left is faster.
    lastQuestion = regex.findall(r'(?r)<h3>(.*?)<A NAME="bottom">', str(respData))
    out.write(lastQuestion[0] + '\n')

    nextUrlData = regex.findall(r'(?r)<a href="questions-20(.*?).html">', str(respData))
    
    #The oldest page won't have a link at the bottom. This is a temporary workaround.
    if len(nextUrlData[0]) > 6:
        return

    year, month = nextUrlData[0].split("-")
    nextUrl = 'http://www.billwurtz.com/questions/questions-20' + year + '-' + month + '.html'

    print('Parsing ' + nextUrl)
    out.close()
    
    return nextUrl

def stripTags(rawFileName, cleanFileName):
    print('Cleaning the file...')
    with open(rawFileName, 'r') as raw, open(cleanFileName, 'a') as clean:
        for question in raw:
            date = re.findall(r'<dco>(.*?)</dco>', str(question), re.DOTALL)
            if date:
                print(date[0])
                date, time = date[0].split('&nbsp; \n')
                clean.write('[' + date + ' - ' + time + ']' + '\n')

                qnaList = re.findall(r'<qco>(.*?)<h3>', str(question), re.DOTALL)
                qnaList = [item + '\n' for item in qnaList]
                for q in qnaList:
                    soup = BeautifulSoup(q, "html.parser")
                    clean.write(soup.get_text())

                lastSubQuestion = regex.findall(r'(?r)<qco>(.*?)', str(question), re.DOTALL)
                soup = BeautifulSoup(lastSubQuestion[0], "html.parser")
                clean.write(soup.get_text() + '\n')

nextUrl = pageScraper(homeUrl)
'''
while nextUrl:
    nextUrl = pageScraper(nextUrl)
'''