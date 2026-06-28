from dao.base_dao import BaseDAO
from models.order import Order

class OrderDAO(BaseDAO):
    def __init__(self, file_path="data/orders.json"):
        super().__init__(file_path)

    def find_all(self):
        data = self._read_all()
        return [Order.from_dict(item) for item in data]

    def find_by_id(self, order_id):
        orders = self.find_all()
        for order in orders:
            if order.id == order_id:
                return order
        return None

    def find_by_username(self, username):
        orders = self.find_all()
        return [o for o in orders if o.user_username == username]

    def insert(self, order):
        orders = self.find_all()
        max_id = max([o.id for o in orders if o.id is not None], default=0)
        order.id = max_id + 1
        
        orders.append(order)
        self._write_all([o.to_dict() for o in orders])
        return order

    def update(self, order):
        orders = self.find_all()
        for idx, o in enumerate(orders):
            if o.id == order.id:
                orders[idx] = order
                self._write_all([x.to_dict() for x in orders])
                return True
        return False
