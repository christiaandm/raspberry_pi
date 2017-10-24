#!/bin/python
led_pin = 19
button_pin = 4
# importeer de GPIO bibliotheek.

import RPi.GPIO as GPIO

# Importeer de time biblotheek voor tijdfuncties.
from time import sleep

# Zet de pinmode op Broadcom SOC.
GPIO.setmode(GPIO.BCM)
# Zet waarschuwingen uit.

GPIO.setwarnings(False)

# Zet de GPIO pin als uitgang.
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    while True:
        input_state = GPIO.input(button_pin)
        print(input_state)
        if input_state == True:
            print('Button Pressed')
            # time.sleep(0.2)
            # Zet de LED aan.
            GPIO.output(led_pin, 1)
            # Wacht een seconde.
            sleep(0.1)
            # Zet de LED uit.
            GPIO.output(led_pin, 0)
            # Wacht een seconde.
            sleep(0.1)

            # Zet de LED aan.
            GPIO.output(led_pin, 1)
            # Wacht een seconde.
            sleep(0.1)
            # Zet de LED uit.
            GPIO.output(led_pin, 0)
            # Wacht een seconde.
            sleep(0.1)

except KeyboardInterrupt:
    # GPIO netjes afsluiten.
    GPIO.cleanup()
