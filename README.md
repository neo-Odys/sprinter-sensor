# sprinter-sensor 
Sprinter timing detection system using ultrasonic sensor and OLED display

sudo apt update
sudo apt install libjpeg-dev libfreetype6-dev python3-pil python3-smbus i2c-tools -y


python3 -m venv venv
source venv/bin/activate
pip install RPi.GPIO luma.oled




sudo raspi-config
i2cdetect -y 1


source venv/bin/activate
python main.py  # zakładając, że to Twój plik

