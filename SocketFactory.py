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

secretKey = 'TopSecretKey'
cipher = AESCipher(key=secretKey)

class SocketSender(threading.Thread):
    def __init__(self, ip_addr, ip_port, work_queue):
        threading.Thread.__init__(self)
        self.ip_addr = ip_addr
        self.ip_port = ip_port
        self.work_queue = work_queue

    def run(self):
        sock = socket.socket()
        sock.connect((self.ip_addr,  self.ip_port))
        while True:
            if not (self.work_queue.empty()):
                item = self.work_queue.get()
                data = {"data": item}
                raw_data = json.dumps(data, ensure_ascii=False).encode("utf-8")
                a = True
                while a:
                    print(raw_data)
                    sock.send(raw_data)
                    get_srv_data = sock.recv(2048)
                    if get_srv_data == b'OK':
                        print (get_srv_data)
                        a = False
                    else:
                        print ('Error message')
                        a = True

        sock.close()



class SocketReader(threading.Thread):
    def __init__(self, ip_addr, ip_port, work_queue, app_name, defender_count):
        threading.Thread.__init__(self)
        self.ip_addr = ip_addr
        self.ip_port = ip_port
        self.work_queue = work_queue
        self.app_name = app_name
        self.defender_count = defender_count


    def run(self):
        sock = socket.socket()
        sock.bind(('localhost', self.ip_port))
        sock.listen(self.defender_count)
        conn, addr = sock.accept()

        message_attack = 'Attack ' + self.app_name

        print('connected:', addr)

        while True:
            raw_data = conn.recv(2048)
            if not raw_data:
                print('WARNING: no data')
            test1 = str(raw_data)
            if test1.find('"}')>10 and test1.find('"}') != 0:
                test1 = test1[2:(test1.find('"}')+2)]
                data = json.loads(test1)
                try:
                    def_data_get = cipher.decrypt(data['data'])
                    def_data_get = json.loads(def_data_get)
                    def_data_get.update({'service_name': self.app_name})
                    print(def_data_get)
                    print('\n')
                    # print(type(def_data_get))
                    # print('\n\n\n')
                    self.work_queue.put(def_data_get)
                    conn.send(b'OK')
                except:
                    print('Error message')
                    conn.send(b'Error message')
            else:
                print(message_attack)
                #conn.send(message_attack)

        conn.close()













