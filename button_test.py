import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


try:
    while True:
        input_state = GPIO.input(17)
        input_state2 = GPIO.input(22)
        print(input_state)
        print(input_state2)
        time.sleep(0.2)
        if input_state == True:
            print('Button Pressed')
            time.sleep(0.2)

except KeyboardInterrupt:
    # GPIO netjes afsluiten.
    GPIO.cleanup()