import pymysql
import serial

def connect():
    connection = pymysql.connect(
        host='localhost',
        user='patriicke',
        password='DATAbase@123',
        db='picc_project',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection


while True:
    sr = serial.Serial('/dev/ttyACM0', 9600)
    data = sr.readline().decode('utf-8').strip()
    card  = ''
    
    if "****"  in data or 'This card was' in data:
        continue
    elif "READING" in data:
        print(data)
    else:
        card = data;
        print("Card: ", card)
        connection = connect()
        try:
            with connection.cursor() as cursor:
                sql = 'SELECT * FROM authorized_cards WHERE card_uid = %s'
                cursor.execute(sql, card)
                result = cursor.fetchone()
        finally:
            connection.close()
    
        if result:
            sr.write(b'200')
            print("200")
        else:
            sr.write(b'404')
            print("404")
        