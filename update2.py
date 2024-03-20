import RPi.GPIO as gpio
import time

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



print "forward"
forward(4,25)

