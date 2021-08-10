import mysql.connector
import pandas as pd
from sqlalchemy import create_engine


def connect_mysqldb(dbname, hostname="localhost", username="root", password="root"):
    mydb_connection = mysql.connector.connect(host=hostname, port=3306, user=username, password=password,database=dbname)
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


def insert_dataframe_to_db(df, table_name, db_name):

    engine = create_engine("mysql+mysqlconnector://{user}:{pw}@{host}/{db}"
                           .format(host="localhost", db=db_name, user="root", pw="root"))

    #engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(user="root", pw="root1234", db=db_name))

    df.to_sql(name=table_name, con=engine,  if_exists='append', index=False, chunksize = 1000)

    return 1


def delete_records_from_db(query, dbname):
    mydb_connection = connect_mysqldb(dbname)
    mycursor = mydb_connection.cursor()
    mycursor.execute(query)
    mydb_connection.commit()
    print(mycursor.rowcount, "rows deleted.")
    mycursor.close()
    mydb_connection.close()
    return mycursor.rowcount