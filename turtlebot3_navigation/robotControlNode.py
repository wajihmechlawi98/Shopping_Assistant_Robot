#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from moveBaseSendGoal import sendPose
from pos_goals import *
from move_base_msgs.msg import MoveBaseActionResult
from turtlebot3_msgs.msg import Sound
import time
from Voice_Assistant.text_to_speech import play_sound
from face_detection_v2 import greet
Goal_Reached = True
checkEntrancePose = True
soundPublisher = rospy.Publisher('/sound', Sound, queue_size=1)
tone = Sound()
desiredPose = "entrance"
time_goal_reached = 0


def poseCallBack(pose_msg):
    rospy.loginfo("Desired Pos: %s", pose_msg.data)
    global desiredPose
    desiredPose = pose_msg.data

    global Goal_Reached
    if Goal_Reached:
        Goal_Reached = False
        play_sound("lets_go")
        tone.value = tone.ON
        soundPublisher.publish(tone)
        
        if desiredPose == "position1":
            sendPose(pos1)
        elif desiredPose == "position2":
            sendPose(pos2)
        elif desiredPose == "position3":
            sendPose(pos3)


def navResultCB(statusMsg=MoveBaseActionResult):
    text_data = statusMsg.status.text
    print(text_data)
    if desiredPose!="entrance":
        play_sound("arrived")
    
    global time_goal_reached
    time_goal_reached = time.time()
    print("time_goal_reached: ", time_goal_reached)
    global Goal_Reached
    Goal_Reached = True
    
    tone.value = tone.OFF
    soundPublisher.publish(tone)
    # print(statusMsg)
    # text = statusMsg.


def listener():

    rospy.init_node('pose_Node')
    rospy.Subscriber("desired_Pose", String, poseCallBack)
    rospy.Subscriber("/move_base/result", MoveBaseActionResult, navResultCB)
    tone.value = tone.ON
    soundPublisher.publish(tone)
    global desiredPose
    global Goal_Reached
    
    while not rospy.is_shutdown():
        
        # print(time.time() - time_goal_reached)
        if desiredPose!="entrance" and Goal_Reached == True:
            print(time.time() - time_goal_reached)

            if((time.time() - time_goal_reached) > 15):
                play_sound("entrance")
                desiredPose = "entrance"
                Goal_Reached = False
                sendPose(entrance)
                print("back home")
                
        # elif desiredPose=="entrance" and Goal_Reached == True:
        greet(desiredPose)
    # rospy.spin()


if __name__ == '__main__':
    listener()
