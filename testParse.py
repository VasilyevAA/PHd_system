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
import random

secretKey = 'TopSecretKey'


def parseLog(raw):
    ip_list = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,6}', raw, re.DOTALL)
    raw = {'sourse':ip_list[0], 'destination_resource':ip_list[1]}
    return (json.dumps(raw, ensure_ascii=False).encode("utf-8"))


str1 = 'ip 123.22.11.1.1 asd.123.qwe.1 1.1.1.1 80.1.233.44 asdxzv sad .asdasd'
ip_list = re.findall ('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', str1, re.DOTALL)



cipher = AESCipher(key=secretKey)
print (type(str1))
print (str1)
print (type(json.loads(parseLog(str1))))
print (json.loads(parseLog(str1)))
qwe = json.loads(parseLog(str1))
qwe.update({'service_name': 'AgentDefender'})
print (qwe)
print('ololo %s'%('192.168.1.'+(str(random.randint(1, 255)))))

enc_line_data = cipher.encrypt(parseLog(str1))
print ('   '+enc_line_data)
enc_line_data = json.dumps(enc_line_data, ensure_ascii=False).encode("utf-8")

print (enc_line_data)
print (type(enc_line_data))


