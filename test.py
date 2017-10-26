#!/bin/python
import picamera
from picamera import camera


led_red = 19
led_green = 6
led_yellow = 17
sensor_pin = 4
status_pin = 22
status = "off"
callback = False
import socket
import RPi.GPIO as GPIO
import time
from threading import Thread

# Zet de pinmode op Broadcom SOC.
GPIO.setmode(GPIO.BCM)
# Zet waarschuwingen uit.

GPIO.setwarnings(False)

# Zet de GPIO pin als uitgang.
GPIO.setup(led_green, GPIO.OUT)
GPIO.setup(led_red, GPIO.OUT)
GPIO.setup(led_yellow, GPIO.OUT)

GPIO.output(led_green, 0)
GPIO.output(led_red, 0)
GPIO.output(led_yellow, 0)

GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(status_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def status_pin_function(self):
    global status
    if status == "off":
        status = "on"
        print("asdf")
    else:
        status = "off"
        print("asdf22")
        GPIO.remove_event_detect(status_pin)
        time.sleep(2)
        GPIO.add_event_detect(status_pin, GPIO.RISING, callback=status_pin_function, bouncetime=300)

GPIO.add_event_detect(status_pin, GPIO.RISING, callback=status_pin_function, bouncetime=300)


while True:
    pass