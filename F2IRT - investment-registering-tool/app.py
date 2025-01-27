from flask import Flask, render_template, request, redirect
from utils import create_database, register_operation, get_operations

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    ticker = request.form["ticker"]
    date = request.form["date"]
    unit_price = float(request.form["unit_price"])
    quantity = int(request.form["quantity"])
    fees = float(request.form["fees"])
    taxes = float(request.form["taxes"])

    register_operation(ticker, date, unit_price, quantity, fees, taxes)
    return redirect("/records")

@app.route("/records")
def records():
    operations = get_operations()
    return render_template("records.html", operations=operations)

if __name__ == "__main__":
    create_database()
    app.run(debug=True)
