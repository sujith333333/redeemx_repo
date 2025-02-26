import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

import uuid
from datetime import datetime
from src.user.utils import hash_password
from src.user.models import User
import pymysql
import os

# # Data to insert
data_to_insert = (str(uuid.uuid4()), datetime.utcnow(), "admin", "admin", hash_password("admin"), "admin", "admin@gmail.com", 987078907, True, False, False)

# SQL query for inserting data
insert_query = "INSERT INTO user (id, created_at, name, username, password, emp_id, email, mobile_number, is_admin, is_vendor, is_user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

# Using 'with' to manage the connection and cursor

def fun():
    # import pdb; pdb.set_trace()
    with pymysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), database=os.getenv("DB_NAME")) as connection:
        with connection.cursor() as cursor:
            
            # Execute the insert query with the data
            cursor.execute(insert_query, data_to_insert)
            
            # Commit the transaction to save the changes
            connection.commit()

            print("Data inserted successfully!")

fun()