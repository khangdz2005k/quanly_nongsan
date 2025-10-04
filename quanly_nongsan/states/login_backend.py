import reflex as rx
from dotenv import load_dotenv
import bcrypt
import pyodbc
import os

load_dotenv()
# Lấy chuỗi kết nối từ biến môi trường đã được tải
CONNECTION_STRING = os.getenv("DATABASE_URL")


class State(rx.State):
    username: str = ""
    password: str = ""
    error_message: str = ""
    current_user: dict = {}

    def handle_login(self):
        """Xử lý logic đăng nhập."""
        self.error_message = ""  # Reset thông báo lỗi
        try:
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                # Tìm user dựa trên username
                cursor.execute(
                    "SELECT Username, PasswordHash, Role FROM Users WHERE Username = ?", self.username
                )
                user_row = cursor.fetchone()
                if user_row and bcrypt.checkpw(
                    self.password.encode(), user_row.PasswordHash.encode()
                ):
                    self.current_user = {"username": user_row.Username, "role": user_row.Role}
                    if(self.current_user["role"] == "user"):
                        return rx.redirect("/customer")
                    else:
                        return rx.redirect("/product_types")
                    # ĐĂNG NHẬP THÀNH CÔNG!
                    # Thay vì alert, chúng ta chuyển hướng đến trang dashboard
                else:
                    # ĐĂNG NHẬP THẤT BẠI
                    self.error_message = "Tên đăng nhập hoặc mật khẩu không đúng."

        except Exception as e:
            self.error_message = "Lỗi kết nối database."
            print(f"Lỗi đăng nhập: {e}")
            
    def handle_logout(self):
        self.current_user = {}
        self.username = ""
        self.password = ""
        return rx.redirect("/login_page")
    
    def login_on_enter(self, key: str):
        if key == "Enter":
            return self.handle_login()

    def set_username(self, value: str):
        self.username = value
        self.error_message = ""

    def set_password(self, value: str):
        self.password = value
        self.error_message = ""
