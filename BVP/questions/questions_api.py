from pathlib import Path
import pandas as pd
from datetime import date
from mysqldb.mysql_db_connection import insert_dataframe_to_db, delete_records_from_db, get_data_from_db, insert_data_to_db
from werkzeug.utils import secure_filename
import os


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','docx','xlsx', 'csv'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def question_details(request_body, timestamp):
    request_df = pd.DataFrame(request_body)
    q_no = request_df["q_no"][0]
    request_df = request_df.drop(["q_no"], axis=1)
    request_df["user_year_id"] = request_df["user_id"]+"_" + str(date.today().year)
    user_year_id = request_df["user_year_id"][0]
    table_name = "question_" + q_no
    db_name = "bvp_db"
    delete_query = f"DELETE FROM {table_name} WHERE user_year_id='{user_year_id}'"
    # deleting records of user_year_id
    record_count = delete_records_from_db(delete_query, db_name)
    # adding new records
    response = insert_dataframe_to_db(request_df, table_name, db_name)
    status = {"status": "Failure"}
    if response:
        status = {"status": "Success"}
    return status


def get_questions_details(user_id, question_no, timestamp):
    table_name = "question_" + question_no
    user_year_id = user_id + "_" + str(date.today().year)
    get_query = f"select * from {table_name} where user_year_id = '{user_year_id}'"
    question_df = get_data_from_db(get_query, "bvp_db")
    if not question_df.empty:
        question_df = question_df.drop(["user_year_id", "user_id"], axis=1)
        response = question_df.to_dict("records")
    else:
        response=[]
    return response


def upload_files_to_server(request):
    timestamp = request.headers.get("Time-Stamp")
    user_id = request.headers.get("user_id")
    question_no = request.args['q_no']

    status = {"status": "Failure"}
    insert_query = "INSERT INTO uploaded_files (user_year_id, user_id, question_no, file_path) " \
                       "VALUES (%s, %s, %s, %s)"
    values = []
    if 'files[]' in request.files:
        files = request.files.getlist('files[]')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                user_year_id = user_id + "_" + str(date.today().year)
                upload_filename = user_year_id  + "_"+question_no + "_"+filename
                project_dir = str(Path(__file__).parent.parent)
                file_path = os.path.join(project_dir,"data", upload_filename)
                file.save(file_path)
                values.append((user_year_id, user_id,question_no, file_path))

        row_count = insert_data_to_db(insert_query, values, dbname="bvp_db")
        if row_count:
            status = {"status": "Success"}

    return status


