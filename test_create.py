#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time
import os
import threading


path1 = ['1\\test1.1','1\\test1.2']
path2 = ['2\\test2.1','2\\test2.2']
path3 = ['3\\test3.1','3\\test3.2']

allProcesses = []
pathAll = [path1, path2, path3]

class WriteData(threading.Thread):
    def __init__(self, arr):
        threading.Thread.__init__(self)
        self.arr = arr

    def run(self):
        i = 1
        for pt in self.arr:
            print(os.getcwd() + '/' + pt)
            lol = os.getcwd()
            for x in range(0, 100):
                f = open(str(lol) + '/' + pt, 'a+')
                print(f.read())
                f.seek(len(f.read()))
                f.write('%s    %s file for process %s: %s\n' % (datetime.datetime.now(), i, self.getName(), x))
                f.close()
                time.sleep(2)

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
