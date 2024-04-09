from flask import Flask, request
import RPi.GPIO as GPIO
import atexit
import threading
import speech_recognition as sr


r = sr.Recognizer()


# Initialize Flask app
app = Flask(__name__)

# GPIO setup for the motor
motorInput1 = 17  # Motor input 1
motorInput2 = 22  # Motor input 2

GPIO.setmode(GPIO.BCM)
GPIO.setup(motorInput1, GPIO.OUT)
GPIO.setup(motorInput2, GPIO.OUT)

# Initialize PWM on one of the motor inputs for speed control
pwm = GPIO.PWM(motorInput1, 100)  # 100 Hz frequency
pwm.start(0)  # Start with 0% duty cycle

def cleanup():
    pwm.stop()
    GPIO.cleanup()

atexit.register(cleanup)

def listen1():
    r = sr.Recognizer()
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
            print("Motor on")
            # Add GPIO logic to turn on the motor
            GPIO.output(motorInput2, GPIO.LOW)  # Ensure one input is always low
            pwm.ChangeDutyCycle(50)  # Set motor speed to 50%
        elif 'motor off' in text:
            print("Motor off")
            # Add GPIO logic to turn off the motor
            GPIO.output(motorInput2, GPIO.LOW)  # Ensure one input is always low
            pwm.ChangeDutyCycle(0)  # Set motor speed to 0%
        else:
            print("Repeat")

@app.route("/")
def web_interface():
    with open("web_interface.html") as html_file:
        response = html_file.read().replace('\n', '')
    return response

@app.route("/set_speed")
def set_speed():
    speed = int(request.args.get("speed", 0))
    abs_speed = abs(speed) if abs(speed) <= 100 else 100  # Ensure speed is between 0 and 100

    GPIO.output(motorInput2, GPIO.LOW)  # Ensure one input is always low
    pwm.ChangeDutyCycle(abs_speed)  # Adjust speed

    return f"Speed set to {abs_speed}"

def run_flask():
    app.run(host='0.0.0.0', port=5005)

def main():
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    audio_thread = threading.Thread(target=process_audio)
    audio_thread.daemon = True  # Daemonize the thread so it will be terminated when the main program exits
    audio_thread.start()

if __name__ == "__main__":
    main()

