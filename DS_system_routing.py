#!/usr/bin/env python
# -*- coding: utf-8 -*-

import queue
import socket
import threading
from subprocess import Popen, PIPE
from DS_AES_256 import AESCipher
from SocketFactory import SocketReader

secretKey = 'TopSecretKey'
ip_port = 10000



def do_docker_command(command):
    proc = Popen(
        command,
        shell=True,
        stdout=PIPE, stderr=PIPE
    )
    proc.wait()  # дождаться выполнения
    res = proc.communicate()  # получить tuple('stdout', 'stderr')
    if proc.returncode:
        print
        res[1]
    print
    'result:', res[0]


class RoutingData(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue


    def run(self):
        
        while True:
            if not work_queue.empty():
                routing_item = work_queue.get()
                return 0
                routing_command = "iptables -A INPUT --destanation $s "%(routing_item[0])



if __name__ == "__main__":

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_addr = s.getsockname()[0]
    print(ip_addr)
    s.close()

    cipher = AESCipher(key=secretKey)
    work_queue = queue.Queue()

    p = SocketReader(ip_addr, ip_port, work_queue, 'DS_routing_app', 1)
    p.setName('Thread - SocketReader')
    p.start()

    p = RoutingData(work_queue)
    p.setName('Thread - RoutingData')
    p.start()