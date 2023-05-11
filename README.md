# RFID Card Reader Application

This application reads the unique ID of RFID cards using the MFRC522 RFID reader and checks their validity against a database on a server.

## Requirements

- Arduino Uno or equivalent board
- MFRC522 RFID reader
- Ethernet Shield W5100
- Piezo buzzer
- Two LEDs (green and red)
- Valid RFID cards database on a server

## Installation

1. Clone the repository on your local machine.
2. Connect the components as per the circuit diagram.
3. Modify the `serverUrl` constant in the `cardReader.ino` file with the URL of the server where the valid cards database is hosted.
4. Upload the `cardReader.ino` file to the Arduino board.
5. Run the server using the `entrypoint.sh` script in the `server` directory.

## Usage

1. Power on the Arduino board and wait for the initialization to complete.
2. Hold a valid RFID card near the RFID reader.
3. If the card is valid, the green LED will turn on, the buzzer will sound a success tone, and the card's unique ID will be displayed on the Serial Monitor.
4. If the card is invalid or not found in the database, the red LED will turn on, the buzzer will sound an error tone, and a message will be displayed on the Serial Monitor.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
