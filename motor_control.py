from flask import Flask
from flask import request
import RPi.GPIO as gpio
import time
import atexit

app = Flask(__name__)

def cleanup():
    pwm.stop()
    GPIO.cleanup()

atexit.register(cleanup)

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
  pwm.ChangeDutyCycle(speed)

  time.sleep(sec)
  pwm.stop()
  gpio.cleanup()


@app.route("/")
def web_interface():
  html = open("web_interface.html")
  response = html.read().replace('\n', '')
  return response

@app.route("/set_speed")
def set_speed():
  speed = int(request.args.get("speed",0))
  forward(speed, 100)

  print "Received " + str(speed)

  return "Received " + str(speed)

def main():
  app.run(host= '0.0.0.0')

main()

