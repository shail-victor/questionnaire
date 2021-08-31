from flask import request, Blueprint, send_file
from reports.generate_reports import download_report
report_api = Blueprint('report_api', __name__)


@report_api.route('/bvp/generate/report', methods=['GET'])
def report():

    timestamp = request.headers.get("Time-Stamp")
    user_id = request.headers.get("user_id")
    year = request.headers.get("year")
    college_name = request.headers.get("college_name")
    response = download_report(user_id, year, college_name, timestamp)
    return send_file(response, attachment_filename=college_name+"_"+year+".xlsx", as_attachment=True)

