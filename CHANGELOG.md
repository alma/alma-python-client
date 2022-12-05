# Changelog

3.0.1 (2022-12-05)
------------------

- Configure credentials later in the flow.


3.0.0 (2022-06-29)
------------------

**Breaking change**

- Move the code from the `alma` namespace into the `alma_client` namespace.
- Remove support for Python 3.6 and Python 3.7


2.0.2 (2022-06-22)
------------------

- Fix `potential-fraud` method URLs (#27)


2.0.1 (2022-06-17)
------------------

- Adds `include_child_accounts` and `custom_fields` params to the DataExport creation endpoint


2.0.0 (2021-08-12)
------------------

**Breaking changes**

- Move from requests to HTTPX
- Handle both sync and async python clients
- Remove support for Python 3.5
- Add support for Python 3.9


1.2.0 (2020-09-01)
------------------

- Add support for different authentication methods
- Add Black & isort checks on pull requests


1.1.0 (2020-03-25)
------------------

- Add support for Python 3.5+


1.0.1 (2020-03-24)
------------------

- Automatically detects the API mode from the api_key.


1.0.0 (2020-03-24)
------------------

- Create a Python client for Alma
- Handle Order entity for Payment
- Handle the refund endpoint
- Handle pagination for orders
- Handle the send-sms API for payments.
