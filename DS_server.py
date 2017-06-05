#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import json
from DS_AES_256 import AESCipher

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
    data['data']['comment'] = data['data']['comment'].upper()
    print(data['data']['comment'])
    aw_data = json.dumps(data, ensure_ascii=False).encode("utf-8")
    print(type(aw_data))
    conn.send(aw_data)

conn.close()