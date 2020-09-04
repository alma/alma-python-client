# alma-python-client

[![Travis Build Status](https://travis-ci.org/alma/alma-python-client.svg?branch=main)](https://travis-ci.org/alma/alma-python-client) [![PyPI](https://img.shields.io/pypi/v/alma-client.svg)](https://pypi.python.org/pypi/alma-client)

Python API Client for the Alma API

## Install

```bash
pip install alma-client
```

## Demo

We support both a sync and async client.

### Synchronous client


```python
from alma import Client

alma_client = Client.with_api_key("sk_test..")
payments = alma_client.payments.fetch_all()

for p in payments:
    print(f"{p.id}: Paiement en {len(p.payment_plan)} fois")


payment_data = {
    "payment": {
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
}

eligibility = alma_client.payments.eligibility(payment_data)
if eligibility.eligible:
    payment = alma_client.payments.create(payment_data)

print(payment.raw_data)
```


### Asynchronous client


```python
from alma import AsyncClient

alma_client = AsyncClient.with_api_key("sk_test..")
payments = await alma_client.payments.fetch_all()

for p in payments:
    print(f"{p.id}: Paiement en {len(p.payment_plan)} fois")


payment_data = {
    "payment": {
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
}

eligibility = await alma_client.payments.eligibility(payment_data)
if eligibility.eligible:
    payment = await alma_client.payments.create(payment_data)

print(payment.raw_data)
```
