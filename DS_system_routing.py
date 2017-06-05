#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import multiprocessing
import os
from DS_AES_256 import AESCipher

def do_this(what):
    whoami(what)

def whoami(what):
    t1 = datetime.datetime.now()
    for i in range(0, 100):
        x = i*i
        if(x%1000000==0):
            print('{}: Start time {}'.format(datetime.datetime.now(), x))
    print("Process %s says: %s" % (os.getpid(), what))
    print('Start time %s' % t1)

if __name__ == "__main__":
    whoami("I'm the main program")
    for n in range(4):
        p = multiprocessing.Process(target=do_this,
          args=("I'm function %s" % n,))
        p.start()
        print('danger                         :'+os.getcwd()+'/')