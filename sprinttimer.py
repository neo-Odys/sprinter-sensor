import RPi.GPIO as GPIO
import time
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import ImageDraw, ImageFont, Image

# GPIO setup
BUZZER = 10
BUTTON_PIN = 20
TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.output(BUZZER, GPIO.HIGH)  # Buzzer off by default (active LOW)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# OLED setup
serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

def display_text(text):
    image = Image.new("1", device.size)
    draw = ImageDraw.Draw(image)
    draw.text((10, 20), text, fill=255)
    device.display(image)

def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start_time = time.time()
    while GPIO.input(ECHO) == 0:
        start = time.time()
        if start - start_time > 0.01:
            return None

    stop_time = time.time()
    while GPIO.input(ECHO) == 1:
        stop = time.time()
        if stop - stop_time > 0.01:
            return None

    duration = stop - start
    distance = (duration * 34300) / 2
    return round(distance, 2)

def beep(duration=0.5):
    GPIO.output(BUZZER, GPIO.LOW)
    time.sleep(duration)
    GPIO.output(BUZZER, GPIO.HIGH)

try:
    while True:
        display_text("Press the button")
        print("Waiting for button press...")
        while GPIO.input(BUTTON_PIN) == GPIO.HIGH:
            time.sleep(0.1)

        # Countdown
        for i in range(5, 0, -1):
            display_text(f"Starting in:\n{i} s")
            time.sleep(1)

        # Start timer
        beep(0.5)
        start_time = time.time()

        while True:
            elapsed = round(time.time() - start_time, 2)
            display_text(f"Time:\n{elapsed} s")
            distance = measure_distance()
            if distance is not None and distance < 100:  # detected object under 1 meter
                break
            time.sleep(0.1)

        final_time = round(time.time() - start_time, 2)
        beep(0.5)
        display_text(f"Result:\n{final_time} s")
        print(f"Object detected after {final_time} seconds")
        time.sleep(5)

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    GPIO.output(BUZZER, GPIO.HIGH)
    GPIO.cleanup()

