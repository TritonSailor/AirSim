#!/usr/bin/env python
# Software License Agreement (BSD License)

## Simple talker demo that published std_msgs/Strings messages
## to the 'chatter' topic

import rospy
import tf
import ros_numpy
from std_msgs.msg import String
#from geometry_msgs.msg import PoseStamped

# ROS Image message
from sensor_msgs.msg import Image

# AirSim Python API
from AirSimClient import *
import time
import ast

def talker():
    pub = rospy.Publisher("airsimImage", Image, queue_size=1)
    rospy.init_node('image_raw', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    # connect to the AirSim simulator 
    client = CarClient()
    client.confirmConnection()

    start = time.time()
    number = 1

    while not rospy.is_shutdown():
         # get camera images from the car
        responses = client.simGetImages([
        #    ImageRequest(0, AirSimImageType.DepthVis),  #depth visualiztion image
        #    ImageRequest(1, AirSimImageType.DepthPerspective, True), #depth in perspective projection
        #    ImageRequest(1, AirSimImageType.Scene), #scene vision image in png format
            ImageRequest(1, AirSimImageType.Scene, False, False)])  #scene vision image in uncompressed RGBA array
        print('Retrieved images: %d', len(responses))

        for response in responses:
            filename = './' + str(0)

            if response.pixels_as_float:
                print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
                AirSimClientBase.write_pfm(os.path.normpath(filename + '.pfm'), AirSimClientBase.getPfmArray(response))
            elif response.compress: #png format
                print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
                AirSimClientBase.write_file(os.path.normpath(filename + '.png'), response.image_data_uint8)
            else: #uncompressed array
                print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
                img_rgba_string = response.image_data_uint8
                img_rgb_string = ''.join("" if i % 4 == 0 else char for i, char in enumerate(img_rgba_string, 1))
                #img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) #.tolist() #get numpy array
#                img_rgba = img1d.reshape(response.height, response.width, 4) #reshape array to 4 channel image array H X W X 4
#                img_rgba = (np.flipud(img_rgba)) #original image is fliped vertically
#                img_rgb = img_rgba[:,:,:3] 
#                img_rgb_list = img_rgb.tolist()
                #img_rgba[:,:,1:2] = 100 #just for fun add little bit of green in all pixels
#                AirSimClientBase.write_png(os.path.normpath(filename + '.png'), img_rgba) #write to png
                #AirSimClientBase.write_file(os.path.normpath(filename), img_rgba) #write to file  

        # get state of the car
#        car_state = client.getCarState()
#        pos = car_state.kinematics_true.position
#        orientation = car_state.kinematics_true.orientation
#        milliseconds = (time.time() - start) * 1000
       # print("%s,%d,%d,%f,%f,%f,%f,%f,%f,%f" % \
       #   (milliseconds, car_state.speed, car_state.gear, pos.x_val, pos.y_val, pos.z_val, 
       #    orientation.w_val, orientation.x_val, orientation.y_val, orientation.z_val))
#        simPose = PoseStamped()
#        simPose.pose.position.x = pos.x_val
#        simPose.pose.position.y = pos.y_val
#        simPose.pose.position.z = pos.z_val
#        simPose.pose.orientation.w = orientation.w_val
#        simPose.pose.orientation.x = orientation.x_val
#        simPose.pose.orientation.y = orientation.y_val
#        simPose.pose.orientation.z = orientation.z_val
#        simPose.header.stamp = rospy.Time.now()
#        simPose.header.seq = 0
#        simPose.header.frame_id = "simFrame"
# pos.y_val, pos.z_val, orientation.w_val, orientation.x_val, orientation.y_val, orientation.z_val)
#        print("%f" % (simPose.pose.position.x))
#        print("%f" % (simPose.pose.position.y))
#        print("%f" % (simPose.pose.position.z))

        msg=Image() 
        msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = "frameId"
        msg.encoding = "rgb8"
        msg.height = 360
        msg.width = 640
        msg.data = img_rgb_string
        msg.is_bigendian = 0
        msg.step = msg.width * 3
       # amsg = ros_numpy.msgify(Image, img_rgba)
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
