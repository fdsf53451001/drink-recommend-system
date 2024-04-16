import psycopg2
import os
import json
import bcrypt

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
        username = body['username']
        password = body['password']
        # username = 'user3'
        # password = 'user3'
        
        def get_hashed_password(plain_text_password):
            # Hash a password for the first time
            # (Using bcrypt, the salt is saved into the hash itself)
            # Encode the plain_text_password to bytes
            return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt()).decode('utf=8')
        
        def check_password(plain_text_password, hashed_password):
            # Check hashed password. Using bcrypt, the salt is saved into the hash itself
            # Encode the plain_text_password to bytes
            return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)
        
        hashed_password = get_hashed_password(password)
        
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
    
        query = "INSERT INTO users (name, password) VALUES (%s, %s);"
        cursor.execute(query, (username, hashed_password,))
        connection.commit()
        
        return {"statusCode": 200,"body": hashed_password}
    
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
    
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("Connection closed.")
