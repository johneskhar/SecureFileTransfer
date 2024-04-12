import mysql.connector


def get_database_connection():
    return mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        password="johnes24",
        database="secure_file_transfer"
    )

def get_files_by_user_id(user_id, is_encrypted=True):
    connection = get_database_connection()
    cursor = connection.cursor()

    try:
        # Select files based on user_id and encryption status
        table_name = "encrypted_files" if is_encrypted else "decrypted_files"
        select_query = f"SELECT file_id, file_path, {'date_encrypted' if is_encrypted else 'date_decrypted'} FROM {table_name} WHERE user_id = %s"
        cursor.execute(select_query, (user_id,))
        files = cursor.fetchall()
        return files

    except Exception as e:
        print(f"Error fetching files: {e}")
        return []

    finally:
        connection.close()

def save_encrypted_file_info(user_id, file_path, date_encrypted):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        # Insert the encrypted file information into the database
        insert_query = "INSERT INTO encrypted_files (user_id, file_path, date_encrypted) VALUES (%s, %s, %s)"
        values = (user_id, file_path, date_encrypted)  # Add user_id to the values tuple
        cursor.execute(insert_query, values)

        # Commit the changes and close the connection
        connection.commit()
    except Exception as e:
        print(f"Error saving encrypted file info: {e}")
    finally:
        connection.close()


def save_decrypted_file_info(user_id, file_path, date_decrypted):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        # Insert the decrypted file information into the database
        insert_query = "INSERT INTO decrypted_files (user_id, file_path, date_decrypted) VALUES (%s, %s, %s)"
        values = (user_id, file_path, date_decrypted)  # Add user_id to the values tuple
        cursor.execute(insert_query, values)

        # Commit the changes and close the connection
        connection.commit()
    except Exception as e:
        print(f"Error saving decrypted file info: {e}")
    finally:
        connection.close()


def get_encrypted_files(user_id=None):
    connection = get_database_connection()
    cursor = connection.cursor()

    # Select encrypted files
    if user_id is None:
        select_query = "SELECT file_id, file_path, date_encrypted FROM encrypted_files"
        cursor.execute(select_query)
    else:
        select_query = """
        SELECT ef.file_id, ef.file_path, ef.date_encrypted
        FROM encrypted_files ef
        JOIN users u ON ef.user_id = u.user_id
        WHERE u.user_id = %s
        """
        cursor.execute(select_query, (user_id,))

    encrypted_files = cursor.fetchall()

    # Close the connection
    connection.close()

    return encrypted_files


def get_decrypted_files(user_id=None):
    connection = get_database_connection()
    cursor = connection.cursor()

    # Select decrypted files
    if user_id is None:
        select_query = "SELECT file_id, file_path, date_decrypted FROM decrypted_files"
        cursor.execute(select_query)
    else:
        select_query = """
        SELECT df.file_id, df.file_path, df.date_decrypted
        FROM decrypted_files df
        JOIN users u ON df.user_id = u.user_id
        WHERE u.user_id = %s
        """
        cursor.execute(select_query, (user_id,))

    decrypted_files = cursor.fetchall()

    # Close the connection
    connection.close()

    return decrypted_files

def get_all_encrypted_files():
    connection = get_database_connection()
    cursor = connection.cursor()

    # Select all encrypted files
    select_query = "SELECT file_id, file_path, date_encrypted FROM encrypted_files"
    cursor.execute(select_query)
    encrypted_files = cursor.fetchall()

    # Close the connection
    connection.close()

    return encrypted_files

def get_all_decrypted_files():
    connection = get_database_connection()
    cursor = connection.cursor()

    # Select all decrypted files
    select_query = "SELECT file_id, file_path, date_decrypted FROM decrypted_files"
    cursor.execute(select_query)
    decrypted_files = cursor.fetchall()

    # Close the connection
    connection.close()

    return decrypted_files


def delete_file(file_path, is_encrypted):
    connection = get_database_connection()
    cursor = connection.cursor()

    try:
        # Determine the table name based on the encryption status
        table_name = "encrypted_files" if is_encrypted else "decrypted_files"

        # Delete the file from the appropriate table based on the file path
        delete_query = f"DELETE FROM {table_name} WHERE file_path = %s"
        cursor.execute(delete_query, (file_path,))

        print(f"Deleted file {file_path} from {table_name} table")

        # Commit the changes
        connection.commit()

    except Exception as e:
        # Rollback the transaction in case of an error
        connection.rollback()
        print(f"Error deleting file: {e}")
        raise e

    finally:
        # Close the connection
        connection.close()


def get_current_user_id():
    # Placeholder function to return the current user ID
    # Implement this function based on your user management system
    # This could involve session management or querying user information from the database
    # For demonstration purposes, returning a static user ID here
    return 1  # Assuming the user ID is 1