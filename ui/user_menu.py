from ui.console_utils import print_header, print_subheader, print_menu_options, read_input, read_int, print_table
from service.album_service import AlbumService
from service.order_service import OrderService

class UserMenu:
    def __init__(self, user, album_service, order_service):
        self.user = user
        self.album_service = album_service
        self.order_service = order_service
        self.cart = {}  # album_id (int) -> quantity (int)

    def run(self):
        while True:
            print_header(f"Customer Menu - Welcome, {self.user.name} ({self.user.username})")
            options = {
                "1": "Browse All Albums",
                "2": "Search Albums",
                "3": "View Shopping Cart",
                "4": "Order History",
                "5": "Logout"
            }
            print_menu_options(options)
            choice = read_input("Select Menu")

            if choice == "1":
                self.browse_albums()
            elif choice == "2":
                self.search_albums()
            elif choice == "3":
                self.view_cart()
            elif choice == "4":
                self.view_order_history()
            elif choice == "5":
                print("Logging out...")
                break
            else:
                print(" [!] Invalid option. Try again.")

    def browse_albums(self):
        print_subheader("All Available Albums")
        albums = self.album_service.get_all_albums()
        headers = ["ID", "Title", "Artist", "Genre", "Price", "Stock"]
        rows = []
        for a in albums:
            rows.append([a.id, a.title, a.artist, a.genre, f"${a.price:,}", a.stock])
        print_table(headers, rows)

        ans = read_input("Add an album to cart? (y/n)", required=False).lower()
        if ans == 'y':
            self.add_to_cart()

    def search_albums(self):
        print_subheader("Search Albums")
        print(" [1] By Title")
        print(" [2] By Artist")
        print(" [3] By Genre")
        choice = read_input("Search By")
        
        search_type = "title"
        if choice == "2":
            search_type = "artist"
        elif choice == "3":
            search_type = "genre"
        elif choice != "1":
            print(" [!] Defaulting to search by Title.")
            
        keyword = read_input("Enter keyword")
        albums = self.album_service.search_albums(keyword, search_type)
        
        headers = ["ID", "Title", "Artist", "Genre", "Price", "Stock"]
        rows = []
        for a in albums:
            rows.append([a.id, a.title, a.artist, a.genre, f"${a.price:,}", a.stock])
        print_table(headers, rows)

        if albums:
            ans = read_input("Add search result to cart? (y/n)", required=False).lower()
            if ans == 'y':
                self.add_to_cart()

    def add_to_cart(self):
        album_id = read_int("Enter Album ID to add")
        album = self.album_service.get_album_by_id(album_id)
        if not album:
            print(" [!] Album not found.")
            return
            
        if album.stock <= 0:
            print(" [!] This album is out of stock.")
            return

        qty = read_int(f"Enter quantity (Available: {album.stock})")
        if qty <= 0:
            print(" [!] Quantity must be greater than 0.")
            return
            
        current_qty = self.cart.get(album_id, 0)
        if current_qty + qty > album.stock:
            print(f" [!] Cannot add {qty}. Total in cart ({current_qty + qty}) exceeds available stock ({album.stock}).")
            return

        self.cart[album_id] = current_qty + qty
        print(f" [✓] Added '{album.title}' (x{qty}) to your cart.")

    def view_cart(self):
        while True:
            print_subheader("Your Shopping Cart")
            if not self.cart:
                print(" Your cart is currently empty.")
                print("─" * 60)
                print(" [1] Go Back")
                choice = read_input("Select")
                if choice == "1" or not choice:
                    break
                continue
                
            headers = ["Album ID", "Title", "Artist", "Price", "Qty", "Subtotal"]
            rows = []
            total = 0
            for album_id, qty in list(self.cart.items()):
                album = self.album_service.get_album_by_id(album_id)
                if not album:
                    del self.cart[album_id]
                    continue
                subtotal = album.price * qty
                total += subtotal
                rows.append([album.id, album.title, album.artist, f"${album.price:,}", qty, f"${subtotal:,}"])
                
            print_table(headers, rows)
            print(f" Total Price: ${total:,}")
            print("─" * 60)
            
            print(" [1] Checkout (Purchase)")
            print(" [2] Modify Item Quantity")
            print(" [3] Delete Item")
            print(" [4] Empty Cart")
            print(" [5] Go Back")
            choice = read_input("Select Option")
            
            if choice == "1":
                self.checkout()
                break
            elif choice == "2":
                self.modify_cart_qty()
            elif choice == "3":
                self.delete_cart_item()
            elif choice == "4":
                self.cart.clear()
                print(" [✓] Cart emptied.")
            elif choice == "5":
                break
            else:
                print(" [!] Invalid option.")

    def modify_cart_qty(self):
        album_id = read_int("Enter Album ID to modify")
        if album_id not in self.cart:
            print(" [!] Album not in cart.")
            return
            
        album = self.album_service.get_album_by_id(album_id)
        if not album:
            del self.cart[album_id]
            return
            
        qty = read_int(f"Enter new quantity (Available stock: {album.stock})")
        if qty <= 0:
            del self.cart[album_id]
            print(" [✓] Item removed from cart.")
        elif qty > album.stock:
            print(f" [!] Cannot update. Requested quantity {qty} exceeds available stock {album.stock}.")
        else:
            self.cart[album_id] = qty
            print(" [✓] Quantity updated.")

    def delete_cart_item(self):
        album_id = read_int("Enter Album ID to delete")
        if album_id in self.cart:
            del self.cart[album_id]
            print(" [✓] Item removed from cart.")
        else:
            print(" [!] Album not in cart.")

    def checkout(self):
        print_subheader("Checkout Confirmation")
        confirm = read_input("Process purchase? (y/n)").lower()
        if confirm == 'y':
            try:
                order = self.order_service.checkout(self.user.username, self.cart)
                print(f" [✓] Purchase completed successfully!")
                print(f"     Order ID: {order.id}")
                print(f"     Total Paid: ${order.total_price:,}")
                self.cart.clear()
            except ValueError as e:
                print(f" [!] Checkout failed: {e}")

    def view_order_history(self):
        print_subheader("Your Order History")
        orders = self.order_service.get_user_orders(self.user.username)
        if not orders:
            print(" No order history found.")
            return

        for order in orders:
            print(f"\nOrder ID: {order.id} | Date: {order.order_date} | Status: [{order.status}]")
            headers = ["Album ID", "Album Title", "Price", "Qty", "Subtotal"]
            rows = []
            for item in order.items:
                rows.append([item.album_id, item.album_title, f"${item.price:,}", item.quantity, f"${(item.price * item.quantity):,}"])
            print_table(headers, rows)
            print(f"Total Order Price: ${order.total_price:,}")
            print("-" * 50)
