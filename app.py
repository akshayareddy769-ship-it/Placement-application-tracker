from pathlib import Path
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DATABASE = Path(__file__).resolve().parent / "applications.db"

STATUSES = [
    "Applied",
    "Interview Scheduled",
    "Selected",
    "Rejected"
]


def get_connection():
    connection = sqlite3.connect(str(DATABASE))
    connection.row_factory = sqlite3.Row
    return connection


with get_connection() as connection:
    connection.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            application_date TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)


@app.route("/")
def home():
    search = request.args.get("search", "").strip()
    selected_status = request.args.get("filter_status", "")

    query = "SELECT * FROM applications WHERE company LIKE ?"
    parameters = ["%" + search + "%"]

    if selected_status in STATUSES:
        query += " AND status = ?"
        parameters.append(selected_status)
    else:
        selected_status = ""

    query += " ORDER BY id DESC"

    with get_connection() as connection:
        applications = connection.execute(
            query, parameters
        ).fetchall()

        total = connection.execute(
            "SELECT COUNT(*) FROM applications"
        ).fetchone()[0]

        counts = dict(connection.execute(
            "SELECT status, COUNT(*) FROM applications "
            "GROUP BY status"
        ).fetchall())

    return render_template(
        "index.html",
        applications=applications,
        search=search,
        total=total,
        counts=counts,
        selected_status=selected_status,
        statuses=STATUSES
    )




@app.route("/add", methods=["POST"])
def add():
    company = request.form.get("company", "").strip()
    role = request.form.get("role", "").strip()
    application_date = request.form.get("application_date", "")
    status = request.form.get("status", "")

    if not company or not role or status not in STATUSES:
        return "Please enter a company, role, and valid status.", 400

    try:
        datetime.strptime(application_date, "%Y-%m-%d")
    except ValueError:
        return "Please enter a valid application date.", 400

    with get_connection() as connection:
        connection.execute("""
            INSERT INTO applications
                (company, role, application_date, status)
            VALUES (?, ?, ?, ?)
        """, (company, role, application_date, status))

    return redirect(url_for("home"))


@app.route("/delete/<int:application_id>", methods=["POST"])
def delete(application_id):
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM applications WHERE id = ?",
            (application_id,)
        )

    return redirect(url_for("home"))
@app.route("/update/<int:application_id>", methods=["POST"])
def update_status(application_id):
    status = request.form.get("status", "")

    if status not in STATUSES:
        return "Please choose a valid status.", 400

    with get_connection() as connection:
        connection.execute(
            "UPDATE applications SET status = ? WHERE id = ?",
            (status, application_id)
        )

    return redirect(url_for("home"))
@app.route("/edit/<int:application_id>", methods=["GET", "POST"])
def edit(application_id):
    with get_connection() as connection:
        application = connection.execute(
            "SELECT * FROM applications WHERE id = ?",
            (application_id,)
        ).fetchone()

    if application is None:
        return "Application not found.", 404

    if request.method == "POST":
        company = request.form.get("company", "").strip()
        role = request.form.get("role", "").strip()
        application_date = request.form.get("application_date", "")

        if not company or not role:
            return "Please enter a company and job role.", 400

        try:
            datetime.strptime(application_date, "%Y-%m-%d")
        except ValueError:
            return "Please enter a valid date.", 400

        with get_connection() as connection:
            connection.execute(
                "UPDATE applications "
                "SET company = ?, role = ?, application_date = ? "
                "WHERE id = ?",
                (company, role, application_date, application_id)
            )

        return redirect(url_for("home"))

    return render_template("edit.html", application=application)




if __name__ == "__main__":
    app.run(debug=True)