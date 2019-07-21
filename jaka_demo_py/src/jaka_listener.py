#!/usr/bin/env python
#coding=utf-8
import rospy
import math
import socket
import json
import traceback
import time
#导入mgs到pkg中
from jaka_demo_py.msg import joint_data


def tcp_client():
    tcp_server_addr = ('192.168.2.208',10001)
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)

    try:
        sock.connect(tcp_server_addr)
        print "connect success"

    except Exception:
        print traceback.format_exc()
    #给机器人上电
    testDict = '{"cmdName":"power_on"}'
    sock.sendall(testDict.decode())
    recvdata = sock.recv(2048).decode()
    print "recvdata in client ",recvdata
    time.sleep(6)
    #给机器人上使能
    testDict = '{"cmdName":"enable_robot"}' 
    sock.sendall(testDict.decode())
    recvdata = sock.recv(2048).decode()
    print "recvdata in client ",recvdata
    time.sleep(3)
    #进入位置控制模式
    testDict = '{"cmdName":"servo_move","relFlag":1}'
    sock.sendall(testDict.encode())
    recvdata = sock.recv(2048).decode()
    print "recvdata in client:",recvdata
    time.sleep(1)
    j = 0
    while j < 3:  
        j = j+1   
        for i in range(1,376):
            #testDict='{"cmdName":"servo_j","jointPosition":[-0.16,0.16,-0.16, -0.16,-0.180,0.0],"relFlag":1}'
            a = '{"cmdName":"servo_j","jointPosition":'
            b =   '[-0.16,0.16,-0.16, -0.16,-0.180,0.0]'
            c =  ',"relFlag":1}'
            testDict = a+b+c
            #testDict='{"cmdName":"servo_j","jointPosition":[0.16,-0.16,0.16, 0.16,0.160,0.0],"relFlag":1}'
            #testDict = '{"cmdName":"servo_p","catPosition":[0.0,0.0,-0.1,0,0,0],"relFlag":1}'
            sock.sendall(testDict.encode())   
            recvdata = sock.recv(2048).decode()
            print "recvdata in client:", recvdata
            time.sleep(0.008)

        for i in range(1,376):
            a = '{"cmdName":"servo_j","jointPosition":'
            b =   '[0.16,-0.16,0.16, 0.16,0.160,0.0]'
            c =  ',"relFlag":1}'
            testDict = a+b+c
            #testDict='{"cmdName":"servo_j","jointPosition":[0.16,-0.16,0.16, 0.16,0.160,0.0],"relFlag":1}'
            #testDict = '{"cmdName":"servo_p","catPosition":[0.0,0.0,-0.1,0,0,0],"relFlag":1}'
            sock.sendall(testDict.encode())   
            recvdata = sock.recv(2048).decode()
            print "recvdata in client:", recvdata
            time.sleep(0.008)

    sock.close()



def callback(joint_data):
    try:
        go = str(list(joint_data.joint_data_go))
        back = str(list(joint_data.joint_data_back))

    except Exception:
        print traceback.format_exc()
    print "joint_data.joint_data_go :",str(list(joint_data.joint_data_go))
    print "joint_data.joint_data_back",str(list(joint_data.joint_data_back))
    tcp_server_addr = ('192.168.2.208',10001)
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)

    try:
        sock.connect(tcp_server_addr)
        print "connect success"

    except Exception:
        print traceback.format_exc()
    #给机器人上电
    testDict = '{"cmdName":"power_on"}'
    sock.sendall(testDict.decode())
    recvdata = sock.recv(2048).decode()
    print "recvdata in client ",recvdata
    time.sleep(6)
    #给机器人上使能
    testDict = '{"cmdName":"enable_robot"}' 
    sock.sendall(testDict.decode())
    recvdata = sock.recv(2048).decode()
    print "recvdata in client ",recvdata
    time.sleep(3)
    #进入位置控制模式
    testDict = '{"cmdName":"servo_move","relFlag":1}'
    sock.sendall(testDict.encode())
    recvdata = sock.recv(2048).decode()
    print "recvdata in client:",recvdata
    time.sleep(1)
    j = 0
    while j < 3:  
        j = j+1   
        for i in range(1,376):
            a = '{"cmdName":"servo_j","jointPosition":'
            c =  ',"relFlag":1}'
            testDict = a+go+c
            sock.sendall(testDict.encode())   
            recvdata = sock.recv(2048).decode()
            print "recvdata in client:", recvdata
            time.sleep(0.008)            

        for i in range(1,376):
            a = '{"cmdName":"servo_j","jointPosition":'
            c =  ',"relFlag":1}'
            testDict = a+back+c
            sock.sendall(testDict.encode())   
            recvdata = sock.recv(2048).decode()
            print "recvdata in client:", recvdata
            time.sleep(0.008)

    sock.close()

def listener():
    rospy.init_node('jaka_listener', anonymous=True)
    #Subscriber函数第一个参数是topic的名称，第二个参数是接受的数据类型 第三个参数是回调函数的名称
    rospy.Subscriber('joint_info', joint_data, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
    #tcp_client()

