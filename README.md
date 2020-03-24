# alma-python-client

[![Travis Build Status](https://travis-ci.org/alma/alma-python-client.svg?branch=master)](https://travis-ci.org/alma/alma-python-client)

Python API Client for the Alma API


## Demo


```python
from alma import Client

alma_client = Client(api_key="sk_test..")
payments = alma_client.payments.fetch_all()

for p in payments:
	print(f"{p.id}: Payment en {len(p.payment_plan)} fois")
```
