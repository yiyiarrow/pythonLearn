#!/usr/bin/env python
# _*_ coding: utf-8 _*_

from bs4 import BeautifulSoup
import os
import sys
import urllib2
import time
import threading
# import random
reload(sys)
sys.setdefaultencoding('utf8')

path1 = os.getcwd()
global new_path
new_path = os.path.join(path1, u'豆瓣妹子')
if not os.path.isdir(new_path):
    os.mkdir(new_path)


class PageDownload(threading.Thread):
    def __init__(self, url, path, count):
        threading.Thread.__init__(self)
        self.url = url
        self.path = path
        self.count = count
        self.thread_stop = False


    def run(self):
        while not self.thread_stop:
            time.sleep(1)
            headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
            req = urllib2.Request(self.url, headers=headers) 
            socket = urllib2.urlopen(req)
            image = socket.read()
            print self.url
            f = open(self.path + os.sep + str(self.count) + self.url[-15:], 'wb')
            f.write(image)
            socket.close()
            f.close()
            self.thread_stop = True

    def stop(self):
        self.thread_stop = True


global total_photos
total_photos = 0


def handle(page, t, path):
    i = 0
    global total_photos
    url = 'http://www.dbmeinv.com/?pager_offset=%s' % page
    print url
    source_code = urllib2.urlopen(url)
    soup = BeautifulSoup(source_code)
    my_girl = soup.find_all('img')

    if my_girl == []:
        print u'已经全部抓取完毕'
        sys.exit()

    print u'开始抓取第%d页...' % page

    for girl in my_girl:
        i += 1
        link = girl.get('src') or girl.get('data-src')
        download = PageDownload(link, path, t)
        time.sleep(6)
        download.start()

    time.sleep(2)	
    print u"第%d页%d张" % (page, i)
    total_photos += i


if __name__ == '__main__':
    # global total_photos
    for i in range(1, 3):
        handle(i, i, new_path)

    print u'抓取结束...共%d张！' % total_photos
