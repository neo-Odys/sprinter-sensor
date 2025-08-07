# sprinter-sensor 
Sprinter timing detection system using ultrasonic sensor and OLED display

### Installtion
```
sudo apt update
sudo apt install libjpeg-dev libfreetype6-dev python3-pil python3-smbus i2c-tools -y


python3 -m venv venv
source venv/bin/activate
pip install RPi.GPIO luma.oled


sudo raspi-config
i2cdetect -y 1


source venv/bin/activate
python main.py  # zakładając, że to Twój plik
```


### Autostart
```
sudo nano /etc/systemd/system/sprinttimer.service

[Unit]
Description=Sprint Timer Service
After=network.target

[Service]
ExecStart=/home/brotus/workspace/sprinter-sensor/venv/bin/python /home/brotus/workspace/sprinter-sensor/sprinttimer.py
WorkingDirectory=/home/brotus/workspace/sprinter-sensor
StandardOutput=inherit
StandardError=inherit
Restart=always
User=brotus

[Install]
WantedBy=multi-user.target

sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable sprinttimer.service
sudo systemctl start sprinttimer.service

sudo systemctl status sprinttimer.service
```
