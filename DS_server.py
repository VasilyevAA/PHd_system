#!/usr/bin/env python
# -*- coding: utf-8 -*-

import queue
import threading
import socket
import random
from subprocess import Popen, PIPE
import re
from DS_AES_256 import AESCipher
from SocketFactory import SocketReader, SocketSender



secretKey = 'TopSecretKey'

ip_port = 9090

ip_cam_arr = ['192.168.0.20', '192.168.0.21', '192.168.0.22', '192.168.0.32', '192.168.0.33', '192.168.0.34']
sensor_arr = ['192.168.0.55', '192.168.0.56', '192.168.0.57', '192.168.0.58', '192.168.0.59', '192.168.0.77']
mqtt_arr = '192.168.0.100'
total_camera_container = 0
total_sensor_container = 0

ip_cam_port = {80, 21, 20}
mqtt_port = {80, 22, 60000}
sensor_port = {5566, 23}


def check_port(host):
    while True:
        port = random.randint(30000, 60000)
        # Создаем новый сокет
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.01)
        try:
            sock.connect((host, port))
        except:
            #print("Порт %s закрыт." % port + '\n' + '--------')
            return port
        else:
            #print("Порт %s открыт!" % port + '\n' + '--------')
            sock.close() # Закрываем сокет


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



class DockerWorker(threading.Thread):
    def __init__(self, docker_queue, queue_read, queue_send, ip_addres):
        threading.Thread.__init__(self)
        self.ip_addres = ip_addres
        self.queue_read = queue_read
        self.queue_send = queue_send

    def run(self):
        global total_camera_container
        global total_sensor_container
        while True:
            if not (self.queue_read.empty()):
                message_from_deffender = self.queue_read.get()



                destination_resource_ip = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', message_from_deffender['destination_resource'], re.DOTALL)[0]
                destination_resource_port = message_from_deffender['destination_resource'][len(destination_resource_ip) + 1:]
                print('%s test destination %s'%(destination_resource_ip, destination_resource_port))

                attack_source_ip = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', message_from_deffender['source'], re.DOTALL)[0]
                attack_source_port = message_from_deffender['source'][len(attack_source_ip) + 1:]
                print('%s test atack %s' % (attack_source_ip, attack_source_port))

                docker_command = ''
                if destination_resource_ip in ip_cam_arr and destination_resource_port in ip_cam_port:
                    camera_name = 'ds_camera_%s' % total_camera_container
                    total_camera_container += 1
                    docker_command = 'docker run -di --name=%s -h "ip_camera" ds_camera'%(camera_name)
                    for i in ip_cam_port:
                        docker_command = docker_command[:docker_command.find('-di')]+" -p %s:%s"%(check_port(self.ip_addres), i)+docker_command[docker_command.find('-di'):]


                    do_docker_command(docker_command)


                elif destination_resource_ip in mqtt_arr and destination_resource_port in mqtt_port:
                    mqtt_name = 'mqtt_broker_%s' % total_sensor_container
                    total_sensor_container += 1
                    docker_command = 'docker run -di --name=%s -h "mqtt_broker" ds_mqtt_broker' % (mqtt_name)
                    for i in ip_cam_port:
                        docker_command = docker_command[:docker_command.find('-di')] + " -p %s:%s" % (
                        check_port(self.ip_addres), i) + docker_command[docker_command.find('-di'):]

                    do_docker_command(docker_command)

                elif destination_resource_ip in sensor_arr and destination_resource_port in sensor_port:
                    sensor_name = 'sensor_name_%s' % total_sensor_container
                    total_sensor_container += 1
                    docker_command = 'docker run -di --name=%s -h "sensor_container" ds_sensor_container' % (sensor_name)
                    for i in ip_cam_port:
                        docker_command = docker_command[:docker_command.find('-di')] + " -p %s:%s" % (
                        check_port(self.ip_addres), i) + docker_command[docker_command.find('-di'):]

                    do_docker_command(docker_command)


                else:
                    print('attacker cant do this options')




if __name__ == "__main__":
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_addres = s.getsockname()[0]
        print(ip_addres)
        s.close()

        cipher = AESCipher(key=secretKey)
        work_queue_reader = queue.Queue()
        work_queue_sender = queue.Queue()
        docker_queue = queue.Queue()

        print('App start listning defenders')
        p = SocketReader(ip_addres, ip_port, work_queue_reader, 'DS_server_app', 1)
        p.setName('Thread - SocketReader')
        p.start()

        p = DockerWorker(docker_queue, work_queue_reader, work_queue_sender, ip_addres)
        p.setName('Thread - DockerWorker')
        p.start()

        p = SocketSender(10000, work_queue_sender)
        p.setName('Thread - SocketSender')
        p.start()


    except KeyboardInterrupt:
        print('exit combination')

        for x in threading.enumerate():
            if x != threading.current_thread():
                x.stop()

        for x in range (1, total_camera_container+1):
            print('stop ds_camera_%s' % x)
            command_docker_stop = 'docker stop ds_camera_%s' % x
            command_docker_delete = 'docker container rm ds_camera_%s' % x

        for x in range (1, total_sensor_container+1):
            print('stop ds_camera_%s' % x)
            command_docker_stop = 'docker stop ds_sensor_container_%s' % x
            command_docker_delete = 'docker container rm ds_sensor_container_%s' % x

        for x in mqtt_arr:
            print('stop ds_camera_%s' % x)
            command_docker_stop = 'docker stop ds_mqtt_broker_%s' % x
            command_docker_delete = 'docker container rm ds_mqtt_broker_%s' % x







