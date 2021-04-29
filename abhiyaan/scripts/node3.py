#!/usr/bin/env python

import rospy
import message_filters
from std_msgs.msg import String



def callback(data):
	rospy.loginfo("%s", data.data)
	
def callback1(data):
	rospy.loginfo("%s", data.data)

def node3():
	rospy.init_node('node3', anonymous=True)
	rospy.Subscriber("team_abhiyaan", String, callback) 
	rospy.Subscriber("autonomy", String, callback1)
	
	
	rospy.spin()
	
if __name__ == '__main__':
	node3()
