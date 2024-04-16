import psycopg2
import os
import json

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
        place = None
        if 'place' in body:
            place = body['place']
        
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
    
        
        if place:
            query = "SELECT DISTINCT store_name, address, company_description FROM beverage_info WHERE position(%s in address)>0;"
            cursor.execute(query, (place,))
            rows = cursor.fetchall()
        else:
            query = "SELECT DISTINCT store_name, address, company_description FROM beverage_info"
            cursor.execute(query)
            rows = cursor.fetchall()
        
        
        # if not rows:
        #     return {"statusCode": 401,"body": "Unauthorized"}
        
        # id = rows[0][0]
        # query = "UPDATE users SET score=%s WHERE id=%s;";
        # cursor.execute(query, (score, id))
        # connection.commit()
        
        return {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST,GET'
            },
            "body": json.dumps({'rows':rows})
        }
    
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
    
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("Connection closed.")
