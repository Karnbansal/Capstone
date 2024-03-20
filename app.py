import RPi.GPIO as gpio
import time

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_speed', methods=['GET'])
def set_speed():
    speed = int(request.args.get('speed'))
    print('Received speed:', speed)
    forward(4, speed)
    # Here you can perform any action with the received speed value
    return " speeddddddddddd"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)  # Set debug to False

def init():
 gpio.setmode(gpio.BCM)
 gpio.setup(17, gpio.OUT)
 gpio.setup(22, gpio.OUT)
 pwm = gpio.PWM(17, 100)
 pwm.start(0)
 return pwm

def forward(sec, speed):
 pwm=init()
 gpio.output(17, False)
 gpio.output(22, True)
 pwm.changeDutyCycle(speed)
 time.sleep(sec)
 pwm.stop()
 gpio.cleanup()
