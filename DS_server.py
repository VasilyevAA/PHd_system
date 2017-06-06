#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import json
from DS_AES_256 import AESCipher


secretKey = 'TopSecretKey'



cipher = AESCipher(key=secretKey)
sock = socket.socket()
sock.bind(('', 9090))
sock.listen(2)
conn, addr = sock.accept()

print('connected:', addr)

while True:
    raw_data = conn.recv(2048)
    if not raw_data:
        print('WARNING: no data')
    data = json.loads(raw_data.decode("utf-8"))
    print(data)
    print(data['data'])
    def_data_get = cipher.decrypt(data['data'])
    print(def_data_get)
    print(type(def_data_get))
    conn.send(b'OK')

conn.close()