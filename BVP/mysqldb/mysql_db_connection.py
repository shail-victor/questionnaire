import mysql.connector
import pandas as pd


def connect_mysqldb(dbname, hostname="localhost", username="root", password="@Root1234"):
    mydb_connection = mysql.connector.connect(host=hostname, user=username, password=password,database=dbname)
    if mydb_connection:
        print("Connected to Mysql")
    else:
        print("Connection Failed!!!!")

    return mydb_connection


def get_data_from_db(query, database):
    mydb_connection = connect_mysqldb(database)
    mycursor = mydb_connection.cursor()
    mycursor.execute(query)
    #myresult = mycursor.fetchall()
    result_df = pd.DataFrame(mycursor.fetchall())
    if not result_df.empty:
        result_df.columns = mycursor.column_names
    mycursor.close()
    mydb_connection.close()
    return result_df


def insert_data_to_db(query, value, dbname):
    mydb_connection = connect_mysqldb(dbname)
    mycursor = mydb_connection.cursor()
    mycursor.executemany(query, value)
    mydb_connection.commit()
    print(mycursor.rowcount, "rows inserted.")
    mycursor.close()
    mydb_connection.close()
    return mycursor.rowcount
