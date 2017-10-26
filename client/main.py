#!/bin/python
import threading

from client import send_ping
import RPi.GPIO as GPIO
import time

led_red = 19
led_green = 6
led_yellow = 17
sensor_pin = 4
status_pin = 22
status = "off"
callback = False

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

def set_status(new_status):
    "standby,triggerd,on,off"
    global status

    print("@@@@@@@@@status" + new_status+ " oud" + status)

    old_status = status
    status = new_status

    if status == "standby":
        GPIO.output(led_green, 1)
        GPIO.output(led_yellow, 0)
        GPIO.output(led_red, 0)
    elif status == "triggerd":
        GPIO.output(led_green, 0)
        GPIO.output(led_yellow, 1)
        GPIO.output(led_red, 0)
    elif status == "on" and old_status != status:
        pass
        # GPIO.output(led_green, 0)
        # GPIO.output(led_yellow, 0)
        # GPIO.output(led_red, 1)
    elif status == "off":
        GPIO.output(led_green, 0)
        GPIO.output(led_yellow, 0)
        GPIO.output(led_red, 0)

set_status("standby")


def sensor_triggerd(self):
    print("triggerd")
    if status != "standby":
        return
    set_status("triggerd")
    time.sleep(5)
    if status == "triggerd":
        set_status("on")


def status_pin_function(self):
    global status
    print("status button pressed")
    set_status("standby")


GPIO.add_event_detect(status_pin, GPIO.RISING, callback=status_pin_function, bouncetime=300)
GPIO.add_event_detect(sensor_pin, GPIO.RISING, callback=sensor_triggerd, bouncetime=300)

def background_ping():
    """thread background_check function"""
    while True:
        try:
            command = send_ping(status)
            if command == "set_status:standby":
                set_status("standby")
            if command == "set_status:on":
                set_status("on")
        except:
            set_status("on")
        continue

background_thread = threading.Thread(target=background_ping)
background_thread.start()

try:
    while True:
        if status == "off":
            GPIO.output(led_green, 0)
            GPIO.output(led_yellow, 0)
            GPIO.output(led_red, 0)
            time.sleep(2)
            continue
        elif status == "standby":
            callback = True
            GPIO.output(led_green, 1)
            GPIO.output(led_yellow, 0)
            GPIO.output(led_red, 0)
            time.sleep(0.2)
        elif status == "triggerd":
            GPIO.output(led_green, 0)
            GPIO.output(led_yellow, 1)
            GPIO.output(led_red, 0)
            time.sleep(0.1)
        elif status == "on":
            GPIO.output(led_green, 0)
            GPIO.output(led_yellow, 0)
            GPIO.output(led_red, 1)
            time.sleep(0.2)
            GPIO.output(led_green, 0)
            GPIO.output(led_yellow, 0)
            GPIO.output(led_red, 0)
            time.sleep(0.2)
except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()



