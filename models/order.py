class OrderItem:
    def __init__(self, album_id, album_title, quantity, price):
        self.album_id = album_id
        self.album_title = album_title
        self.quantity = quantity
        self.price = price

    def to_dict(self):
        return {
            "album_id": self.album_id,
            "album_title": self.album_title,
            "quantity": self.quantity,
            "price": self.price
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            album_id=data.get("album_id"),
            album_title=data.get("album_title"),
            quantity=data.get("quantity"),
            price=data.get("price")
        )


class Order:
    def __init__(self, user_username, items, total_price, status="PREPARING", order_date=None, id=None):
        self.id = id
        self.user_username = user_username
        self.items = items  # list of OrderItem
        self.total_price = total_price
        self.status = status  # PREPARING, SHIPPED, DELIVERED, CANCELLED
        self.order_date = order_date

    def to_dict(self):
        return {
            "id": self.id,
            "user_username": self.user_username,
            "items": [item.to_dict() for item in self.items],
            "total_price": self.total_price,
            "status": self.status,
            "order_date": self.order_date
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            user_username=data.get("user_username"),
            items=[OrderItem.from_dict(item) for item in data.get("items", [])],
            total_price=data.get("total_price"),
            status=data.get("status", "PREPARING"),
            order_date=data.get("order_date")
        )
