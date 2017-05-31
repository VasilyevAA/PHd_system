#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import json

sock = socket.socket()
sock.connect(('localhost', 9090))
data = {"data":{"hostname":"192.168.7.6","ipaddress":"192.168.7.6","comment":"АдминистраторСервер", "command":"discovery"}}
raw_data = json.dumps(data, ensure_ascii=False).encode("utf-8")
sock.send(raw_data)
print(data)
print(raw_data)

return_raw_data = sock.recv(2048)
data = json.loads(return_raw_data.decode("utf-8"))
print(data)
sock.close()

