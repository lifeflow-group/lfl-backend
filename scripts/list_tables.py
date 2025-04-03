import psycopg2
import os
from dotenv import load_dotenv

# python scripts/list_tables.py

# Load environment variables from the .env file
load_dotenv()

# Get DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to the database
try:
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()

    # Execute a simple query to check the connection
    cursor.execute(
        """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public';
    """
    )
    rows = cursor.fetchall()

    # Print the results to the screen
    for row in rows:
        print(row)

except Exception as e:
    print(f"Error: {e}")

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
