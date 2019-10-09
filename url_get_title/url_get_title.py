# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import threading
import Queue
import time

with open('url.txt') as f:
    l = f.readlines()


def btdk(url):
    try:
        res  = requests.get(url, timeout = 10)
        res.encoding = res.apparent_encoding
        html = res.text
        #html = requests.get(url, timeout = 10).text
    except:
        html = '<html><title>%s</title><meta name="keywords" content="" /><meta name="description" content="" /></html>'%url
    soup = BeautifulSoup(html.lower(),"html.parsar")
    t = soup.title.text.encode('utf8','ignore')
    try:
        k = soup.find(attrs={"name":"keywords"})['content'].encode('utf8','ignore')
    except:
        k = ""
    try:
        d = soup.find(attrs={"name":"description"})['content'].encode('utf8','ignore')
    except:
        d = ""

    return t,d,k


class MyThread(threading.Thread):

    def __init__(self, queue, url):
        threading.Thread.__init__(self)
        self.queue = queue
        self.url = url

    def run(self):
        while True:
            url = self.queue.get()
            t,k,d = btdk(url)
            with open('tdk.txt', 'a+') as s:
                line = url+'#'+t+'#'+'\n'
                s.writelines(line)
            self.queue.task_done()


def test(l, ts=4):
    ll = [i.rstrip() for i in l]
    for j in range(ts):
        t = MyThread(queue,ll)
        t.setDaemon(True)
        t.start()
    for url in ll:
        queue.put(url)
    queue.join()
if __name__ == '__main__':
    queue = Queue.Queue()
    start = time.time()
    test(l,4)
    end = time.time()
    print '共耗时:%s秒' % (end - start)
