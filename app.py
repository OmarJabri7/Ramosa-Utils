from io import BytesIO
import asyncio
import pandas as pd
from flask import Flask, render_template, request, send_file
from utils.doc2xlsx import gen_reviews
from utils.ali_express import ali_express_scraper
from utils.amazon_scrape import amazon_scraper
import logging
from threading import Thread

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
thread_q = []


def store_data(f):
    def wrapper(*args):
        thread_q.append(f(*args))
    return wrapper


@store_data
def get_products(message):
    app.logger.info("Started Thread")
    products = message.lower().replace("find", '')
    products = products.split(",")
    idx = "hot products"
    for product in products:
        amazon_data = amazon_scraper(idx + product)
        prods = []
        for hot_product in amazon_data["products"]:
            prods.extend(ali_express_scraper(hot_product["title"]))
    df = pd.DataFrame.from_dict(prods)
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    output.seek(0)
    app.logger.info("Finished Thread...")
    return df


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
    res.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    output.seek(0)
    return send_file(output, attachment_filename='reviews.xlsx', as_attachment=True)


@app.route("/products", methods=["GET", "POST"])
def products():
    app.logger.info("Extracting products...")
    message = request.form['products']
    product_thread = Thread(target=get_products, daemon=True, args=(message,))
    product_thread.start()
    product_thread.join()
    df = thread_q[0]
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    output.seek(0)
    return send_file(output, attachment_filename='products.xlsx', as_attachment=True)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
