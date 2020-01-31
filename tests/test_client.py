from unittest import TestCase

import pytest
from alma import Client


class ClientTest(TestCase):
    def test_client_raises_with_no_api_key_arguments(self):
        with pytest.raises(
            TypeError, match=r"__init__\(\) missing 1 required positional argument: 'api_key'"
        ):
            Client()

    def test_client_raises_with_empty_api_key_value(self):
        with pytest.raises(ValueError, match=r"An API key is required"):
            Client(api_key="")

    def test_client_raises_with_empty_api_key_set_to_None(self):
        with pytest.raises(ValueError, match=r"An API key is required"):
            Client(api_key=None)
