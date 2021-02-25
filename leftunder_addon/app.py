from flask import Flask
import json, requests

app = Flask(__name__)
config = json.loads(open("/data/options.json").read())
grocy_api_endpoint = config["grocy_endpoint"] + "api/"
grocy_headers = {"GROCY-API-KEY": config["grocy_api_key"]}


def name_lookup(product_response, product_id):
    for product in product_response:
        if product["id"] == product_id:
            if product["userfields"] and "shortName" in product["userfields"]:
                return product["userfields"]["shortName"]
            return product["name"]


def ready_to_eat_lookup(product_response, product_id):
    for product in product_response:
        if product["id"] == product_id:
            if product["userfields"] and "readyToEat" in product["userfields"]:
                return product["userfields"]["readyToEat"] == "1"
            return False


@app.route("/")
def send_data():
    response = {}

    products = requests.get(grocy_api_endpoint + "objects/products", headers=grocy_headers).json()
    stock = requests.get(grocy_api_endpoint + "stock", headers=grocy_headers).json()
    volatile = requests.get(grocy_api_endpoint + "stock/volatile", headers=grocy_headers).json()

    response["overdue"] = []
    for due_product in volatile["due_products"] + volatile["expired_products"]:
        response["overdue"].append(name_lookup(products, due_product["product"]["id"]))

    response["missing"] = []
    for missing_product in volatile["missing_products"]:
        response["missing"].append(missing_product["product"]["name"])

    response["ready_to_eat"] = []
    for stock_item in stock:
        if stock_item["amount"] == 0:
            continue
        if ready_to_eat_lookup(products, stock_item["product"]["id"]):
            response["ready_to_eat"].append(stock_item["product"]["name"])
    return response


app.run(port=5338, host="0.0.0.0")
