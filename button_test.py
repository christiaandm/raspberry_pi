import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


try:
    while True:
        input_state = GPIO.input(4)
        print(input_state)
        if input_state == True:
            print('Button Pressed')
            # time.sleep(0.2)

except KeyboardInterrupt:
    # GPIO netjes afsluiten.
    GPIO.cleanup()