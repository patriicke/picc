#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9

MFRC522 rfid(SS_PIN, RST_PIN);
MFRC522::MIFARE_Key key;

byte nuidPICC[4];

int LED_GREEN_PIN = 2;
int LED_RED_PIN = 3;

int PIEZO_BUZZER_PIN = 7;

int ERROR_FREQUENCY = 300;
int SUCCESS_FREQUENCY = 1000;

void setup()
{
  pinMode(LED_GREEN_PIN, OUTPUT);
  pinMode(LED_RED_PIN, OUTPUT);

  pinMode(PIEZO_BUZZER_PIN, OUTPUT);

  Serial.begin(9600);

  SPI.begin();
  rfid.PCD_Init();
  for (byte i = 0; i < 6; i++)
  {
    key.keyByte[i] = 0xFF;
  }
}

void loop()
{
  if (!rfid.PICC_IsNewCardPresent())
  {
    return;
  }

  if (!rfid.PICC_ReadCardSerial())
  {
    return;
  }

  if (rfid.uid.uidByte[0] != nuidPICC[0] ||
      rfid.uid.uidByte[1] != nuidPICC[1] ||
      rfid.uid.uidByte[2] != nuidPICC[2] ||
      rfid.uid.uidByte[3] != nuidPICC[3])
  {
    for (byte i = 0; i < 4; i++)
    {
      nuidPICC[i] = rfid.uid.uidByte[i];
    }
    printHex(rfid.uid.uidByte, rfid.uid.size);
  }
  else
  {
    printHex(rfid.uid.uidByte, rfid.uid.size);
  }

  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();

  if (Serial.available())
  {
    String message = Serial.readStringUntil('\n');
    if (strcmp(message.c_str(), "200") == 0)
    {
      authorized();
    }
    else
    {
      notAuthorized();
    }
  }
}

void printHex(byte *buffer, byte bufferSize)
{
  for (byte i = 0; i < bufferSize; i++)
  {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
  Serial.println("");
}

void authorized()
{
  digitalWrite(LED_GREEN_PIN, HIGH);
  tone(PIEZO_BUZZER_PIN, SUCCESS_FREQUENCY, 800);
  delay(1500);
  digitalWrite(LED_GREEN_PIN, LOW);
}

void notAuthorized()
{
  digitalWrite(LED_RED_PIN, HIGH);
  tone(PIEZO_BUZZER_PIN, ERROR_FREQUENCY, 300);
  delay(800);
  tone(PIEZO_BUZZER_PIN, ERROR_FREQUENCY, 300);
  delay(800);
  tone(PIEZO_BUZZER_PIN, ERROR_FREQUENCY, 300);
  digitalWrite(LED_RED_PIN, LOW);
}
