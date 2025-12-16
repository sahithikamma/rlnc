from flask import Flask, render_template, request, redirect, url_for, session
from db import admin_col, emp_col, salary_col
from bson import ObjectId   # 🔥 IMPORTANT

app = Flask(__name__)
app.secret_key = "rlnc_secret_key"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


# ---------------- LOGIN ROUTE ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role")
        username = request.form.get("username")
        password = request.form.get("password")

        # -------- ADMIN LOGIN --------
        if role == "admin":
            admin = admin_col.find_one({
                "username": username,
                "password": password
            })

            if admin:
                session.clear()
                session["admin"] = username

                employees = list(emp_col.find())
                print("EMPLOYEES DATA:", employees)

                return render_template(
                    "admin_dashboard.html",
                    employees=employees
                )

            return render_template(
                "login.html",
                error="Invalid Admin Credentials"
            )

        # -------- EMPLOYEE LOGIN --------
        elif role == "employee":
            emp = emp_col.find_one({
                "username": username,
                "password": password
            })

            if emp:
                session.clear()
                session["employee"] = str(emp["_id"])   # store as string

                # 🔥 fetch salary using ObjectId
                emp_id = ObjectId(session["employee"])
                salary = list(salary_col.find({"emp_id": emp_id}))

                print("SALARY DATA:", salary)

                return render_template(
                    "employee_dashboard.html",
                    salary=salary
                )

            return render_template(
                "login.html",
                error="Invalid Employee Credentials"
            )

        # -------- ROLE NOT SELECTED --------
        return render_template(
            "login.html",
            error="Please select a role"
        )

    # -------- GET REQUEST --------
    return render_template("login.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
