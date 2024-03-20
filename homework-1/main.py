"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2
import csv

conn = psycopg2.connect(host="localhost", database="north", user="postgres", password="1479")

try:
    with conn:
        with conn.cursor() as cur:
            tables = ['customers_data.csv', 'employees_data.csv', 'orders_data.csv']

            for table in tables:
                path = 'north_data/' + table

                with open(path, 'r', newline='\n', encoding='windows-1251') as f:
                    reader = csv.DictReader(f)

                    if table == 'customers_data.csv':
                        for line in reader:
                            cur.execute("INSERT INTO customers VALUES (%s, %s, %s)",
                                        (line['customer_id'], line['company_name'], line['contact_name']))

                    elif table == 'employees_data.csv':
                        for line in reader:
                            cur.execute("INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s)",
                                        (line['employee_id'], line['first_name'], line['last_name'],
                                         line['title'], line['birth_date'], line['notes']))

                    elif table == 'orders_data.csv':
                        for line in reader:
                            cur.execute("INSERT INTO orders VALUES (%s, %s, %s, %s, %s)",
                                        (line['order_id'], line['customer_id'], line['employee_id'],
                                         line['order_date'], line['ship_city']))

            cur.execute("SELECT * FROM customers")

            rows = cur.fetchall()
            for row in rows:
                print(row)

except Exception as ex:
    print('[INFO] Error while working with PostgreSQL', ex)

finally:
    conn.close()
