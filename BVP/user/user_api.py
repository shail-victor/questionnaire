
from mysqldb.mysql_db_connection import get_data_from_db, insert_data_to_db


def user_info(email_id, password, timestamp):
    query = f"select password from users where email_id ='{email_id}'"
    dbname = "bvp_db"
    result = get_data_from_db(query, dbname)
    if not result.empty:
        db_password = result["password"][0]
        if db_password == password:
            status = {"status": "Success", "reason":""}
        else:
            status = {"status": "Failure", "reason":"invalid password"}
    else:
        status = {"status": "Failure", "reason": "user does not exist"}
    return status


def register_user(user_details, timestamp):
    query = f"select password from users where email_id ='{user_details['email_id']}'"
    dbname = "bvp_db"
    result = get_data_from_db(query, dbname)
    if result.empty:
        insert_query = "INSERT INTO users (College_name,Director_Name, Director_contact_no, director_email_id, name,contact_no, email_id,password,role) " \
                       "VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s)"
        value = [(user_details['college_name'], user_details['director_name'], user_details['director_contact_no'],
             user_details['director_email_id'], user_details['name'], user_details['contact_no'],
                  user_details['email_id'], user_details['password'], user_details['role'])]
        row_count = insert_data_to_db(insert_query, value, dbname="bvp_db")
        if row_count:
            status = {"status": "Success", "reason": ""}
        else:
            status = {"status": "Failure", "reason": "insertion failed"}
    else:
        status = {"status": "Failure", "reason": "user already exist"}

    return status


