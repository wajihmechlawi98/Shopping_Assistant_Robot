import cv2
from Voice_Assistant.text_to_speech import play_sound
from age_and_gender_detection.Age_Gender_Detection import get_numb_of_faces
from robotControlNode import checkEntrancePose, time_goal_reached, Goal_Reached
# import rospy

cap = cv2.VideoCapture('/dev/video4')
def greet():
    prev_face_num = 0
    face_counter = 0
    face_detected = False
    
    # if checkEntrancePose:
    while True:
        _, frame = cap.read()
        
        print("checkEntrancePose", checkEntrancePose)
        #1- get the number of faces detected in the frame
        num_of_faces = get_numb_of_faces(frame)
        print("num_of_faces", num_of_faces)
        if checkEntrancePose:
            #2- greet in case of face detected
            if num_of_faces != 0:
                if num_of_faces == prev_face_num and face_counter < 50:
                    face_counter += 1

                if face_counter == 50:
                    face_counter += 1
                    face_detected = True
                    play_sound("welcome")
                    play_sound("scan")

            if num_of_faces != prev_face_num:
                face_counter = 0
                face_detected = False
                
            prev_face_num = num_of_faces
            
            # ask the user for his product
            # if face_detected:
            #     print("test")
            # if Goal_Reached:
                # if (rospy.get_rostime()- time_goal_reached) > 15:
                #     print ("return back")
            
        
        cv2.imshow("frame", frame)
        if cv2.waitKey(30) & 0xff == ord('q'):
            break


greet()
