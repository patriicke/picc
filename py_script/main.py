import pymysql
import serial
import asyncio

async def connect_to_database():
    connection = pymysql.connect(
        host='localhost',
        user='patriicke',
        password='DATAbase@123',
        db='picc_project',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.Cursor
    )
    return connection

ser = serial.Serial('/dev/ttyACM0', 9600)

products = [
    {"id": 1, "name": "Coca Cola", "price": 2000},
    {"id": 2, "name": "Fanta", "price": 3500},
    {"id": 3, "name": "Sprite", "price": 5000},
    {"id": 4, "name": "Red Bull", "price": 10000},
    {"id": 5, "name": "Monster", "price": 4500},
    {"id": 6, "name": "Pepsi", "price": 1000},
    {"id": 7, "name": "7up", "price": 9000},
    {"id": 8, "name": "Dr Pepper", "price": 500},
    {"id": 9, "name": "Lipton Ice Tea", "price": 4800},
    {"id": 10, "name": "Snickers", "price": 8000},
]


async def read_serial_data():
    with serial.Serial('/dev/ttyACM0', 9600) as ser:
        while True:
            data = ser.readline().decode('utf-8').strip()
            if data != "200" and data != "404":
                print(f"Card: {data}")
                try:
                    connection = await connect_to_database()
                    cursor = connection.cursor()
                    sql = 'SELECT * FROM authorized_cards WHERE card_uid = %s'
                    cursor.execute(sql, data)
                    result = cursor.fetchall()
                    if result:
                        ser.write(b'200\n')
                        await handle_card_interaction(data)
                    else:
                        ser.write(b'404\n')
                except Exception as e:
                    print(f'Error: {e}')
                finally:
                    connection.close()

async def handle_card_interaction(card_uid):
    while True:
        print("Choose an option:")
        print("1. Top up")
        print("2. Check balance")
        print("3. Buy product")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            await top_up(card_uid)
        elif choice == "2":
            await check_balance(card_uid)
        elif choice == "3":
            await buy_product(card_uid)
        elif choice == str(0):
            print("Exiting... \n")
            print("Place a card here to continue.")
            break
        else:
            print("Invalid choice. Try again.")

async def top_up(card_uid):
    amount = float(input("Enter the amount to top up: "))
    try:
        connection = await connect_to_database()
        cursor = connection.cursor()
        sql = "UPDATE authorized_cards SET balance = balance + %s WHERE card_uid = %s"
        cursor.execute(sql, (amount, card_uid))
        connection.commit()
        print("Top-up successful!")
    except Exception as e:
        print(f'Error: {e}')
    finally:
        connection.close()

async def check_balance(card_uid):
    try:
        connection = await connect_to_database()
        cursor = connection.cursor()
        sql = "SELECT balance FROM authorized_cards WHERE card_uid = %s"
        cursor.execute(sql, card_uid)
        result = cursor.fetchone()
        if result:
            balance = result[0]
            print(f"Balance: {balance}")
        else:
            print("Card not found.")
    except Exception as e:
        print(f'Error: {e}')
    finally:
        connection.close()

async def buy_product(card_uid):
    print("Available products:")
    for product in products:
        print(f"{product['id']}. {product['name']} - Price: {product['price']}")

    product_id = int(input("Enter the product ID: "))
    selected_product = next((product for product in products if product['id'] == product_id), None)
    if selected_product:
        try:
            connection = await connect_to_database()
            cursor = connection.cursor()
            sql = "SELECT balance, points FROM authorized_cards WHERE card_uid = %s"
            cursor.execute(sql, card_uid)
            result = cursor.fetchone()
            if result:
                balance = result[0]
                points = result[1]
                if balance >= selected_product['price']:
                    updated_balance = balance - selected_product['price']
                    updated_points = points + 1  # Increment points by 1
                    sql = "UPDATE authorized_cards SET balance = %s, points = %s WHERE card_uid = %s"
                    cursor.execute(sql, (updated_balance, updated_points, card_uid))
                    connection.commit()
                    print("Purchase successful!")
                else:
                    print("Insufficient balance.")
            else:
                print("Card not found.")
        except Exception as e:
            print(f'Error: {e}')
        finally:
            connection.close()
    else:
        print("Invalid product ID.")

async def main():
    print('PYTHON SCRIPT STARTED SUCCESSFULLY')
    await read_serial_data()


if __name__ == '__main__':
    asyncio.run(main())