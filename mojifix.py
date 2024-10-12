import os
import mariadb
import ftfy
import argparse

# Get environment variables for MariaDB connection
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

def fix_encoding(table, column, primary):
    try:
        # Establish the database connection
        connection = mariadb.connect(
            host='localhost',
            database=MYSQL_DATABASE,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )

        print(f"Connected to MariaDB database '{database}'.")

        cursor = connection.cursor(dictionary=True)

        # Fetch all rows from the table and column
        select_query = f"SELECT {primary} AS id, {column} FROM {table}"
        cursor.execute(select_query)
        rows = cursor.fetchall()

        # Iterate through each row and fix encoding
        for row in rows:
            original_value = row[column]
            
            # Skip rows where the column value is None (empty)
            if original_value is None:
                print(f"Skipping row {row['id']} - no value in column '{column}'")
                continue

            # Fix the encoding using ftfy
            fixed_value = ftfy.fix_text(original_value)
            
            # If the value has been fixed, update the row
            if original_value != fixed_value:
                update_query = f"UPDATE {table} SET {column} = %s WHERE {primary} = %s"
                cursor.execute(update_query, (fixed_value, row['id']))
                print(f"Fixed encoding for row {row['id']}")

        # Commit the updates to the database
        connection.commit()
        print(f"Encoding fix applied to column '{column}' in table '{table}'.")

    except mariadb.Error as e:
        print(f"Error while connecting to MariaDB: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("MariaDB connection is closed.")

if __name__ == '__main__':
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Fix encoding in a MariaDB table column using ftfy.')
    parser.add_argument('table', type=str, help='Name of the MariaDB table')
    parser.add_argument('column', type=str, help='Name of the column to fix encoding')
    parser.add_argument('primary', type=str, help='Name of the primary key for this column')

    # Parse command line arguments
    args = parser.parse_args()

    table = args.table
    column = args.column
    primary = args.primary

    if not MYSQL_DATABASE or not MYSQL_USER or not MYSQL_PASSWORD:
        print("Please set the MYSQL_DATABASE, MYSQL_USER, and MYSQL_PASSWORD environment variables.")
    else:
        # Call the function to fix encoding
        fix_encoding(table, column, primary)
