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
        body = json.loads("{}".format(event['body']))
        store_name = body['store_name']
        # store_name = '五桐號-台北內湖江南店'
        
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
        
        query = "SELECT drink_name, calories, ingredients, price FROM beverage_info WHERE store_name=%s;"
        cursor.execute(query, (store_name,))
        rows = cursor.fetchall()
        
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
