import re
import regex
from bs4 import BeautifulSoup

question = '<dco>7.16.18&nbsp; \n10:51 pm</dco> &nbsp;<qco> i want to become lost at sea</qco> </h3> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\nthat sounds like fun but if you get too lost you might end up on land\n'
#question = '<dco>7.6.18&nbsp; \n4:15 am</dco> &nbsp;<qco> <a href="q.php?date=201807041252">7.4.18&nbsp;&nbsp;12:52 pm</a> Are we talking about this: http://www.billwurtz.com/got-to-know-whats-going-on.mp3 \n</qco></h3> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;no<h3> <qco> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This sounds like G Major, not E.\n</qco></h3> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;that\'s right<h3> <qco> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; On what syllable are you putting Do?</qco> </h3> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;same one as you. that song is in G. \'what\'s going on\' by marvin gaye is in E.'
#qna = '<dco>7.6.18&nbsp; \n4:15 am</dco> &nbsp;<qco> <a href="q.php?date=201807041252">7.4.18&nbsp;&nbsp;12:52 pm</a> This is question #1 \n</qco></h3> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This is answer #1<h3> <qco> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This is question #2\n</qco></h3> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This is answer #2<h3> <qco> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; This is question #3</qco> </h3> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This is answer #3'

date = re.findall(r'<dco>(.*?)</dco>', str(question), re.DOTALL)
date, time = date[0].split('&nbsp; \n')
print('[' + date + ' - ' + time + ']')

qnaList = re.findall(r'<qco>(.*?)<h3>', str(question), re.DOTALL)
qnaList = [item + '\n' for item in qnaList]
for q in qnaList:
    soup = BeautifulSoup(q, "html.parser")
    print(soup.get_text())

lastSubQuestion = regex.findall(r'(?r)<qco>(.*?)', str(question), re.DOTALL)
soup = BeautifulSoup(lastSubQuestion[0], "html.parser")
print(soup.get_text() + '\n')

