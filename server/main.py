from fastapi import FastAPI
import pymysql

app = FastAPI()

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

@app.get('/')
def welcome():
    return {
        "message": "Welcome to our PICC Card Validator on SERVER",
        "success": True,
    }

@app.get('/cards/{card_uid}')
def get_card(card_uid: str):
    connection = connect()
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM authorized_cards WHERE card_uid = %s'
            cursor.execute(sql, card_uid)
            result = cursor.fetchone()
    finally:
        connection.close()

    if result:
        return result
    else:
        return {'error': 'Card not found'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
