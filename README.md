# Raspberry Pi E-Mail Notifier

### Requirements

* Raspberry pi 2 or higher
* Adafruit PiTFT 2.2
* Python 3.7
* Luxafor
* IMAP access to an E-Mail box

### Installation

Step 1: Install drivers for the _Adafruit PiTFT2.2_

```sh
cd ~
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/adafruit-pitft.sh
chmod +x adafruit-pitft.sh
sudo ./adafruit-pitft.sh
```

Step 2: Download and install requirements for Python3.7

```sh
cd ~
git clone https://github.com/Vepnar/rpi-email-notifier.git
cd rpi-email-notifier
python3.7 -m pip install -r requirements.txt
```

Step 3: Configure the application

This application won't run out of the box  and you have to edit a configuration file

```sh
nano config.cfg
```

Step 3: Starting the application

```sh
sudo python3.7 main.py
```


#### This project will be based on the following little projects I made before

* [PiTFTGpio.py](https://github.com/Vepnar/Little-projects/blob/master/Python/RaspberryPi/PiTFTgpio.py)
* [PiTFT.py](https://github.com/Vepnar/Little-projects/blob/master/Python/RaspberryPi/PiTFT.py)
* [emailnotifier.py](https://github.com/Vepnar/Little-projects/blob/master/Python/Networking/emailnotifier.py)
