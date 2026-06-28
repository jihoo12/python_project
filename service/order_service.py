from datetime import datetime
from dao.order_dao import OrderDAO
from dao.album_dao import AlbumDAO
from models.order import Order, OrderItem

class OrderService:
    def __init__(self, order_dao=None, album_dao=None):
        self.order_dao = order_dao or OrderDAO()
        self.album_dao = album_dao or AlbumDAO()

    def checkout(self, username, cart):
        """
        cart is a dict of {album_id (int): quantity (int)}
        """
        if not cart:
            raise ValueError("Your cart is empty.")

        order_items = []
        total_price = 0
        albums_to_update = []

        # 1. Verification phase
        for album_id, qty in cart.items():
            if qty <= 0:
                continue
            
            album = self.album_dao.find_by_id(album_id)
            if not album:
                raise ValueError(f"Album with ID {album_id} does not exist.")
            
            if album.stock < qty:
                raise ValueError(f"Insufficient stock for '{album.title}'. Available stock: {album.stock}, requested: {qty}")
            
            # Record what needs to be updated
            album.stock -= qty
            albums_to_update.append(album)
            
            # Create OrderItem
            item_price = album.price * qty
            total_price += item_price
            order_items.append(OrderItem(
                album_id=album.id,
                album_title=album.title,
                quantity=qty,
                price=album.price
            ))

        if not order_items:
            raise ValueError("No valid items in the cart to purchase.")

        # 2. Execution phase
        for album in albums_to_update:
            self.album_dao.update(album)

        order_date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        order = Order(
            user_username=username,
            items=order_items,
            total_price=total_price,
            status="PREPARING",
            order_date=order_date_str
        )
        
        return self.order_dao.insert(order)

    def get_user_orders(self, username):
        return self.order_dao.find_by_username(username)

    def get_all_orders(self):
        return self.order_dao.find_all()

    def update_order_status(self, order_id, new_status):
        order = self.order_dao.find_by_id(order_id)
        if not order:
            raise ValueError(f"Order with ID {order_id} not found.")
        
        valid_statuses = ["PREPARING", "SHIPPED", "DELIVERED", "CANCELLED"]
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")

        # If cancelled, restore stock
        if new_status == "CANCELLED" and order.status != "CANCELLED":
            for item in order.items:
                album = self.album_dao.find_by_id(item.album_id)
                if album:
                    album.stock += item.quantity
                    self.album_dao.update(album)

        order.status = new_status
        self.order_dao.update(order)
        return order
