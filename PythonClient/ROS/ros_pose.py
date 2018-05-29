#!/usr/bin/env python
# Software License Agreement (BSD License)

## Simple talker demo that published std_msgs/Strings messages
## to the 'chatter' topic

import rospy
import tf
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from AirSimClient import *
import time


def talker():
    pub = rospy.Publisher("airsimPose", PoseStamped, queue_size=1)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    # connect to the AirSim simulator 
    client = CarClient()
    client.confirmConnection()

    start = time.time()


    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        #rospy.loginfo(hello_str)
        #pub.publish(hello_str)

        # get state of the car
        car_state = client.getCarState()
        pos = car_state.kinematics_true.position
        orientation = car_state.kinematics_true.orientation
        milliseconds = (time.time() - start) * 1000
       # print("%s,%d,%d,%f,%f,%f,%f,%f,%f,%f" % \
       #   (milliseconds, car_state.speed, car_state.gear, pos.x_val, pos.y_val, pos.z_val, 
       #    orientation.w_val, orientation.x_val, orientation.y_val, orientation.z_val))
        simPose = PoseStamped()
        simPose.pose.position.x = pos.x_val
        simPose.pose.position.y = pos.y_val
        simPose.pose.position.z = pos.z_val
        simPose.pose.orientation.w = orientation.w_val
        simPose.pose.orientation.x = orientation.x_val
        simPose.pose.orientation.y = orientation.y_val
        simPose.pose.orientation.z = orientation.z_val
        simPose.header.stamp = rospy.Time.now()
        simPose.header.seq = 1
        simPose.header.frame_id = "simFrame"
# pos.y_val, pos.z_val, orientation.w_val, orientation.x_val, orientation.y_val, orientation.z_val)
#        print("%f" % (simPose.pose.position.x))
#        print("%f" % (simPose.pose.position.y))
#        print("%f" % (simPose.pose.position.z))
        
        rospy.loginfo(simPose)
        pub.publish(simPose)
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
