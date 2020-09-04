import inspect

from alma.async_client import AsyncClient


def test_async_client():
    client = AsyncClient("sk_live_3geNR4OVI0gQGCAKgcYqQs2I")
    inspect.iscoroutinefunction(client.payments.fetch_all)
