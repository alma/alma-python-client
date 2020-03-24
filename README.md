# alma-python-client

[![Travis Build Status](https://travis-ci.org/alma/alma-python-client.svg?branch=master)](https://travis-ci.org/alma/alma-python-client)

Python API Client for the Alma API


## Demo


```python
from alma import Client

alma_client = Client(api_key="sk_test..")
payments = alma_client.payments.fetch_all()

for p in payments:
    print(f"{p.id}: Paiement en {p.installments_count)} fois")


payment_data = {
    "purchase_amount": 10000,
    "return_url": "http://merchant.com/payment-success",
    "shipping_address": {
        "first_name": "Martin",
        "last_name": "Dupond",
        "line1": "1 rue de Rivoli",
        "postal_code": "75004",
        "city": "Paris"
    }
}

eligibility = alma_client.payments.eligibility(payment_data)
if eligibility.eligible:
    alma_client.payments.create(payment_data)
```
