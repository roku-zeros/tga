from pyqiwip2p import QiwiP2P
from coinbase_commerce.client import Client


QIWI_PRIV_KEY = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6IjZyMXcyZC0wMCIsInVzZXJfaWQiOiI3OTc3MTI2NTAzOSIsInNlY3JldCI6ImRhNDE3NzUyNjI5MzMwZTU5ZDY0MmRhZDcwNzc4OTJlZDNkYjU4ZWQ4YTE0MTAyZmY3ZWI2YzY1NjA1NzQ1YTcifX0="
p2p = QiwiP2P(auth_key=QIWI_PRIV_KEY)
CB_API_KEY = "a2b45d1c-5cb8-4342-a287-ee7022fbef99"
client = Client(api_key=CB_API_KEY)


def qiwi_check(product):
    bill = p2p.bill(amount=product.price, lifetime=60, comment="_")
    return bill.bill_id, bill.pay_url


def crypto_check(product):
    charge_info = {
        "name": "Test",
        "description": "_",
        "local_price": {
            "amount": str(product.price),
            "currency": "RUB"
        },
        "pricing_type": "fixed_price"
    }
    charge = client.charge.create(**charge_info)
    return charge.id, charge.hosted_url
