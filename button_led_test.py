#!/bin/python
import picamera
from picamera import camera

led_red = 19
led_green = 6
led_yellow = 17
button_pin = 4

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

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(button_pin, GPIO.RISING)

def sensor_triggerd(self):
    GPIO.remove_event_detect(button_pin)
    print("sensor triggerd")
    GPIO.output(led_green, 0)
    GPIO.output(led_yellow, 1)
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


GPIO.add_event_callback(button_pin, sensor_triggerd)

def check_code(code):
    print("check_code functie")
    GPIO.output(led_yellow, 0)
    if code == '1234':
        correct_code()
    else:
        wrong_code()

def correct_code():
    GPIO.output(led_green, 1)
    GPIO.output(led_red, 0)
    GPIO.add_event_detect(button_pin, GPIO.RISING)
    print("correct code functie")

def wrong_code():
    while True:
        GPIO.output(led_red, 1)
        print("wrong code functie")
        time.sleep(0.2)
        GPIO.output(led_red, 0)
        time.sleep(0.2)
    pass

def connection_lost():
    pass


def send_ping():
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005
    MESSAGE = "Hello, World!testset"
    print("UDP target IP:", str(UDP_IP))
    print("UDP target port:" + str(UDP_PORT))
    print("message:", MESSAGE)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))


try:
    while True:
        # camera = picamera.PiCamera()
        # camera.start_preview()
        # time.sleep(5)
        # camera.capture('/home/pi/Pictures/image.jpg')
        # camera.stop_preview()
        # print("oke")
        # print(GPIO.input(button_pin))
        # time.sleep(2)
        # send_ping()
        continue
except KeyboardInterrupt:
    # GPIO netjes afsluiten.
    GPIO.cleanup()