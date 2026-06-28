from ui.console_utils import print_header, print_subheader, print_menu_options, read_input, read_int, print_table
from service.album_service import AlbumService
from service.order_service import OrderService
from service.user_service import UserService

class AdminMenu:
    def __init__(self, user, album_service, order_service, user_service):
        self.user = user
        self.album_service = album_service
        self.order_service = order_service
        self.user_service = user_service

    def run(self):
        while True:
            print_header(f"Admin Menu - Logged in as: {self.user.name}")
            options = {
                "1": "Manage Album Catalog",
                "2": "Manage Orders",
                "3": "View User List",
                "4": "Logout"
            }
            print_menu_options(options)
            choice = read_input("Select Menu")

            if choice == "1":
                self.manage_albums()
            elif choice == "2":
                self.manage_orders()
            elif choice == "3":
                self.view_users()
            elif choice == "4":
                print("Logging out admin...")
                break
            else:
                print(" [!] Invalid option. Try again.")

    def manage_albums(self):
        while True:
            print_subheader("Album Catalog Management")
            options = {
                "1": "View All Albums",
                "2": "Add New Album",
                "3": "Update Album Info",
                "4": "Delete Album",
                "5": "Back"
            }
            print_menu_options(options)
            choice = read_input("Select Option")

            if choice == "1":
                self.view_all_albums()
            elif choice == "2":
                self.add_album()
            elif choice == "3":
                self.update_album()
            elif choice == "4":
                self.delete_album()
            elif choice == "5":
                break
            else:
                print(" [!] Invalid option.")

    def view_all_albums(self):
        print_subheader("All Albums in Catalog")
        albums = self.album_service.get_all_albums()
        headers = ["ID", "Title", "Artist", "Genre", "Price", "Stock"]
        rows = []
        for a in albums:
            rows.append([a.id, a.title, a.artist, a.genre, f"${a.price:,}", a.stock])
        print_table(headers, rows)

    def add_album(self):
        print_subheader("Add New Album")
        title = read_input("Album Title")
        artist = read_input("Artist")
        genre = read_input("Genre")
        price = read_int("Price")
        stock = read_int("Stock")

        try:
            album = self.album_service.add_album(title, artist, genre, price, stock)
            print(f" [✓] Album added successfully with ID: {album.id}")
        except ValueError as e:
            print(f" [!] Error: {e}")

    def update_album(self):
        print_subheader("Update Album Info")
        album_id = read_int("Enter Album ID to update")
        album = self.album_service.get_album_by_id(album_id)
        if not album:
            print(" [!] Album not found.")
            return

        print(f" Modifying: ID {album.id} | {album.title} by {album.artist}")
        print(" (Press Enter to keep the current value)")
        
        title = read_input(f"New Title ({album.title})", required=False) or None
        artist = read_input(f"New Artist ({album.artist})", required=False) or None
        genre = read_input(f"New Genre ({album.genre})", required=False) or None
        
        price_str = read_input(f"New Price ({album.price})", required=False)
        price = int(price_str) if price_str else None
        
        stock_str = read_input(f"New Stock ({album.stock})", required=False)
        stock = int(stock_str) if stock_str else None

        try:
            self.album_service.update_album(album_id, title, artist, genre, price, stock)
            print(" [✓] Album updated successfully.")
        except ValueError as e:
            print(f" [!] Error: {e}")

    def delete_album(self):
        print_subheader("Delete Album")
        album_id = read_int("Enter Album ID to delete")
        album = self.album_service.get_album_by_id(album_id)
        if not album:
            print(" [!] Album not found.")
            return

        confirm = read_input(f"Are you sure you want to delete '{album.title}'? (y/n)").lower()
        if confirm == 'y':
            try:
                self.album_service.delete_album(album_id)
                print(" [✓] Album deleted successfully.")
            except ValueError as e:
                print(f" [!] Error: {e}")

    def manage_orders(self):
        while True:
            print_subheader("Order Management")
            options = {
                "1": "View All Orders",
                "2": "Update Order Status",
                "3": "Back"
            }
            print_menu_options(options)
            choice = read_input("Select Option")

            if choice == "1":
                self.view_all_orders()
            elif choice == "2":
                self.update_order_status()
            elif choice == "3":
                break
            else:
                print(" [!] Invalid option.")

    def view_all_orders(self):
        print_subheader("All Orders")
        orders = self.order_service.get_all_orders()
        if not orders:
            print(" No orders found in the system.")
            return

        for order in orders:
            print(f"\nOrder ID: {order.id} | User: {order.user_username} | Date: {order.order_date} | Status: [{order.status}]")
            headers = ["Album ID", "Album Title", "Price", "Qty", "Subtotal"]
            rows = []
            for item in order.items:
                rows.append([item.album_id, item.album_title, f"${item.price:,}", item.quantity, f"${(item.price * item.quantity):,}"])
            print_table(headers, rows)
            print(f"Total Price: ${order.total_price:,}")
            print("-" * 50)

    def update_order_status(self):
        print_subheader("Update Order Status")
        order_id = read_int("Enter Order ID")
        order = self.order_service.order_dao.find_by_id(order_id)
        if not order:
            print(" [!] Order not found.")
            return

        print(f" Current Status: [{order.status}]")
        print(" Choose New Status:")
        print(" [1] PREPARING")
        print(" [2] SHIPPED")
        print(" [3] DELIVERED")
        print(" [4] CANCELLED")
        choice = read_input("Select Status Option")

        status_map = {
            "1": "PREPARING",
            "2": "SHIPPED",
            "3": "DELIVERED",
            "4": "CANCELLED"
        }
        
        new_status = status_map.get(choice)
        if not new_status:
            print(" [!] Invalid choice.")
            return

        try:
            self.order_service.update_order_status(order_id, new_status)
            print(f" [✓] Order status updated to [{new_status}].")
        except ValueError as e:
            print(f" [!] Error: {e}")

    def view_users(self):
        print_subheader("Registered User List")
        users = self.user_service.user_dao.find_all()
        headers = ["ID", "Username", "Name", "Role"]
        rows = []
        for u in users:
            rows.append([u.id, u.username, u.name, u.role])
        print_table(headers, rows)
