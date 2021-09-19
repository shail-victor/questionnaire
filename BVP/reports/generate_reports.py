import pandas as pd
from mysqldb.mysql_db_connection import connect_mysqldb
from reports.question_data import questions_list
from io import BytesIO
from constants import criteria3_db_name



def download_report(user_id, year, college_name, timestamp):
    mydb_connection = None
    mycursor = None

    try:
        user_year_id = user_id + "_" + year
        question_data = pd.DataFrame(questions_list,
                                     columns=['id', "questionid", 'question', 'columnDefs', 'isMultipleTable',
                                              "TableHeading"])
        mydb_connection = connect_mysqldb(criteria3_db_name)
        mycursor = mydb_connection.cursor()

        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        workbook = writer.book
        worksheet = workbook.add_worksheet("Criterion III")

        criteria_format = workbook.add_format(
            {'text_wrap': True, 'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter',
             'fg_color': '#E59866', 'font_color': 'blue', 'font_size': 26})

        worksheet.merge_range('E9:T14', f"Criterion III – Research, Innovations and Extension\n {college_name} ", criteria_format)

        for index, row in question_data.iterrows():
            table_name = "question" + "_" + str(row["id"])
            mycursor.execute(f"select * from {table_name} where user_year_id = '{user_year_id}'")
            result_df = pd.DataFrame(mycursor.fetchall())

            if "_" in str(row["id"]):
                row["id"] = row["id"].replace("_", ".")

            if not result_df.empty:
                print(f"data found for table: {table_name}")
                result_df.columns = mycursor.column_names
                result_df = result_df.drop(columns=["user_year_id", "user_id"])
                question_columns = pd.DataFrame(row["columnDefs"])["headerName"].to_list()
                result_df.columns = question_columns

                result_df.to_excel(writer, sheet_name=row["questionid"], index=False, startcol=2, startrow=12,
                                   header=False, encoding='utf8')

                workbook = writer.book
                worksheet = writer.sheets[row["questionid"]]

                # Create a format to use in the merged range.
                merge_format = workbook.add_format({'text_wrap': True, 'bold': 1, 'border': 1, 'align': 'left', 'valign': 'vcenter',
                    'fg_color': '#EEE8AA', 'font_color': 'blue', 'font_size':12})

                worksheet.merge_range('B1:G8', str(row["id"]) + ".   " + row["question"], merge_format)

                # Header
                format_header = workbook.add_format(
                    {'text_wrap': True, 'align': 'center', 'bold': True, 'font_color': 'red', 'border': 5,
                     'bg_color':"#87CEEB"})

                # Write the header manually
                for colx, value in enumerate(result_df.columns.values):
                    worksheet.write(11, 2 + colx, value)

                worksheet.conditional_format(f'C12:{chr(1 + 65 + len(result_df.columns)) + "12"}',
                                             {'type': 'no_blanks', 'format': format_header})

                # data
                data_format = workbook.add_format(
                    {'text_wrap': True, 'align': 'center', 'bold': True, 'font_color': 'black'})
                worksheet.set_column(f'C13:{chr(1 + 65 + len(result_df.columns)) + str(12 + result_df.shape[0])}', 35,
                                     cell_format=data_format)

                # border
                border_fmt = workbook.add_format({'bottom': 5, 'top': 5, 'left': 5, 'right': 5, 'bg_color': '#E8E3E2'})
                worksheet.conditional_format(f'C13:{chr(1 + 65 + len(result_df.columns)) + str(12 + result_df.shape[0])}',
                                             {'type': 'no_errors', 'format': border_fmt})



        # the writer has done its job
        writer.close()
        #writer.save()

        # go back to the beginning of the stream
        output.seek(0)

        return output
    except Exception as e:
        print(e)
    finally:
        mycursor.close()
        mydb_connection.close()
