from flask import Flask, request
import RPi.GPIO as GPIO
import atexit

# Initialize Flask app
app = Flask(__name__)

# GPIO setup for one side of the H-bridge
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

@app.route("/")
def web_interface():
    with open("web_interface.html") as html_file:
        response = html_file.read().replace('\n', '')
    return response

@app.route("/set_speed")
def set_speed():
    speed = int(request.args.get("speed", 0))
    direction = GPIO.HIGH if speed > 0 else GPIO.LOW
    abs_speed = abs(speed) if abs(speed) <= 100 else 100  # Ensure speed is between 0 and 100

    GPIO.output(motorInput2, GPIO.LOW)  # Ensure one input is always low
    pwm.ChangeDutyCycle(abs_speed)  # Adjust speed

    return "Speed set to {speed}"

def main():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()

