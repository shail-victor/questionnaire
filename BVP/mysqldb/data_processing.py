from mysql_db_connection import get_data_from_db, insert_data_to_db


#(Director_Name, Director_contact_no, director_email_id, name,contact_no, email_id,password,role)

def insert_data():
  insert_query = "INSERT INTO users (College_name,Director_Name, Director_contact_no, director_email_id, name,contact_no, email_id,password,role) " \
                 "VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s)"
  value = [
    ('BVP','Sanjay', '8394483824', "sanjay@gmail.com", 'Shailesh','9162999899','shailesh@gmail.com','shail1234','co-ordinator')
    ]

  insert_data_to_db(insert_query, value, dbname="bvp_db")


def fetch_data():
  query = "select * from users"
  dbname ="bvp_db"
  result = get_data_from_db(query, dbname)
  print(result)

insert_data()
fetch_data()