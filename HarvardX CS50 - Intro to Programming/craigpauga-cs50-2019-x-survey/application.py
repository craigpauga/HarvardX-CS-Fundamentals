import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Initialize people
people = []


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():

    email = request.form.get("email")
    password = request.form.get("password")
    magic = request.form.get("gridRadios")
    house = request.form.get("house")

    if not email:
        return render_template("error.html", message="You must input an email")
    elif not password:
        return render_template("error.html", message="You must input a password")
    file = open("survey.csv", "a")
    writer = csv.writer(file)
    writer.writerow((email, password))
    file.close()
    return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    file = open("survey.csv", "r")
    reader = csv.reader(file)
    people = list(reader)
    file.close()
    return render_template("sheet.html", people=people)
