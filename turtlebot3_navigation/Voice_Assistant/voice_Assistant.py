# import speech_recognition as sr
# import pyttsx3
# import wikipedia
# import datetime

# # Initialize the text-to-speech engine
# engine = pyttsx3.init()

# # Define a function to speak
# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# # Initialize the speech recognition engine
# r = sr.Recognizer()

# # # Define a function to recognize speech
# def recognize_speech():
#     with sr.Microphone() as source:
#         r.adjust_for_ambient_noise(source)
#         audio = r.listen(source)
#         try:
#             query = r.recognize_google(audio)
#             print("You said: " + query)
#             return query
#         except sr.UnknownValueError:
#             print("Sorry, I didn't catch that.")
#             return ""
#         except sr.RequestError as e:
#             print("Could not request results from Google Speech Recognition service; {0}".format(e))
#             return ""

# # Define the main function
# def main():
#     # Greet the user
#     speak("Hello! How can I help you today?")
#     # Listen for the user's query
#     query = recognize_speech()
#     # If the user said something, process the query
#     if query:
#         # Fetch information from Wikipedia
#         if "wikipedia" in query.lower():
#             speak("Searching Wikipedia...")
#             query = query.replace("wikipedia", "")
#             results = wikipedia.summary(query, sentences=2)
#             speak("According to Wikipedia, " + results)
#         # Get the current date and time
#         elif "what time is it" in query.lower():
#             now = datetime.datetime.now()
#             speak("The time is " + now.strftime("%I:%M %p"))
#         elif "what is today's date" in query.lower():
#             now = datetime.datetime.now()
#             speak("Today's date is " + now.strftime("%B %d, %Y"))
#         # If the query is not recognized, apologize and ask the user to try again
#         else:
#             speak("Sorry, I didn't understand what you said. Please try again.")
#     # Say goodbye to the user
#     speak("Goodbye!")

# if __name__ == "__main__":
#     main()
