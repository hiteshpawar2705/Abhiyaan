#!/usr/bin/env python
#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt


class TurtleBot:

    def __init__(self):
        # Creates a node with name 'turtlebot_controller' and make sure it is a
        # unique node (using anonymous=True).
        rospy.init_node('turtlebot_controller', anonymous=True)

        # Publisher which will publish to the topic '/turtle2/cmd_vel'.
        self.velocity_publisher = rospy.Publisher('/turtle2/cmd_vel',
                                                  Twist, queue_size=10)

        # A subscriber to the topic '/turtle2/pose'. self.update_pose is called
        # when a message of type Pose is received.
        self.pose_subscriber = rospy.Subscriber('/turtle2/pose',
                                                Pose, self.update_pose)

        self.pose = Pose()
        self.rate = rospy.Rate(10)

        # A subscriber to the topic '/turtle1/pose'. self.update_pose is called
        # when a message of type Pose is received.
        self.turtle1_pose_subscriber = rospy.Subscriber('/turtle1/pose',
                                                Pose, self.turtle1_pose)

        self.pose_turtle1 = Pose()
        self.rate = rospy.Rate(10)

        


    def update_pose(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

    def turtle1_pose(self, data):
        self.pose_turtle1 = data
        self.pose_turtle1.x = round(self.pose_turtle1.x, 4)
        self.pose_turtle1.y = round(self.pose_turtle1.y, 4)
    

    def euclidean_distance(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        return sqrt(pow((goal_pose.x - self.pose.x), 2) +
                    pow((goal_pose.y - self.pose.y), 2))

    def linear_vel(self, goal_pose, constant=1.5):
        return constant * self.euclidean_distance(goal_pose)

    def steering_angle(self, goal_pose):
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

    def angular_vel(self, goal_pose, constant=6):
        return constant * (self.steering_angle(goal_pose) - self.pose.theta)

    def move2goal(self):
        """Moves the turtle to the goal."""

        goal_pose = Pose()
        goal_pose.x =  self.pose_turtle1.x + float(5) 
        goal_pose.y = self.pose_turtle1.y #+ 5.54 
        

        # Please, insert a number slightly greater than 0 (e.g. 0.01).
        distance_tolerance = float(0.01)  

        vel_msg = Twist()

        while self.euclidean_distance(goal_pose) >= distance_tolerance:
            a = float(self.pose_turtle1.x - self.pose.x)
            if  0.7< a<=2:
                goal_pose = Pose()
                goal_pose.x = float(self.pose_turtle1.x) #+5.54
                goal_pose.y = float(self.pose_turtle1.y) + float(2) #+5.54)
            elif -1.6<a<0.7:
                goal_pose = Pose()
                goal_pose.x = float(self.pose_turtle1.x) + float(2) #+5.54)
                goal_pose.y = float(self.pose_turtle1.y)#+5.54)
            elif a == -1.6:
                goal_pose.x =  self.pose_turtle1.x + float(5) 
                goal_pose.y = self.pose_turtle1.y
            else:
                goal_pose.x =  self.pose_turtle1.x + float(5) 
                goal_pose.y = self.pose_turtle1.y #+ 5.54 
            # Porportional controller

            # Linear velocity in the x-axis.
            vel_msg.linear.x = self.linear_vel(goal_pose)
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0

            # Angular velocity in the z-axis.
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = self.angular_vel(goal_pose)

            # Publishing our vel_msg
            self.velocity_publisher.publish(vel_msg)
            #print(self.pose.x)
            print(self.pose_turtle1.x)

            # Publish at the desired rate.
            self.rate.sleep()

        # Stopping our robot after the movement is over.
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        print("Done!")
        self.velocity_publisher.publish(vel_msg)

        # If we press control + C, the node will stop.
        rospy.spin()

if __name__ == '__main__':
    try:
        x = TurtleBot()
        x.move2goal()
    except rospy.ROSInterruptException:
        pass
