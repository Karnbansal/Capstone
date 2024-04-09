import threading
from subprocess import call
import speech_recognition as sr
import serial
import RPi.GPIO as GPIO      
import os
import time

# Global variables
r = sr.Recognizer()
led = 27
text = {}
text1 = {}



def listen1():
    with sr.Microphone(device_index=2) as source:
        r.adjust_for_ambient_noise(source)
        print("Say Something")
        audio = r.listen(source)
        print("Got it")
    return audio

def voice(audio1):
    try: 
        text1 = r.recognize_google(audio1) 
        print ("You said: " + text1)
        return text1
    except sr.UnknownValueError: 
        print("Google Speech Recognition could not understand") 
        return "NONE"
    except sr.RequestError as e: 
        print("Could not request results from Google")
        return 0

def process_audio():
    while True:
        audio1 = listen1() 
        text = voice(audio1)
        if 'motor on' in text: 
            print("Light on")
        elif 'motor off' in text:
            print("Light off")
        else:
            print("Repeat")

if __name__ == '__main__':
    audio_thread = threading.Thread(target=process_audio)
    audio_thread.daemon = True  # Daemonize the thread so it will be terminated when the main program exits
    audio_thread.start()
    
    # Main program logic
    running = True
    while running:
        # Add your main program logic here
        user_input = input("Enter 'quit' to exit: ")
        if user_input.lower() == 'quit':
            running = False  # Set the flag to False to exit the loop
            # You can add additional cleanup or exit logic here if needed
            print("Exiting program...")
