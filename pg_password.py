# pip install psycopg2
# pip install bcrypt
import psycopg2
import bcrypt

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="hw_26_09_24",
    user="admin",
    password="admin",
    port=5556
)
cur = conn.cursor()

# Create a table to store hashed passwords
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50),
        hashed_password TEXT
    )
""")
conn.commit()

# danny, 1234 ==> danny, alygfalehbjvfladhv
# 1234 ==> alygfalehbjvfladhv
# 1235 ==> alygfalehbjvflsgf4


# Function to hash and store a password
def create_user(username, password):
    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Insert the username and hashed password into the database
    cur.execute("""
        INSERT INTO users (username, hashed_password)
        VALUES (%s, %s)
    """, (username, hashed_password.decode()))  # Store as text
    conn.commit()


# Function to check a password
def check_password(username, password):
    # Retrieve the hashed password from the database
    cur.execute("SELECT hashed_password FROM users WHERE username = %s", (username,))
    result = cur.fetchone()

    if result:
        hashed_password_from_db = result[0]
        # Compare the provided password with the stored hash
        if bcrypt.checkpw(password.encode(), hashed_password_from_db.encode()):
            print("Password is correct!")
        else:
            print("Incorrect password!")
    else:
        print("Username not found.")


# Example usage
create_user('user1', 'my_password1')  # Creating a new user
check_password('user1', 'my_password1')  # Verifying the password

# Close connection
cur.close()
conn.close()