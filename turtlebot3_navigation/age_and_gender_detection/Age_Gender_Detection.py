import cv2 
import math
import time
import numpy as np
import rospkg

rospack = rospkg.RosPack()
pkg_path =  rospack.get_path('turtlebot3_navigation')

faceProto = pkg_path + "/src/age_and_gender_detection/modelNweight/opencv_face_detector.pbtxt"
faceModel = pkg_path + "/src/age_and_gender_detection/modelNweight/opencv_face_detector_uint8.pb"

# ageProto = "modelNweight/age_deploy.prototxt"
ageProto = pkg_path + "/src/age_and_gender_detection/modelNweight/age_deploy.prototxt"

# ageModel = "modelNweight/age_net.caffemodel"
ageModel = pkg_path + "/src/age_and_gender_detection/modelNweight/age_net.caffemodel"

genderProto = pkg_path + "/src/age_and_gender_detection/modelNweight/gender_deploy.prototxt"
genderModel = pkg_path + "/src/age_and_gender_detection/modelNweight/gender_net.caffemodel"

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']

# Load network
ageNet = cv2.dnn.readNet(ageModel, ageProto)
genderNet = cv2.dnn.readNet(genderModel, genderProto)
faceNet = cv2.dnn.readNet(faceModel, faceProto)


def getFaceBox(frame, net = faceNet, conf_threshold=0.7):
    # frameOpencvDnn = frame.copy()
    # frameOpencvDnn = frame
    # height, width = np.shape(frame)
    bboxes = []
    threshold = 25000
    if frame is None:
        print('frame is None')
        return 0,bboxes
    
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            box_x = x2 - x1
            box_y = y2 - y1
            box_area = box_x * box_y
            
            if box_area > threshold:
                bboxes.append([x1, y1, x2, y2])
            # print(x1, y1, x2, y2)
            # print(box_area)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight/150)), 8)
    return frame, bboxes



padding = 20

def get_numb_of_faces(frame):
    frame,bboxes = getFaceBox(frame)
    num_of_faces = len(bboxes)
    return num_of_faces
    
def age_gender_detector(frame):
    male , female = 0,0
    # Read frame
    t = time.time()
    frameFace, bboxes = getFaceBox(frame)
    for bbox in bboxes:
        # print(bbox)
        face = frame[max(0,bbox[1]-padding):min(bbox[3]+padding,frame.shape[0]-1),max(0,bbox[0]-padding):min(bbox[2]+padding, frame.shape[1]-1)]

        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)
        genderPreds = genderNet.forward()
        gender = genderList[genderPreds[0].argmax()]
        if gender == genderList[0]:
            male = male + 1
        else :
            female = female + 1
        ageNet.setInput(blob)
        agePreds = ageNet.forward()
        age = ageList[agePreds[0].argmax()]

        label = "{},{}".format(gender, age)
        cv2.putText(frameFace, label, (bbox[0], bbox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
    return frameFace, len(bboxes), male , female

def main():
    cap = cv2.VideoCapture(0)
    while True:
        ret, input = cap.read()
        # input = cv2.imread("image3.jpg")
        frame, num_of_faces, num_of_male, num_of_female = age_gender_detector(input)
        print("num_of_faces:", num_of_faces )
        print("male: %d , female: %d"  %(num_of_male , num_of_female) )
        print("------------" )
        
        cv2.imshow("frame", frame)
        if cv2.waitKey(30) & 0xff == ord('q'):
            break
        
if __name__ == '__main__':
    main()
    