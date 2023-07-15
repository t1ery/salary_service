import psycopg2


def create_connection():
    try:
        connection = psycopg2.connect(
            user="Enter the username",
            password="Enter the password",
            host="Enter the host",
            port="Enter the port",
            database="Enter the database"
        )
        return connection
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")


def create_table():
    connection = create_connection()
    try:
        cursor = connection.cursor()
        create_table_query = '''CREATE TABLE IF NOT EXISTS employees
            (id SERIAL PRIMARY KEY,
            login VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(50) NOT NULL,
            salary INTEGER NOT NULL,
            next_raise_date DATE NOT NULL,
            token VARCHAR(255),
            token_expiration TIMESTAMP);'''
        cursor.execute(create_table_query)
        connection.commit()
        print("Table created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()


def insert_employee(cursor, login, password, salary, next_raise_date):
    insert_query = f"INSERT INTO employees (login, password, salary, next_raise_date) VALUES ('{login}', '{password}', {salary}, '{next_raise_date}')"
    insert_query += " ON CONFLICT DO NOTHING"
    cursor.execute(insert_query)
