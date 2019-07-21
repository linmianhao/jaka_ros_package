#include "ros/ros.h"
#include "std_msgs/String.h"
#include <sensor_msgs/JointState.h>
#include <boost/thread.hpp>
#include <sstream>
#include <vector>
#include "robot.h"
#include "robot_client.h"
#define JNUMBER 6
std::vector<float> pos(JNUMBER,0.0);


void updateOringinPos(const sensor_msgs::JointState& msg)
{
  for(int i=0;i<JNUMBER;i++)
  pos[i]=msg.position[i];
}


int main(int argc, char **argv)
{

  ros::init(argc, argv, "joint_states_pub");
  ros::NodeHandle n;
  ros::Publisher chatter_pub = n.advertise<std_msgs::String>("count", 1000);
 // ros::Subscriber sub=n.subscribe("/joint_path_command",10,chatterCB);

  int count=0;
  ros::Rate loop_rate(125);
  Robot robot("192.168.0.101:50051");
  
  pos[0]=33.0737;
  pos[1]=55.0518;
  pos[2]=-107.8239;
  pos[3]=163.9009;
  pos[4]=135.3886;
  pos[5]=92.0091;
  
  robot.start();

 // ros::Subscriber sub=n.subscribe("/joint_states", 1000, updateOringinPos);
 int reply=robot.ServoJEnable(true);
 std::cout<<"servoj enable "<<reply<<std::endl;
  
  // SubscribeAndPublish test("192.168.2.60:50051");  
  // ros::MultiThreadedSpinner s(2);  //多线程
  // ros::spin(s);  
 while (ros::ok())
  {
   std_msgs::String msg;
   pos[1]-=0.06;
  // ++count;
   if(pos[1]>0)
   {
     std::stringstream ss;
     ss << "hello world " << count;
     msg.data = ss.str();
     chatter_pub.publish(msg);
     robot.servoJMove(pos,8);
     ros::spinOnce();
        
     loop_rate.sleep();
   }
   else
    break;
  }
  printf("sleeping!\n");
  sleep(30);
  printf("enable shut down!\n");
  
 reply=robot.ServoJEnable(false);
 std::cout<<"servoj enable "<<reply<<std::endl;
//  robot.stop();
 return 0;
}
