from coinbase_commerce.client import Client
import os

API_KEY = "a2b45d1c-5cb8-4342-a287-ee7022fbef99"

# initialize client
client = Client(api_key=API_KEY)

# charge info
charge_info = {
    "name": "The Sovereign Individual",
    "description": "Mastering the Transition to the Information Age",
    "local_price": {
        "amount": "100.00",
        "currency": "USD"
    },
    "pricing_type": "fixed_price"

}
charge = client.charge.create(**charge_info)
saved_charge_id = charge.id

retrieved_charge = client.charge.retrieve(entity_id=saved_charge_id)
print("retrieved charge {!r}".format(retrieved_charge))
print('\n' * 20)
# Get status
print(retrieved_charge['timeline'][-1]['status'])
id = '26b7855b-bcaf-47fa-8c1f-2531b577c839'
retrieved_charge = client.charge.retrieve(entity_id=id)
print(retrieved_charge['timeline'][-1]['status'])

print(os.getcwd())