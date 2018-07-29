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
        date, question = q.split('</dco>')
        date, time = date.split('&nbsp; \\n')
        out.write('[' + date + ' - ' + time + ']' + '\n')
        soup = BeautifulSoup(question, "html.parser")
        
        question = question.split('<\qco>')
        for sub in question:
            sub = sub.strip('<qco>')
            soup = BeautifulSoup(sub, "html.parser")
            out.write(soup.get_text() + '\n\n')

    #Last entry always falls in a different pattern, so parsing right-to-left is faster.
    lastQ = regex.findall(r'(?r)<h3> <dco>(.*?)<A NAME="bottom">', str(respData))
    
    for lq in lastQ:
        date, lastQuestion = lq.split('</dco>')
        date, time = date.split('&nbsp; \\n')
        out.write('[' + date + ' - ' + time + ']' + '\n')
        question = lq.split('<\qco>')
        for sub in question:
            soup = BeautifulSoup(sub, "html.parser")
            out.write(soup.get_text() + '\n\n')

    nextUrlData = regex.findall(r'(?r)<a href="questions-20(.*?).html">', str(respData))
    
    #The oldest page won't have a link at the bottom. This is a temporary workaround.
    if len(nextUrlData[0]) > 6:
        return

    year, month = nextUrlData[0].split("-")
    nextUrl = 'http://www.billwurtz.com/questions/questions-20' + year + '-' + month + '.html'

    print('Parsing ' + nextUrl)
    out.close()
    
    return nextUrl

nextUrl = pageScraper(homeUrl)

while nextUrl:
    nextUrl = pageScraper(nextUrl)
