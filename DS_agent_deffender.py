#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import json
import datetime
import time
import os
import threading


allProcesses = []
pathAll = []
for x in range(0, 3):
    t = str(os.getcwd()) +'\\' + str(x+1)
    pathAll.append(t)

class ReadLogData(threading.Thread):
    def __init__(self, path):
        threading.Thread.__init__(self)
        self.path = path

    def run(self):
        print(self.path)
        files = os.listdir(self.path)
        if files:
            try:
                files = [os.path.join(self.path, file) for file in files]
                pathToFile = max(files, key= os.path.getctime)
                maxRow = 0

                f = open(pathToFile, 'r')
                for i, line in enumerate(f):
                    maxRow = i
                f.close()

                while (True):
                    f = open(pathToFile, 'r')
                    maxRowFile = maxRow
                    for i, line in enumerate(f):
                        if i > maxRow:
                            print('row: %s, data: %s'%(i, line))
                            maxRowFile = i

                    files = os.listdir(self.path)
                    files = [os.path.join(self.path, file) for file in files]
                    maxRow=maxRowFile
                    if pathToFile != max(files, key= os.path.getctime):
                        pathToFile = max(files, key= os.path.getctime)
                        maxRow=int(-1)

                    f.close()

            except KeyboardInterrupt:

                print('Поток %s был остановен' % (self.getName()))



if __name__ == "__main__":

    for path in pathAll:
        p = ReadLogData(path)
        allProcesses.append(p)
        p.start()

    print('danger                         :'+str(os.getpid()))





































# sock = socket.socket()
# sock.connect(('localhost', 9090))
# data = {"data":{"hostname":"192.168.7.6","ipaddress":"192.168.7.6","comment":"АдминистраторСервер", "command":"discovery"}}
# raw_data = json.dumps(data, ensure_ascii=False).encode("utf-8")
# sock.send(raw_data)
# print(data)
# print(raw_data)
#
# return_raw_data = sock.recv(2048)
# data = json.loads(return_raw_data.decode("utf-8"))
# print(data)
# sock.close()

