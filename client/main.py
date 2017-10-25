#!/bin/python
import picamera
from picamera import camera

from client import send_ping

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
GPIO.add_event_detect(sensor_pin, GPIO.RISING)
GPIO.add_event_detect(status_pin, GPIO.RISING)

def set_status(new_status):
    "standby,triggerd,on,off"
    global status
    status = new_status

    if status == "standby":
        GPIO.output(led_green, 1)
        GPIO.output(led_yellow, 0)
        GPIO.output(led_red, 0)
    elif status == "triggerd":
        GPIO.output(led_green, 0)
        GPIO.output(led_yellow, 1)
        GPIO.output(led_red, 0)
    elif status == "on":
        GPIO.output(led_green, 0)
        GPIO.output(led_yellow, 0)
        GPIO.output(led_red, 1)
    elif status == "off":
        GPIO.output(led_green, 0)
        GPIO.output(led_yellow, 0)
        GPIO.output(led_red, 0)

set_status("off")


def sensor_triggerd(self):
    # GPIO.remove_event_detect(sensor_pin)
    set_status("triggerd")
    # GPIO.output(led_green, 0)
    # GPIO.output(led_yellow, 1)
    answer = None
    def check():
        time.sleep(5)
        if answer != None:
            return
        print("te laat")
        check_code(answer)
    Thread(target=check).start()
    answer = input("Input something: ")
    check_code(answer)


def status_pin_function(self):
    global status
    if status == "off":
        set_status("standby")
    else:
        set_status("off")

# def sensor_triggerd(self):
#     # GPIO.remove_event_detect(sensor_pin)
#     set_status("triggerd")
#     # GPIO.output(led_green, 0)
#     # GPIO.output(led_yellow, 1)
#     answer = None
#     def check():
#         time.sleep(5)
#         if answer != None:
#             return
#         print("te laat")
#         check_code(answer)
#     Thread(target=check).start()
#     answer = input("Input something: ")
#     check_code(answer)


GPIO.add_event_callback(status_pin, status_pin_function)

def check_code(code):
    print("check_code functie")
    GPIO.output(led_yellow, 0)
    if code == '1234':
        correct_code()
    else:
        alarm()

def correct_code():
    set_status("standby")
    GPIO.output(led_green, 1)
    GPIO.output(led_red, 0)
    GPIO.add_event_detect(sensor_pin, GPIO.RISING)
    print("correct code functie")

def alarm():
    set_status("on")
    # while True:
    #     global status
    #     status = "niet oke"
    #     GPIO.output(led_red, 1)
    #     print("wrong code functie")
    #     time.sleep(0.2)
    #     GPIO.output(led_red, 0)
    #     time.sleep(0.2)
    # pass

def connection_lost():
    pass


try:
    while True:
        print("loop")
        print(callback)
        if status == "off":
            if callback:
                GPIO.remove_event_detect(sensor_pin)
            GPIO.output(led_green, 0)
            GPIO.output(led_yellow, 0)
            GPIO.output(led_red, 0)
            time.sleep(2)
            continue
        elif status == "standby":
            GPIO.add_event_callback(sensor_pin, sensor_triggerd)
            callback = True
            GPIO.output(led_green, 1)
            GPIO.output(led_yellow, 0)
            GPIO.output(led_red, 0)
            time.sleep(2)
        elif status == "triggerd":
            GPIO.output(led_green, 0)
            GPIO.output(led_yellow, 1)
            GPIO.output(led_red, 0)
            time.sleep(2)
        elif status == "on":
            GPIO.output(led_green, 0)
            GPIO.output(led_yellow, 0)
            GPIO.output(led_red, 1)
            time.sleep(0.2)
            GPIO.output(led_green, 0)
            GPIO.output(led_yellow, 0)
            GPIO.output(led_red, 0)
            time.sleep(0.2)

        try:
            command = send_ping(status)
            if command == "set_status:standby":
                set_status("standby")
            print("command: " + command)
        except ConnectionError:
            alarm()
        continue
except KeyboardInterrupt:
    # GPIO netjes afsluiten.
    GPIO.cleanup()



