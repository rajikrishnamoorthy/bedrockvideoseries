import json
import sqlite3

def lambda_handler(event, context):
    # Vulnerability 1: SQL Injection
    user_id = event['user_id']
    conn = sqlite3.connect('/tmp/database.db')
    cursor = conn.cursor()
    
    # Directly inserting user input into the query without sanitization
    query = f"SELECT * FROM users WHERE id = {user_id};"
    cursor.execute(query)
    
    # Vulnerability 2: Sensitive data exposure in logs
    result = cursor.fetchall()
    print(f"User data: {result}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Query executed successfully')
    }

