# user_management.py
import mysql.connector
import bcrypt

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

import mysql.connector

class UserManagement:
    def __init__(self, db_config):
        self.db_config = db_config
        self.db = None
        self.cursor = None
        self.connect_db()
        self.connection = mysql.connector.connect(**db_config)

    def connect_db(self):
        try:
            self.db = mysql.connector.connect(**self.db_config)
            self.cursor = self.db.cursor(buffered=True)
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def close_db(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()

    def hash_password(self, password):
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def username_exists(self, username):
        # Check if a username already exists in the database
        query = "SELECT * FROM users WHERE username = %s"
        values = (username,)
        self.cursor.execute(query, values)
        user = self.cursor.fetchone()
        return user is not None

    def email_exists(self, email):
        # Check if an email already exists in the database
        query = "SELECT * FROM users WHERE email = %s"
        values = (email,)
        self.cursor.execute(query, values)
        user = self.cursor.fetchone()
        return user is not None

    def register_user(self, username, password, email, secret_key):
        # Implement user registration logic to insert user data into the MySQL database
        # Use prepared statements to prevent SQL injection

        try:
            # Hash the password and store the user's data in the database, including the secret_key
            hashed_password = self.hash_password(password)
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO users (username, password, email, secret_key) VALUES (%s, %s, %s, %s)",
                           (username, hashed_password, email, secret_key))
            self.connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as err:
            print("Error:", err)
            return False

    def login_user(self, username, password, entered_2fa_code):
        # Implement user login logic to check user credentials against the MySQL database
        # Use prepared statements to prevent SQL injection

        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        values = (username, password)

        self.cursor.execute(query, values)
        user_data = self.cursor.fetchone()

        if user_data:
            user = User(user_data[1], user_data[2])
            return user  # Login successful, return the user object
        else:
            return None  # Login failed

        # Retrieve the user's secret key from the database
        select_query = "SELECT password, 2fa_secret_key FROM users WHERE username = %s"
        values = (username,)

        try:
            self.cursor.execute(select_query, values)
            user_data = self.cursor.fetchone()
            if not user_data:
                return False

            hashed_password, secret_key = user_data

            # Verify the entered password
            if self.verify_password(password, hashed_password):
                # Verify the 2FA code
                totp = pyotp.TOTP(secret_key)
                if totp.verify(entered_2fa_code):
                    return True

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        return False

    def close_db(self):
        # Close the database connection when done
        self.cursor.close()
        self.db.close()
