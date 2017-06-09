#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import json
import datetime
import time
import os
import threading
import queue
import re
from DS_AES_256 import AESCipher
from SocketFactory import SocketSender

secretKey = 'TopSecretKey'
allProcesses = []
DS_ip_dest = '127.0.0.1'
ip_port = 9090







def parseLog(raw):
    ip_list = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,6}', raw, re.DOTALL)
    raw = {'source':ip_list[0], 'destination_resource':ip_list[1]}
    return (raw)

class ReadLogData(threading.Thread):
    def __init__(self, path, work_queue):
        threading.Thread.__init__(self)
        self.path = path
        self.work_queue = work_queue

    def run(self):
        try:
            print(self.path)
            files = os.listdir(self.path)
            cipher = AESCipher(key=secretKey)
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
                                #print('row: %s, data: %s'%(i, line))
                                send_dict = parseLog(line)
                                send_dict.update({'service_name':'AgentDefender'})
                                #print(send_dict)
                                enc_line_data = cipher.encrypt(json.dumps(send_dict, ensure_ascii=False).encode("utf-8"))
                                self.work_queue.put(enc_line_data)
                                maxRowFile = i

                        files = os.listdir(self.path)
                        files = [os.path.join(self.path, file) for file in files]
                        maxRow=maxRowFile
                        if pathToFile != max(files, key= os.path.getctime):
                            pathToFile = max(files, key= os.path.getctime)
                            maxRow=int(-1)

                        f.close()
                        time.sleep(10)

                except KeyboardInterrupt:

                    print('Поток %s был остановен' % (self.getName()))
        except:
            print('No idea!!!!')


if __name__ == "__main__":
    pathAll = []
    for x in range(0, 3):
        t = str(os.getcwd()) + '\\' + str(x + 1)
        pathAll.append(t)


    print('Read all configure parametr')
    work_queue = queue.Queue()
    for path in pathAll:
        p = ReadLogData(path, work_queue)
        p.setName('Thread - ReadLogData:'+path)
        allProcesses.append(p)
        p.start()
        print('Started Thread - ReadLogData:'+path)


    p = SocketSender(DS_ip_dest, ip_port, work_queue)
    p.setName('Thread - SocketSender')
    allProcesses.append(p)
    p.start()
    print('Started Thread - SocketSender')




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

