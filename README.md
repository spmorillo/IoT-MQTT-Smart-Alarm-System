# IoT-MQTT-Smart-Alarm-System
This project consists in an IoT Alarm system desgined for indoor environments. It includes a main module that comminucates via MQTT with other small nearby modules. These modules are in charge of sensing the place in order to detect anomalies. If the alarm is activated, a mobile message and an email is sent to inform the user that one of the sensors has detected a presence. In addition to that, the email includes a link to connect to a video streaming.

The main module includes LCD display, keypad matrix, RFID sensor, video camera, leds, and speaker. All of them controlled by a Raspberry Pi 3B and progammed using Python 3.

There are three small modules. Each of them has a different sensor: PIR sensor, magnetic door sensor and distance sensor. All of them controlled by ESP32 sparkfun boards (ESP8266 has also been tested) and programmed using Arduino. 

Project proposed for the consumer electronics subject in ETSIT-UPM in 2018.
