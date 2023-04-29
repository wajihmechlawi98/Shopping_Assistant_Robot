#!/usr/bin/env python3

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

client = actionlib.SimpleActionClient('move_base', MoveBaseAction)

def sendPose(pose = MoveBaseGoal()) :
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = pose.target_pose.pose.position.x
    goal.target_pose.pose.position.y = pose.target_pose.pose.position.y
    goal.target_pose.pose.orientation.z = pose.target_pose.pose.orientation.z
    goal.target_pose.pose.orientation.w = pose.target_pose.pose.orientation.w 
    client.send_goal(goal)

def movebase_client():
    
    client.wait_for_server()

    rospy.loginfo("Goal sent!")
    wait = client.wait_for_result()

    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()


if __name__ == '__main__':
    try:
        rospy.init_node('movebase_client_py')
        result = movebase_client()
        if result:
            rospy.loginfo("Goal execution done!")
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")

