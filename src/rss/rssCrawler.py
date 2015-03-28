import cookielib
from cookielib import CookieJar
import urllib2
import urllib2
from bs4 import BeautifulSoup
import re
import MySQLdb

db = MySQLdb.connect("localhost","root","","socnet" )

cursor = db.cursor()




cj = CookieJar()
proxy = urllib2.ProxyHandler({"http":"http://edcguest:edcguest@172.31.103.29:3128"})
opener = urllib2.build_opener(proxy,urllib2.HTTPCookieProcessor(cj))
opener2 = urllib2.build_opener(proxy,urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0')]


# def get_only_text(url):
    # page = opener2.open(url).read().decode('utf8')
    # soup = BeautifulSoup(page)
    # text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    # return soup.title.text, text
	
# contents = ""	
# html_text = opener.open('http://feeds.feedburner.com/crunchgear').read()

# soup = BeautifulSoup(html_text)
# for tag in soup.findAll("span", attrs = {"base":"http://feeds.feedburner.com/crunchgear"}):
    # contents = "".join(str(item) for item in tag.contents)
# print contents		
def rssTech():
	print 'Adding Tech feeds...',
	feed_xml = opener.open('http://www.theverge.com/rss/frontpage').read()
#print feed_xml[:10000]
	feed = BeautifulSoup(feed_xml.decode('utf8'))
	feed = BeautifulSoup(feed_xml)
	#fname = open("text.txt","wb")
	#fname.write(str(feed_xml))

	titles = map(lambda p: p.text, feed.find_all('title'))
	links = map(lambda p: p.text, feed.find_all('id'))
	contents = map(lambda p: p.text, feed.find_all('content'))
	#print titles
	#print links
#print contents
	text = []
	for content in contents:
		raw_html = content.split('<p>')[1].encode('utf8')
		cleanr =re.compile('<.*?>')
		cleantext = re.sub(cleanr,'', raw_html)
		text.append(cleantext[:500])
		#print text[0]
		#print titles[1]
		#print '-------------------'
	i=2
# for title in titles[2:]:
	# sql = """Insert into rss_rssstore(id,Title,Link) values(i,"""+title+""","""+links[i]+""")"""
		
	# cursor.execute(sql)
	# i+=1	

	
	cursor.execute("""INSERT INTO rss_rssstore(Title,Link,Content,Category) VALUES (%s,%s,%s,%s)""",(titles[1].encode("utf8"),links[1],text[0],'Tech'))	
	for title in titles[2:]:
		cursor.execute("""INSERT INTO rss_rssstore(Title,Link,Content,Category) VALUES (%s,%s,%s,%s)""",(title.encode("utf8"),links[i],text[i-1],'Tech'))
		i+=1
	
	db.commit()	
	print 'Done'



def rssFinance():
	print 'Adding Finance feeds... ',
	feed_xml = opener.open('http://economictimes.indiatimes.com/rssfeeds/13352306.cms').read()
#print feed_xml[:10000]
	feed = BeautifulSoup(feed_xml.decode('utf8'))
	#fname = open("text.txt","wb")
	#fname.write(str(feed_xml))

	titles = map(lambda p: p.text, feed.find_all('title'))
	links = map(lambda p: p.text, feed.find_all('link'))
	#print titles[0:4]
	#print links[0:4]

	contents = map(lambda p: p.text, feed.find_all('description'))
	j=0
	text = []
	for content in contents:
		raw_html = content.encode('utf8')
		cleanr =re.compile('<.*?>')
		cleantext = re.sub(cleanr,'', raw_html)
		text.append(cleantext)
		#print text[j]
		#print '-------------------'
		j+=1

	i=2
#cursor.execute("""INSERT INTO rss_rssstore(Title,Link,Content,Category) VALUES (%s,%s,%s,%s)""",(titles[2].encode("utf8"),links[2],text[0],'Finance'))	
	for title in titles[2:]:
		cursor.execute("""INSERT INTO rss_rssstore(Title,Link,Content,Category) VALUES (%s,%s,%s,%s)""",(title.encode("utf8"),links[i],text[i-1],'Finance'))
		i+=1
	
	db.commit()	
	print 'Done'
	
	
