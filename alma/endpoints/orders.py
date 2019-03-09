from . import Base
from ..entities import Order


class Orders(Base):
    ORDERS_PATH = "/v1/orders"

    def update(self, order_id, data):
        response = self.request(f"{self.ORDERS_PATH}/{order_id}").set_body(data).put()
        return Order(response.json)
