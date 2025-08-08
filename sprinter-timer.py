import RPi.GPIO as GPIO
import time
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import ImageDraw, ImageFont, Image
import os

# === CZASY STARTU ===
PREPARE_TIME_1 = 10
PREPARE_TIME_2 = 5

# === GPIO SETUP ===
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

# === OLED SETUP ===
serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

def display_text(text, second_line=None):
    image = Image.new("1", device.size)
    draw = ImageDraw.Draw(image)
    draw.text((5, 10), text, fill=255)
    if second_line:
        draw.text((5, 30), second_line, fill=255)
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

def countdown_display(main_text, seconds):
    for i in range(seconds, 0, -1):
        image = Image.new("1", device.size)
        draw = ImageDraw.Draw(image)
        draw.text((5, 5), main_text, fill=255)
        draw.text((5, 30), f"Time: {i}s", fill=255)
        device.display(image)
        time.sleep(1)

def save_result(time_val):
    with open("results.txt", "a") as f:
        f.write(f"{time_val}\n")

def get_best_result():
    if not os.path.exists("results.txt"):
        return None
    with open("results.txt") as f:
        try:
            times = [float(line.strip()) for line in f if line.strip()]
            return min(times) if times else None
        except ValueError:
            return None

try:
    while True:
        display_text("Press the button")
        print("Waiting for button press...")
        while GPIO.input(BUTTON_PIN) == GPIO.HIGH:
            time.sleep(0.1)
        beep(0.3)

        countdown_display("Go to start line", PREPARE_TIME_1)
        beep(0.3)

        countdown_display("Prepare...", PREPARE_TIME_2)
        beep(0.5)

        display_text("GO!")
        start_time = time.time()

        while True:
            elapsed = round(time.time() - start_time, 2)
            display_text(f"Time:", f"{elapsed} s")
            distance = measure_distance()
            if distance is not None and distance < 100:
                break
            time.sleep(0.1)

        final_time = round(time.time() - start_time, 2)
        beep(0.5)

        save_result(final_time)
        best_time = get_best_result()

        display_text(f"Result: {final_time}s",
                     f"Best: {best_time}s" if best_time else "No record yet")
        print(f"Object detected after {final_time} seconds")
        time.sleep(5)

except KeyboardInterrupt:
    print("Bye Bye")

finally:
    GPIO.output(BUZZER, GPIO.HIGH)
    GPIO.cleanup()

