#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class Obstacle():
    def __init__(self):
        self.LIDAR_ERR = 0.015
        self._cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        rospy.Subscriber("/scan", LaserScan, self.get_scan)
        self._scan = LaserScan()
        
    
    def get_scan(self, data):
        self._scan = data

    def obstacle(self):
        self.twist = Twist()
        while not rospy.is_shutdown():
            self.scan_filter = [1.5]
            for i in range(720): 
                if i<=170 or i >=550:
                    if self._scan.ranges[i] >= self.LIDAR_ERR:
                        self.scan_filter.append(self._scan.ranges[i])

            if min(self.scan_filter) < 0.25:
                self.twist.linear.x = 0.0
                self.twist.angular.z = 0.0
            else:
                self.twist.linear.x = 0.2
                self.twist.angular.z = 0.0

            self._cmd_pub.publish(self.twist)


def main():
    rospy.init_node('aunchan_obstacle')
    try:
        obstacle = Obstacle()
        obstacle.obstacle()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()