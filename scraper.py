import urllib.request
import urllib.parse
import re
import regex

homeUrl = 'http://www.billwurtz.com/questions/questions.html'
rawFileName = 'recent-questions-raw.txt'
cleanFileName = 'recent-questions.txt'

def pageScraper(url):
    resp = urllib.request.urlopen(url)
    respData = resp.read()
    questions = re.findall(r'<h3>(.*?)</br></br>', str(respData))

    #The file used to store the raw HTML entries. This has to go through another function to strip all remaining tags
    out = open(rawFileName, 'a')

    for q in questions:
        q = stripTags(q)
        out.write(q + '\n\n')

    #Last entry always falls in a different pattern, so parsing right-to-left is faster.
    lastQuestion = regex.findall(r'(?r)<h3>(.*?)<A NAME="bottom">', str(respData))
    out.write(lastQuestion[0] + '\n\n')

    nextUrlData = regex.findall(r'(?r)<a href="questions-20(.*?).html">', str(respData))
    
    #The oldest page won't have a link at the bottom. This is a temporary workaround.
    if len(nextUrlData[0]) > 6:
        return

    year, month = nextUrlData[0].split("-")
    nextUrl = 'http://www.billwurtz.com/questions/questions-20' + year + '-' + month + '.html'

    print('Parsing ' + nextUrl)
    out.close()
    
    return nextUrl

def stripTags(question):
    out = open(cleanFileName, 'a')

nextUrl = pageScraper(homeUrl)

while nextUrl:
    nextUrl = pageScraper(nextUrl)
