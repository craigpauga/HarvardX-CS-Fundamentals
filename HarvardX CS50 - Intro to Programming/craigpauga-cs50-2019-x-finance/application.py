import os
import datetime
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():

    # User reached route via GET (as by submitting a form via POST)
    if request.method == "GET":
        user_id = session["user_id"]

        # Query database for username
        rows = db.execute("SELECT * FROM portfolio WHERE user_id = :user_id", user_id=session["user_id"])

        # Query database for cash
        cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])[0]['cash']

        info = []
        holdings = 0
        if rows:
            for row in rows:

                # Lookup info with API
                stock_info = lookup(row['symbol'])

                # Break down stock info
                name = stock_info['name']
                symbol = stock_info['symbol']
                price = stock_info['price']
                quantity = row['quantity']
                value = float(price)*float(quantity)
                holdings += value
                info.append([name, symbol, usd(price), quantity, usd(value)])
            return render_template("index.html", info=info, cash=usd(cash), holdings=usd(holdings))
        else:
            return render_template("index.html", info=info, cash=usd(cash), holdings=usd(holdings))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via GET (as by submitting a form via POST)
    if request.method == "GET":
        return render_template("buy.html")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get the symbol with the API
        if not request.form.get("symbol"):
            return apology("No symbol", 400)
        else:
            # Get the symbol info
            value = lookup(request.form.get("symbol"))

            # Check if symbol exists
            if not value:
                return apology("Symbol doesn't exist", 400)

            # Get the amount of shares
            quantity = request.form.get("shares")
            try:
                int(quantity)
            except ValueError:
                return apology("That isnt an integer",400)

            # Check if it is positive

            if int(quantity) < 0:
                return apology("That is negeative",400)
            # Get info from dictionary
            stockName = value['name']
            price = value['price']
            symbol = value['symbol']
            total = float(price) * float(quantity)

            # Query database for username
            rows = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

            cash = float(rows[0]['cash'])

            # Check if total is more than cash left
            if total > cash:
                return apology("You can't afford that", 403)
            else:

                # Add new transaction to the database
                rows = db.execute("INSERT INTO transactions (user_id,symbol,price,quantity,total,date) VALUES (:user_id,:symbol,:price,:quantity,:total,:date)",
                    user_id=session["user_id"], symbol=symbol, price=price, quantity=quantity, total=-total, date=datetime.datetime.now())

                # Update new cash total for user
                db.execute("UPDATE users SET cash=:new_total WHERE id=:id", new_total=cash-total, id=session["user_id"])

                # Update new amount of stocks owned
                rows = db.execute("SELECT * FROM portfolio WHERE user_id=:user_id AND symbol=:symbol",
                    user_id=session["user_id"], symbol=symbol)

                if not rows:

                    new_quantity = quantity
                    db.execute("INSERT INTO portfolio (user_id,symbol,quantity) VALUES(:user_id,:symbol,:quantity)",
                        user_id=session["user_id"], symbol=symbol, quantity=new_quantity)
                else:
                    new_quantity = int(rows[0]['quantity']) + int(quantity)
                    db.execute("UPDATE portfolio SET quantity=:new_quantity WHERE user_id=:user_id AND symbol=:symbol",
                        new_quantity=new_quantity, user_id=session["user_id"], symbol=symbol)

            return redirect("/")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    # User reached route via GET (as by submitting a form via POST)
    if request.method == "GET":

        # Ensure username was inputted
        if not request.form.get("check"):
            return apology("You didn't put a name in")

        # Check if name exists
        rows = db.execute("SELECT username FROM users WHERE username=:username", username=request.form.get("check"))

        if not row:
            return render("index.html")
        else:
            return render("index.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Update new amount of stocks owned
    rows = db.execute("SELECT * FROM transactions WHERE user_id=:user_id",
                user_id=session["user_id"])

    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():

    # User reached route via GET (as by submitting a form via POST)
    if request.method == "GET":

        # Ensure username was inputted
        if not request.form.get("symbol"):
            return render_template("quote.html")
        else:
            value = lookup(request.form.get("symbol"))
            return render_template("quoted.html", value=value)

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was inputted
        if not request.form.get("symbol"):
            return apology("Symbol is blank", 400)
        else:
            value = lookup(request.form.get("symbol"))

            if not value:
                return apology("Symbol doesn't exist", 400)

            stockName = value['name']
            price = float(value['price'])
            symbol = value['symbol']

            return render_template("quoted.html", price=usd(price))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was inputted
        if not request.form.get("username"):
            return apology("need username to register", 400)

        # Ensure password was inputted
        elif not request.form.get("password"):
            return apology("need username to register", 400)

        # Ensure password was inputted
        elif not request.form.get("confirmation"):
            return apology("need to confirm password", 400)

        # Ensure password was inputted
        elif not (request.form.get("confirmation") == request.form.get("password")):
            return apology("passwords do not match", 400)

        password_hash = generate_password_hash(request.form.get("password"))

        # Check if user is already registered
        rows = db.execute("SELECT username FROM users WHERE username=:username", username=request.form.get("username"))

        if not rows:

            # Add new user to the database
            db.execute("INSERT INTO users (username,hash) VALUES (:username,:hash)",
                username=request.form.get("username"), hash=password_hash)
        else:
            return apology("That username is already taken", 400)

        return render_template("login.html")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via GET (as by submitting a form via POST)
    if request.method == "GET":

        # Get the symbols of
        rows = db.execute("SELECT * FROM portfolio WHERE user_id=:user_id", user_id=session["user_id"])

        return render_template("sell.html", rows=rows)

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was inputted
        if not request.form.get("symbol"):
            return apology("need to select symbol to sell", 400)

        # Ensure password was inputted
        elif not request.form.get("shares"):
            return apology("need number of shares to sell", 400)

        # Update new amount of stocks owned
        rows = db.execute("SELECT * FROM portfolio WHERE user_id=:user_id", user_id=session["user_id"])

        for row in rows:
            if row['symbol'] == request.form.get("symbol"):

                # Get info from row
                symbol = row['symbol']
                info = lookup(symbol)
                price = info['price']

                # get quantity for that symbol
                quantity = row['quantity']

                # Calculate new quantity after selling
                new_quantity = int(quantity) - int(request.form.get("shares"))

                # Calculate total
                total = float(price) * float(quantity)

                # Check if purchase is greater than owned shares
                if int(quantity) < int(request.form.get("shares")):
                    return apology("You don't have that many stocks", 400)

                # Add new transaction to the database
                db.execute("INSERT INTO transactions (user_id,symbol,price,quantity,total,date) VALUES (:user_id,:symbol,:price,:quantity,:total,:date)",
                    user_id=session["user_id"], symbol=symbol, price=price, quantity=int(request.form.get("shares")), total=total, date=datetime.datetime.now())

                # Update portfolio with amount of stocks
                db.execute("UPDATE portfolio SET quantity=:new_quantity WHERE user_id=:user_id AND symbol=:symbol",
                    new_quantity=new_quantity, user_id=session["user_id"], symbol=symbol)

                # Get amount of cash user has
                cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])

                # New total
                cash = float(cash[0]['cash']) + total

                # Update amount of money they hav
                db.execute("UPDATE users SET cash=:cash WHERE id=:id", cash=cash, id=session["user_id"])
            return redirect("/")


@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():

    # User reached route via GET (as by submitting a form via POST)
    if request.method == "GET":
        return render_template("deposit.html")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure deposit in submitted
        if not request.form.get("deposit"):
            return apology("need to select amount of cash to deposit", 403)

        deposit = float(request.form.get("deposit"))

        # Get amount of cash user has
        cash = float(db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])[0]['cash'])

        # Calculate new cash amount
        cash = cash + deposit

        # Update amount of money they hav
        db.execute("UPDATE users SET cash=:cash WHERE id=:id", cash=cash, id=session["user_id"])

        return render_template("deposit.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
