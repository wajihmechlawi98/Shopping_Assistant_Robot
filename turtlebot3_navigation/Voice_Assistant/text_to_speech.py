
import gtts
from playsound import playsound
import rospkg

rospack = rospkg.RosPack()
pkg_path =  rospack.get_path('turtlebot3_navigation')

# make request to google to get synthesis
# tts = gtts.gTTS("i'm going back to the entrance", lang="en", slow=False)

# save the audio file
# file_name = "entrance.mp3"
# tts.save(file_name)

# play the audio file
# playsound(file_name)


def play_sound(file_name):

    playsound(pkg_path + "/src/Voice_Assistant/" +file_name + ".mp3")

# play_sound("lets_go")
# play_sound("hello")
prev_face_num = 0
def greet_face(faces_number):
    
    if faces_number != 0 and faces_number!=prev_face_num:
        play_sound("hello")
        
        
    prev_face_num = faces_number