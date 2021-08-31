
from mysqldb.mysql_db_connection import get_data_from_db, insert_data_to_db


def user_info(email_id, password, timestamp):
    query = f"select user_id, password, role from users where email_id ='{email_id}'"
    dbname = "bvp_db"
    result = get_data_from_db(query, dbname)
    if not result.empty:
        db_password = result["password"][0]
        user_id = str(result["user_id"][0])
        role = result["role"][0]
        if db_password == password:
            status = {"status": "Success", "reason":"", "user_id": user_id, "role": role}
        else:
            status = {"status": "Failure", "reason":"Invalid Password", "user_id": "", "role": ""}
    else:
        status = {"status": "Failure", "reason": "User does not exist", "user_id": "", "role":""}
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


def get_all_users(timestamp):
    query = f"select user_id,college_name, name, email_id from users"
    dbname = "bvp_db"
    result = get_data_from_db(query, dbname)
    response =[]
    if not result.empty:
        result["co_ordinator"] = result["college_name"]+", "+result["email_id"]
        result = result.drop(columns=["college_name", "email_id"], axis=1)
        response = result.to_dict("records")

    return response


def get_all_years(user_id, timestamp):
    query = f"SELECT distinct user_year_id FROM question_28 where user_id='{user_id}'"
    dbname = "bvp_db"
    result = get_data_from_db(query, dbname)
    response = []
    if not result.empty:
        result["year"] = result["user_year_id"].apply(lambda user_year_id: int(user_year_id.split("_")[1]))
        response = result["year"].sort_values().tolist()
    return response

