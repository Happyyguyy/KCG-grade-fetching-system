from flask import Flask, render_template, request
import mysql.connector as MySQL

app = Flask(__name__)
app.config["HOST"] = "0.0.0.0"
# app.config["FLASK_ENV"] = "development"

# Config MySQL
config = {
    "user": "root",
    "password": "",
    "database": "kcg_grading",
    "unix_socket": "C:/xampp/mysql/mysql.sock"
}

# init MySQL
db = MySQL.connect(**config)
print(db)
cur = db.cursor()


def get_data(cols, sort, assembly):
    # for k, v in kwargs.items():
    #     print(k, v
    # print(str(kwargs["colselection"]).replace(
    # "['", "").replace("']", ""), str(kwargs['fromtable']).replace(
    #     "['", "").replace("']", ""))
    if not sort:
        sort = "''"
    print(sort)
    cur.execute(
        f"SELECT {', '.join(cols)} FROM leg_data LEFT JOIN leg_grades USING (id) WHERE assembly={assembly} ORDER BY {sort}")
    data = cur.fetchall()
    return data



@app.route("/", methods=["GET", "POST"])
def main():
    print(request.method)
    if request.method == "POST":
        print(request.form)
        headers = [k.title() for k, v in request.form.items() if v == "on"]
        sort_by = request.form["sortBy"]
        assembly = request.form["assembly"]
        data = get_data(headers, sort_by, assembly)

        return render_template("main.html", headers=headers, data=data)

    else:
        return render_template("main.html")
