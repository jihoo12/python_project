import os
import sys

from dao.user_dao import UserDAO
from dao.album_dao import AlbumDAO
from dao.order_dao import OrderDAO
from service.user_service import UserService
from service.album_service import AlbumService
from service.order_service import OrderService
from models.user import User
from models.album import Album
from ui.console_utils import print_header, print_subheader, print_menu_options, read_input, read_int
from ui.user_menu import UserMenu
from ui.admin_menu import AdminMenu

def init_default_data(user_dao, album_dao):
    # Initialize Admin and User if users list is empty
    if not user_dao.find_all():
        admin_user = User(username="admin", password="123", name="관리자", role="ADMIN")
        regular_user = User(username="user1", password="123", name="홍길동", role="USER")
        user_dao.insert(admin_user)
        user_dao.insert(regular_user)
        print(" [System] Default users created: admin/123 (ADMIN), user1/123 (USER)")

    # Initialize default albums if empty
    if not album_dao.find_all():
        default_albums = [
            Album(title="BE", artist="BTS", genre="K-POP", price=35000, stock=50),
            Album(title="The Dark Side of the Moon", artist="Pink Floyd", genre="Rock", price=42000, stock=15),
            Album(title="Thriller", artist="Michael Jackson", genre="Pop", price=38000, stock=20),
            Album(title="Kind of Blue", artist="Miles Davis", genre="Jazz", price=29000, stock=10),
            Album(title="Symphony No. 9", artist="Beethoven", genre="Classical", price=25000, stock=30)
        ]
        for album in default_albums:
            album_dao.insert(album)
        print(" [System] Default albums catalog initialized.")

def main():
    user_dao = UserDAO()
    album_dao = AlbumDAO()
    order_dao = OrderDAO()

    # Pre-populate default data on first execution
    init_default_data(user_dao, album_dao)

    user_service = UserService(user_dao)
    album_service = AlbumService(album_dao)
    order_service = OrderService(order_dao, album_dao)

    while True:
        print_header("음반 판매 쇼핑몰 (Album Store)")
        options = {
            "1": "로그인 (Login)",
            "2": "회원가입 (Sign Up)",
            "3": "프로그램 종료 (Exit)"
        }
        print_menu_options(options)
        choice = read_input("메뉴 선택 (Select Option)")

        if choice == "1":
            print_subheader("로그인 (Login)")
            username = read_input("아이디 (Username)")
            password = read_input("비밀번호 (Password)")
            user = user_service.login(username, password)
            if user:
                print(f"\n [✓] 로그인 성공! {user.name}님 환영합니다.")
                if user.role == "ADMIN":
                    menu = AdminMenu(user, album_service, order_service, user_service)
                    menu.run()
                else:
                    menu = UserMenu(user, album_service, order_service)
                    menu.run()
            else:
                print(" [!] 아이디 또는 비밀번호가 틀렸습니다.")

        elif choice == "2":
            print_subheader("회원가입 (Sign Up)")
            username = read_input("아이디 (Username)")
            password = read_input("비밀번호 (Password)")
            name = read_input("이름 (Full Name)")
            try:
                user_service.register(username, password, name, role="USER")
                print(" [✓] 회원가입이 완료되었습니다! 로그인해 주세요.")
            except ValueError as e:
                print(f" [!] 회원가입 실패: {e}")

        elif choice == "3":
            print("\n 프로그램을 종료합니다. 감사합니다!")
            sys.exit(0)
        else:
            print(" [!] 잘못된 선택입니다. 다시 선택해 주세요.")

if __name__ == "__main__":
    main()
