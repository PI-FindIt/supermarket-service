import json
import random


def get_price() -> float:
    mean_value = random.random() * 5 + 1
    return round(random.gauss(mean_value, mean_value / 4), 2)


def get_random_supermarkets() -> list[int]:
    return random.sample(supermarket_ids, random.randint(1, 8))


data = json.load(open("products.json"))
eans = [p["ean"] for p in data["data"]["products"]]
supermarket_ids = range(1, 9)

# key: ean, value: list of tuples (supermarket_id, price)
output: dict[str, list[tuple[int, float]]] = dict()


for ean in eans:
    supermarkets = get_random_supermarkets()
    prices = [(supermarket_id, get_price()) for supermarket_id in supermarkets]
    output[ean] = prices

insert_statements = [
    f"INSERT INTO supermarket_price (supermarket_id, product_ean, price) VALUES ({supermarket_id}, '{ean}', {price});"
    for ean, prices in output.items()
    for supermarket_id, price in prices
]

with open("../migrations/prices.sql", "w") as f:
    for statement in insert_statements:
        f.write(statement + "\n")
