from io import BytesIO

import pandas as pd
from flask import Flask, render_template, request, send_file
from utils.doc2xlsx import gen_reviews
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route('/health', methods=["GET", "POST"])
def home():
    return 200

@app.route("/reviews", methods=["GET", "POST"])
def reviews():
    res = gen_reviews(request.form['reviews'])
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    res.to_excel(writer, sheet_name='Sheet1', index = False)
    writer.save()
    output.seek(0)
    return send_file(output, download_name='reviews.xlsx', as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
