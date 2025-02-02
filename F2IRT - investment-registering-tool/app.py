from flask import Flask, render_template, request, redirect
from utils import create_database, register_operation, get_paginated_operations, delete_record

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    asset_type = request.form['asset_type']
    operation_type = request.form['operation_type']
    ticker = request.form["ticker"]
    date = request.form["date"]
    unit_price = float(request.form["unit_price"])
    quantity = int(request.form["quantity"])
    liquidationFee = float(request.form["liquidationFee"])
    emolumentsFee = float(request.form["emolumentsFee"])
    taxes = float(request.form["taxes"])
    operationalFee = float(request.form["operationalFee"])
    otherFees = float(request.form["otherFees"])
    irrf = float(request.form["irrf"])

    register_operation(asset_type, operation_type, ticker, date, unit_price, quantity, liquidationFee, emolumentsFee, taxes, operationalFee, otherFees, irrf)
    return '''
    <script>
        alert("The operation has been successfully submitted");
        window.location.href = "/";
    </script>
    '''

@app.route("/records", methods=["GET"])
def records():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    operations, total_records = get_paginated_operations(page, per_page)
    total_pages = (total_records // per_page) + (1 if total_records % per_page > 0 else 0)
    return render_template("records.html", operations=operations, page=page, per_page=per_page, total_pages=total_pages)



if __name__ == "__main__":
    create_database()
    app.run(debug=True)
