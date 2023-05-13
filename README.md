# PICC Project

This is a Python script and an Arduino sketch for a PICC (Proximity Integrated Circuit Card) project.

## Description

The project uses an Arduino board with an MFRC522 RFID reader and a piezo buzzer to authenticate PICCs. The Python script runs on a Raspberry Pi and communicates with the Arduino board over serial port. When a PICC is presented to the reader, the Arduino sends the PICC UID to the Raspberry Pi, which checks if the UID is authorized by querying a MySQL database. If the UID is authorized, the Arduino board plays a success tone and lights up a green LED. If the UID is not authorized, the Arduino board plays an error tone and lights up a red LED.

## Installation

1. Clone the repository: `git clone https://github.com/patriicke/rfid.git`
2. Install the required Python packages: `pip install -r requirements.txt`
3. Go to `pcd_device` directory and upload the `pcd_device.ino` sketch to your Arduino board.
4. Connect the MFRC522 RFID reader and the piezo buzzer to your Arduino board.
5. Connect your Arduino board to your device via USB.
6. Create a MySQL database and a table `authorized_cards` with a column `card_uid`.
7. Add authorized PICC UIDs to the `authorized_cards` table.

## Usage

1. Go to `py_script` directory and start the Python script: `python main.py`.
2. Present a PICC to the MFRC522 RFID reader.
3. The Arduino board will play a success or error tone and light up the corresponding LED depending on the UID authorization status `green=success` and `red=error`.
