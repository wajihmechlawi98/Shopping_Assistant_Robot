# import speech_recognition as sr
# import pyaudio
# # import sounddevice as sd

# # sr.Microphone.list_microphone_names()
# # print(sr.Microphone.list_microphone_names())
# def get_audio():
#     recorder = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Say Something....")
#         recorder.adjust_for_ambient_noise(source, duration=0.2)

#         audio = recorder.listen(source)

#         text = recorder.recognize_google(audio)
#         text = text.lower()
#         print("hi")
#         print(" You said:", text)
#     return text


# get_audio()


# import gtts
from playsound import playsound

# make request to google to get synthesis
# tts = gtts.gTTS("Lets go", lang="en", slow=False)

# save the audio file
# file_name = "lets_go.mp3"
# tts.save(file_name)

# play the audio file
# playsound(file_name)


def play_sound(file_name):

    playsound("robot_control/src/Voice_Assistant/" +file_name + ".mp3")

play_sound("lets_go")
play_sound("hello")
prev_face_num = 0
def greet_face(faces_number):
    
    if faces_number != 0 and faces_number!=prev_face_num:
        play_sound("hello")
        
        
    prev_face_num = faces_number