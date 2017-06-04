#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time
import multiprocessing
import os
import threading


path1 = ['dir1/test1.1','dir1/test1.2']
path2 = ['dir2/test2.1','dir2/test2.2']
path3 = ['dir3/test3.1','dir3/test3.2']

allProcesses = []
pathAll = [path1, path2, path3]

def createAndWrite(path):
    i=1
    for pt in path:
        f = open(os.getcwd()+'/'+pt, 'r+')
        print(os.getcwd()+'/'+pt)
        for x in range(0,10):
            f.write('%s    %s file for process %s: %s\n'%(datetime.datetime.now(), i, os.getpid(), x))

        i+=1
        time.sleep(5)


if __name__ == "__main__":
    for path in pathAll:
        #p = multiprocessing.Process(target=createAndWrite, args=path)
        #allProcesses.append(p)
        #p.start()
    #print('danger                         :'+os.getpid())
