#include "ros/ros.h"
#include "std_msgs/String.h"
#include <sensor_msgs/JointState.h>
#include "trajectory_msgs/JointTrajectory.h"
#include "trajectory_msgs/JointTrajectoryPoint.h"
#include <boost/thread.hpp>
#include <sstream>
#include <vector>
#include "robot.h"
#include "robot_client.h"
#include <cstdio>
#include "cubicSpline.h"
#define JNUMBER 6
#define PI 3.1415926
#define AXIS_COUNT 6

using namespace std;

vector<vector<double>> all_points;
vector<float> pos(JNUMBER,0.0);


void chatterCB(const trajectory_msgs::JointTrajectory& msg)
{
	if((int)msg.points.size() != 0)
	{
		cubicSpline spline;
		double time_nsecs=0.0;
		int points_count=0;
		double joint_positions[6] {0.0};
		double right_bound=0;
		ROS_INFO("get the joint_path_command ");
		//    ofstream originFile;
		//    originFile.open("origin2.csv",ios::out | ios::trunc);
		//    originFile<<"time"<<","<<"pos2"<<","<<"vel2"<<","<<"ace2"<<","<<endl;
		std::basic_string<char> jointname=msg.joint_names[0] ;
		points_count= msg.points.size();                        //获取规划后点的个数
		double *Time=new double[points_count];              //划分数组
		double *data_arr=new double[points_count];
		for (int j=0; j < AXIS_COUNT; j++)
		{
			for (int i{}; i < points_count; i++)
			{

				data_arr[i]=msg.points[i].positions[j];
				Time[i]=((double)msg.points[i].time_from_start.toSec());
				//ROS_INFO("%f",((double)msg.points[i].time_from_start.toSec()));
				//             originFile<<msg.points[i].time_from_start.toSec()<<","<<msg.points[i].positions[j]<<","<<msg.points[i].velocities[j]<<","<<msg.points[i].accelerations[j]<<endl;
			} 
			//将各轴数据分开
			//        originFile<<" "<<","<<" "<<","<<" "<<","<<" "<<endl;
			spline.loadData(Time,data_arr,points_count,0,0, cubicSpline::BoundType_First_Derivative);
			double x_out = 0;
			double y_out = 0;
			//ROS_INFO("%f",(double)msg.points[points_count-1].time_from_start.toSec()); 

			vector<double> single_axis_points;

			double step = 0.008;  //default 0.004
			for(double i=0; i<=(((double)msg.points[points_count-1].time_from_start.toSec())); i=i+step)
			{
				x_out = x_out + step;
				spline.getYbyX(x_out, y_out); //x是时间，y是点
				single_axis_points.push_back(y_out); //get points in single axis
			}
			spline.oFile<<" "<<","<<" "<<","<<" "<<","<<" "<<endl;
			all_points.push_back(single_axis_points); //pull all point together. rows represent axis
		}

		//                cout << all_points.size() << endl;
		//		cout << all_points[0].size() << endl;
		//
		//		//print 6 axis point in same time stamp, should change later. should be sent to the sj interface
		//		for (int j=0; j<all_points[0].size(); j++)
		//		{
		//			for(int i=0; i<all_points.size(); i++)
		//				cout << all_points[i][j] << " ";
		//			cout << endl;
		//		}

	}
}



void updateOringinPos(const sensor_msgs::JointState& msg)
{
	for(int i=0;i<JNUMBER;i++)
		pos[i]=msg.position[i];
}

//弧度转换角度
double radian_to_angle(double rad)
{
	double result =(rad * 180)/PI;
	return result;
}


int main(int argc, char **argv)
{

	ros::init(argc, argv, "joint_states_pub");
	ros::NodeHandle n;
	//		ros::Publisher chatter_pub = n.advertise<std_msgs::String>("count", 1000);
	ros::Subscriber sub=n.subscribe("joint_path_command",10,chatterCB);

	int count=0;
	ros::Rate loop_rate(125);
	Robot robot("192.168.2.175:50051");

	//  pos[0]=34.507;
	//  pos[1]=145.062;
	//  pos[2]=-56.326;
	//  pos[3]=164.070;
	//  pos[4]=-137.357;
	//  pos[5]=103.926;

	robot.start();

	// ros::Subscriber sub=n.subscribe("/joint_states", 1000, updateOringinPos);
	int reply=robot.ServoJEnable(true);
	std::cout<<"servoj enable "<<reply<<std::endl;

	// SubscribeAndPublish test("192.168.2.60:50051");  
	// ros::MultiThreadedSpinner s(2);  //多线程
	// ros::spin(s);  
	int j = 0;
	while (ros::ok())
	{
		std_msgs::String msg;
		//print 6 axis point in same time stamp, should change later. should be sent to the sj interface
		if (all_points.size() == 0)
		{
			//			printf("hello\n");
			ros::spinOnce();
			loop_rate.sleep();
		}
		else if (j<all_points[0].size())
		{
			for(int i=0; i<all_points.size(); i++)
			{
				pos[i] = radian_to_angle(all_points[i][j]); //change to angle
				printf("%dpos%d:%f\t", j, i, pos[i]);
			}
			j++;

			//						++count;
			//						std::stringstream ss;
			//						ss << "hello world " << count;
			//						msg.data = ss.str();
			//						chatter_pub.publish(msg);

			robot.servoJMove(pos,1);
			ros::spinOnce();
			loop_rate.sleep();
		}
		else
		{
			all_points.clear();
			j = 0;
			ros::spinOnce();
			loop_rate.sleep();
		}
	}
	printf("sleeping!\n");
	sleep(30);
	printf("enable shut down!\n");

	reply=robot.ServoJEnable(false);
	std::cout<<"servoj enable "<<reply<<std::endl;
	//  robot.stop();
	return 0;
}
