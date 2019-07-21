#!/usr/bin/env python
#coding=utf-8
import socket
import json
import rospy
import traceback
import time
#倒入自定义的数据类型
from jaka_demo_py.msg import gps
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
    
    testDict = '{"cmdName":"power_on"}'
    sock.sendall(testDict.decode())
    recvdata = sock.recv(2048).decode()
    print "recvdata in client ",recvdata
    time.sleep(6)

    testDict = '{"cmdName":"enable_robot"}' 
    sock.sendall(testDict.decode())
    recvdata = sock.recv(2048).decode()
    print "recvdata in client ",recvdata
    time.sleep(3)

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
            b =   '[0.16,-0.16,0.16, 0.16,0.180,0.0]'
            c =  ',"relFlag":1}'
            testDict = a+b+c
            #testDict='{"cmdName":"servo_j","jointPosition":[0.16,-0.16,0.16, 0.16,0.160,0.0],"relFlag":1}'
            #testDict = '{"cmdName":"servo_p","catPosition":[0.0,0.0,-0.1,0,0,0],"relFlag":1}'
            sock.sendall(testDict.encode())   
            recvdata = sock.recv(2048).decode()
            print "recvdata in client:", recvdata
            time.sleep(0.008)

    sock.close()


def talker():
    #Publisher 函数第一个参数是话题名称，第二个参数 数据类型，现在就是我们定义的msg 最后一个是缓冲区的大小
    #queue_size: None（不建议）  #这将设置为阻塞式同步收发模式！
    #queue_size: 0（不建议）#这将设置为无限缓冲区模式，很危险！
    #queue_size: 10 or more  #一般情况下，设为10 。queue_size太大了会导致数据延迟不同步。
    pub = rospy.Publisher('gps_info', gps , queue_size=10)
    rospy.init_node('jaka_talker', anonymous=True)
    #更新频率是1hz
    rate = rospy.Rate(1) 
    x=1.0
    y=2.0
    state='working'
    while not rospy.is_shutdown():
        #计算距离
        rospy.loginfo('Talker: GPS: x=%f ,y= %f',x,y)
        pub.publish(gps(state,x,y))
        x=1.03*x
        y=1.01*y
        rate.sleep()

def talker1():
    #Publisher 函数第一个参数是话题名称，第二个参数 数据类型，现在就是我们定义的msg 最后一个是缓冲区的大小
    #queue_size: None（不建议）  #这将设置为阻塞式同步收发模式！
    #queue_size: 0（不建议）#这将设置为无限缓冲区模式，很危险！
    #queue_size: 10 or more  #一般情况下，设为10 。queue_size太大了会导致数据延迟不同步。
    pub = rospy.Publisher('joint_info', joint_data , queue_size=10)
    rospy.init_node('jaka_talker', anonymous=True)
    #控制器的控制周期是8ms,所以这里填125
    rate = rospy.Rate(125) 
    joint_data_go = [-0.16,0.16,-0.16, -0.16,-0.180,0.0]
    joint_data_back = [0.16,-0.16,0.16, 0.16,0.180,0.0]
    while not rospy.is_shutdown():       
        rospy.loginfo('Talker: joint_data joint_data_go=%s ,joint_data_back= %s',str(joint_data_go),str(joint_data_back))
        pub.publish(joint_data(joint_data_go,joint_data_back))
        rate.sleep()        




if __name__ == '__main__':
    talker1()
    #tcp_client()
    #handle_json_str()


################################ testDict ################################
# {"cmdName":"power_on"}
#{"cmdName":"enable_robot"}
# 
# {"cmdName":"load_program","programName":"vision_test.ngc"}
# {"cmdName":"get_loaded_program"}
# {"cmdName":"play_program"}
# {"cmdName":"pause_program"}
# {"cmdName":"resume_program"}
# {"cmdName":"stop_program"}
# {"cmdName":"get_program_state"}
# {"cmdName":"joint_move","jointPosition":[100,60,70,40,50,10],"speed":10.0}
# {"cmdName":"get_robot_state"}
# {"cmdName":"quit"}
# 
# {"cmdName":"disable_robot"}
# {"cmdName":"power_off"}  
#{"cmdName":"servo_j","jointPosition":[joint1,joint2,joint3,joint4,joint5,joint6],"relFlag":0}
#{"cmdName":"servo_p","catPosition":[10,50,10,0,0,0],"relFlag":0}
#{"cmdName":"servo_move","relFlag":1}
#{"cmdName":"torque_feedforward","grvCurrent":[0.1,0.1,0.1,0.1,0.1,0.1],"includeGrvFlag":1}
#{"cmdName":"get_data"}
#{"cmdName":"rapid_rate","rate_value":0.2}
#{"cmdName":"torque_control_enable","enable_flag":1}
#{"cmdName":"joint_move","jointPosition":[joint1,joint2,joint3,joint4,joint5,joint6],"speed":20.0, "relFlag":0}
# testDict = '{"cmdName":"torque_feedforward","grvCurrent":[0, 100, 0.0, 0.0, 0.0, 0.0],"includeGrvFlag":2}'
# testDict = '{"cmdName":"shutdown"}'
# testDict = '{"cmdName":"power_on"}'
# #testDict = '{"cmdName":"enable_robot"}'
# testDict = '{"cmdName":"joint_move","jointPosition":[100,60,70,40,50,10],"speed":10.0,"relFlag":0}'
# testDict = '{"cmdName":"joint_move","jointPosition":[20,0,0,0,0,0],"speed":10.0,"relFlag":1}'
# sock.sendall(testDict.encode())
# recvdata = sock.recv(2048).decode()
# print "recvdata in client",recvdata