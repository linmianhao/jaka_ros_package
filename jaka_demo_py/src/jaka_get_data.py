#!/usr/bin/env python
#coding=utf-8
import socket
import rospy
import traceback
import time
#导入入自定义的数据类型
from sensor_msgs.msg import JointState
from std_msgs.msg import Header




def get_full_data():
    tcp_server_addr = ('192.168.2.208',10000)
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)

    try:
        sock.connect(tcp_server_addr)
        print "connect to  port 10000 successfully"
    except Exception:
        print traceback.format_exc()
        sock.close()
    
    #send something to client
    #sock.sendall()
    while True:
        recvdata = sock.recv(2048)
        #time.sleep(0.008)
        # 分割字符串获得数据 
        #print "receive data from port 10000:", (recvdata.split())
        joint_actual_position_str = recvdata.split()
        joint_actual_position = joint_actual_position_str[0].split(":")     

        print "len of joint_actual_position:",len(joint_actual_position)
        if len(joint_actual_position) > 1 :
            print "joint_actual_position:",joint_actual_position[1]

    sock.close()

def get_joint_data():
    # 端口固定为10000 ，IP为机器人的IP
    tcp_server_addr = ('192.168.2.208',10000)
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
    try:
        sock.connect(tcp_server_addr)
        print "connect to  port 10000 successfully"
    except Exception:
        print traceback.format_exc()
        sock.close()
    
    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    rospy.init_node('joint_state_publisher',anonymous = True)
    #服务器是80ms发送一次，所以这里填12.5HZ
    rate = rospy.Rate(12.5) 
    joint_position_str = JointState()
    joint_position_str.header = Header()
    joint_position_str.header.stamp = rospy.Time.now()
    joint_position_str.name = ['joint_1', 'joint_2', 'joint_3', 'joint_4','joint_5','joint_6']
    # 关节的角度，单位是弧度
    joint_position_str.position = [0.0,0.0,0,0,0,0]
    joint_position_str.velocity = []
    joint_position_str.effort = []

    while not rospy.is_shutdown():   
        recvdata = sock.recv(2048)
        # 对进行字符串分割recvdata，获得关节数据，如果要获得其他数据，可以对recvdata进行分割        
        joint_actual_position_str = recvdata.split()
        joint_actual_position = (joint_actual_position_str[0].split(":"))[1]
        if len(joint_actual_position) > 1 :           
            for i in range(0,6):
                joint_position = joint_actual_position[1:-1].split(",")
                joint_position_str.position[i] = float(joint_position[i])/180*3.14159
                #print " joint_position_str.position[i] :", joint_position_str.position[i]               
        joint_position_str.header.stamp = rospy.Time.now()
        pub.publish(joint_position_str)
        rate.sleep()


if __name__ == '__main__':
    get_joint_data()


 


#joint_actual_position: ['joint_actual_position', '(12.960000000000008,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)']
#joint_actual_position[1] = '(12.960000000000008,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)' 是一个字符串
# joint_actual_position_str: ['joint_actual_position:(0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)', 'actual_position:(656.0,22.5,11.500000000000016,89.99999999999999,-0.0,0.0,0.0,0.0,0.0)', 'din:
# (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)', 'dout:(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
# ,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)', 'ain:((0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0))', 'aout:((0.0,0.0,0.0,0.0,0.0
# ,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0))', 'tio_din:(0,0,0,0,0,0,0,0)', 'tio_dout:(0,0,0,0,0,0,0,0)', 'tio_ain:(0.0,)', 'task_state:(4)', 'homed:(1,1,1,1,1,1,0,0,0)', 'task_mode:(1
# )', 'interp_state:(1)', 'enabled:(1)', 'estop:(0)', 'paused:(0)', 'rapidrate:(1.0)', 'current_tool_id:(0)', 'protective_stop:(0)', 'on_soft_limit:(0)', 'hard_estop:(1)', 'tool_position:(
# (0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0))', 'drag_near_limit:((0,0,0,0,0,0))']\
# def chuli():
#     a = '(12.960000000000008,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)'
#     b = a[1:-1].split(",")
    
#     print "type(b):",type(b)
#     print "a[1]",a[1:-1]
#     print "type(b[1])",type(b[1])
#     for i in b:
#         print "i\n",i
#         print "type(b[1])",type(float(i))
# b: ['0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0']