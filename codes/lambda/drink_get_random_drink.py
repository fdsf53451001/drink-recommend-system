import psycopg2
import os
import json
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)
        
# Replace these values with your actual database connection details
db_host = os.environ['DB_HOST']
db_port = os.environ['DB_PORT']
db_name = os.environ['DB_NAME']
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']

def lambda_handler(event, context):
    connection, cursor = None, None
    
    try:
        
        # Establish a connection to the database
        connection = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password,
            connect_timeout=3
        )
    
        # Create a cursor object to interact with the database
        cursor = connection.cursor()
        
        query = "SELECT store_name, drink_name, calories, ingredients, price FROM beverage_info ORDER BY RANDOM()LIMIT 3"
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # if not rows:
        #     return {"statusCode": 401,"body": "Unauthorized"}
        
        # id = rows[0][0]
        # query = "UPDATE users SET score=%s WHERE id=%s;";
        # cursor.execute(query, (score, id))
        # connection.commit()
        
        return {"statusCode": 200,"body": json.dumps({'rows':rows}, cls=DecimalEncoder)}
    
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
    
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("Connection closed.")
