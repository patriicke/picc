import os

# Enter the path to the text file where the valid card IDs will be stored
valid_card_file = "cards.txt"

def is_valid_card(card_id):
    # Check if the card ID is present in the text file
    with open(valid_card_file, "r") as f:
        valid_cards = f.read().splitlines()
    if card_id in valid_cards:
        return True
    else:
        return False

def add_valid_card(card_id):
    # Add the card ID to the text file if it's not already present
    with open(valid_card_file, "a+") as f:
        f.seek(0)
        if card_id not in f.read().splitlines():
            f.write(card_id + "\n")
            print("Valid card added.")
        else:
            print("Card already exists.")

# Initialize the RFID reader
# ...

while True:
    if not rfid.PICC_IsNewCardPresent():
        continue
    if not rfid.PICC_ReadCardSerial():
        continue
    card_id = "".join([str(rfid.uid.uidByte[i]) for i in range(4)])
    if is_valid_card(card_id):
        # Valid card detected
        # ...
        add_valid_card(card_id)
    else:
        # Invalid card detected
        # ...
        print("Invalid card detected")
        
