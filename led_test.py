#!/bin/python
pin = 4
# importeer de GPIO bibliotheek.
import RPi.GPIO as GPIO
# Importeer de time biblotheek voor tijdfuncties.
from time import sleep

# Zet de pinmode op Broadcom SOC.
GPIO.setmode(GPIO.BCM)
# Zet waarschuwingen uit.
GPIO.setwarnings(False)

# Zet de GPIO pin als uitgang.
GPIO.setup(pin, GPIO.OUT)

try:
    while True:
        # Zet de LED aan.
        GPIO.output(pin, 1)
        # Wacht een seconde.
        sleep(0.1)
        # Zet de LED uit.
        GPIO.output(pin, 0)
        # Wacht een seconde.
        sleep(0.1)

        # Zet de LED aan.
        GPIO.output(pin, 1)
        # Wacht een seconde.
        sleep(0.1)
        # Zet de LED uit.
        GPIO.output(pin, 0)
        # Wacht een seconde.
        sleep(0.1)

except KeyboardInterrupt:
    # GPIO netjes afsluiten.
    GPIO.cleanup()