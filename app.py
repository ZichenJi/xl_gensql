from flask import Flask, request, render_template
import os
from excel_handler import excel_to_mysql
from sql_executor import get_table_schema, execute_select_sql
from sql_generator import generate_sql

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

current_table = None

@app.route("/", methods=["GET", "POST"])
def index():
    global current_table

    if request.method == "POST" and "file" in request.files:
        file = request.files["file"]

        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            current_table = excel_to_mysql(file_path, file.filename)

            return f"上传成功！当前数据表：{current_table}"

    return render_template("index.html")


@app.route("/query", methods=["POST"])
def query():
    global current_table

    if not current_table:
        return "请先上传Excel文件"

    question = request.form["question"]

    schema_info = get_table_schema(current_table)

    sql = generate_sql(question, current_table, schema_info)[0]

    columns, rows = execute_select_sql(sql)

    result_html = "<h3>生成SQL：</h3><pre>" + sql + "</pre>"
    result_html += "<h3>查询结果：</h3><table border=1>"

    result_html += "<tr>"
    for col in columns:
        result_html += f"<th>{col}</th>"
    result_html += "</tr>"

    for row in rows:
        result_html += "<tr>"
        for cell in row:
            result_html += f"<td>{cell}</td>"
        result_html += "</tr>"

    result_html += "</table>"

    return result_html


if __name__ == "__main__":
    app.run(debug=True)