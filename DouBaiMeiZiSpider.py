#!/usr/bin/env python
# _*_ codeing: utf-8 _*_

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
        self.url   = url
        self.path  = path
        self.count = count
        self.thread_stop = False

    def run(self):
        while not self.thread_stop:
            time.sleep(1)
            socket = urllib2.urlopen(self.url)
            image = socket.read()
            print self.url[-15:]
            f = open(self.path + os.sep + str(self.count) + self.url[-15:], 'wb')
            f.write(image)
            socket.close()
            f.close()
            self.thread_stop = True

    def stop(self):
        self.thread_stop = True


def handle(page, t, path):
    url = 'http://www.dbmeizi.com/?p=%s' % page
    socure_code = urllib2.urlopen(url)
    soup = BeautifulSoup(socure_code)
    my_girl = soup.find_all('img')

    if my_girl == []:
        print u'已经全部抓取完毕'
        sys.exit()

    print u'开始抓取...'

    for girl in my_girl:
        link = girl.get('src') or girl.get('data-src')
        download = PageDownload(link, path, t)
        download.start()


for i in range(0, 21):
    handle(i, i, new_path)

print u'抓取结束...'
