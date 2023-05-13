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
                    else:
                        ser.write(b'404\n')
                except Exception as e:
                    print(f'Error: {e}')
                finally:
                    connection.close()


async def main():
    print('PYTHON SCRIPT STARTED SUCCESSFULLY')
    await read_serial_data()


if __name__ == '__main__':
    asyncio.run(main())
