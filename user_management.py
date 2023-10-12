import bcrypt
import mysql.connector
import pyotp

class UserManagement:
    def __init__(self, db_config):
        self.db_config = db_config
        self.db = None
        self.cursor = None
        self.connect_db()

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

    def verify_password(self, provided_password, hashed_password):
        # Verify a password by encoding the strings as bytes
        provided_password_bytes = provided_password.encode('utf-8')
        hashed_password_bytes = hashed_password.encode('utf-8')

        return bcrypt.checkpw(provided_password_bytes, hashed_password_bytes)

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

    def register_user(self, username, password, email):
        # Implement user registration logic to insert user data into the MySQL database
        # Use prepared statements to prevent SQL injection

        if self.username_exists(username):
            return False, "Username already exists. Please choose a different username."

        if self.email_exists(email):
            return False, "Email already exists. Please use a different email address."

        try:
            # Hash the password
            hashed_password = self.hash_password(password)

            # Generate a random secret key for 2FA
            secret_key = pyotp.random_base32()

            # Insert user data, including the secret_key
            insert_query = "INSERT INTO users (username, password, email, 2fa_secret_key) VALUES (%s, %s, %s, %s)"
            insert_values = (username, hashed_password, email, secret_key)

            self.cursor.execute(insert_query, insert_values)
            self.db.commit()

            return True, "Successfully registered.", secret_key  # Return secret_key on success

        except mysql.connector.Error as err:
            print("Error:", err)
            return False, "Registration failed.", None  # Return None for secret_key

    def login_user(self, username, password):
        # Implement user login logic to check user credentials against the MySQL database
        # Use prepared statements to prevent SQL injection

        query = "SELECT username, password, 2fa_secret_key FROM users WHERE username = %s"
        values = (username,)

        self.cursor.execute(query, values)
        user_data = self.cursor.fetchone()

        if user_data:
            stored_username, stored_password, secret_key = user_data
            if self.verify_password(password, stored_password):
                return True, secret_key, stored_username  # Login successful, return True, the secret key, and the username
            else:
                return False, None, None  # Incorrect password, return False and no secret key and username
        else:
            return False, None, None  # Username not found, return False and no secret key and username

    def generate_secret_key(self, username):
        # Generate a secret key for the user and store it in the database
        secret_key = pyotp.random_base32()
        query = "UPDATE users SET 2fa_secret_key = %s WHERE username = %s"
        values = (secret_key, username)
        self.cursor.execute(query, values)
        self.db.commit()

    def verify_2fa_code(self, username, entered_2fa_code):
        # Retrieve the user's secret_key from the database
        select_query = "SELECT 2fa_secret_key FROM users WHERE username = %s"
        values = (username,)

        try:
            self.cursor.execute(select_query, values)
            user_data = self.cursor.fetchone()
            if not user_data:
                return False

            secret_key = user_data[0]

            # Verify the entered 2FA code
            totp = pyotp.TOTP(secret_key)
            if totp.verify(entered_2fa_code):
                return True

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        return False

    def get_secret_key(self, email):
        query = "SELECT 2fa_secret_key FROM users WHERE username = %s"
        values = (email,)

        self.cursor.execute(query, values)
        user_data = self.cursor.fetchone()

        if user_data:
            return user_data[0]  # Assuming the secret key is in the first column
        else:
            return None  # Handle the case where the user is not found

class User:
    def __init__(self, username, email, secret_key):
        self.username = username
        self.email = email
        self.secret_key = secret_key
