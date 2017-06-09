#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time
import os
import threading
import random


path1 = ['1\\test1.1','1\\test1.2']
path2 = ['2\\test2.1','2\\test2.2']
path3 = ['3\\test3.1','3\\test3.2']

allProcesses = []
pathAll = [path1, path2, path3]

ip_cam_port = [80, 21, 20, 100, 101, 105, 9000, 8000, 3535]

class WriteData(threading.Thread):
    def __init__(self, arr):
        threading.Thread.__init__(self)
        self.arr = arr

    def run(self):
        i = 1
        for pt in self.arr:
            print(os.getcwd() + '/' + pt)
            lol = os.getcwd()
            for x in range(0, 1000):
                f = open(str(lol) + '/' + pt, 'a+')
                f.seek(len(f.read()))
                f.write('%s %s file for process %s: {From:%s      To:%s}\n' % (datetime.datetime.now(), i, self.getName(), '111.11.11.100.9000', '192.168.0.'+(str(random.randint(15, 35)))+'.'+(str(ip_cam_port[random.randint(5, 9000)%len(ip_cam_port)]))))
                f.close()
                time.sleep(5)

            i += 1
            time.sleep(5)

for x in range(0, 3):
    t = str(os.getcwd()) +'\\' + str(x+1)
    try:
        os.makedirs(t)
    except OSError:
        print('папка существует:'+t)

for path in pathAll:
    p = WriteData(path)
    allProcesses.append(p)
    p.start()

print('danger                         :'+str(os.getpid()))
