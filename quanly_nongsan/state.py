# state.py
import reflex as rx
import bcrypt, pyodbc, os
from dotenv import load_dotenv

load_dotenv()
CONNECTION_STRING = os.getenv("DATABASE_URL")


class State(rx.State):
    username: str = ""
    password: str = ""
    error_message: str = ""

    def handle_login(self):
        """Xử lý logic đăng nhập."""
        self.error_message = ""  # Reset thông báo lỗi
        try:
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                # Tìm user dựa trên username
                cursor.execute(
                    "SELECT PasswordHash FROM Users WHERE Username = ?", self.username
                )
                user_row = cursor.fetchone()
                if user_row and bcrypt.checkpw(
                    self.password.encode(), user_row.PasswordHash.encode()
                ):
                    # ĐĂNG NHẬP THÀNH CÔNG!
                    # Thay vì alert, chúng ta chuyển hướng đến trang dashboard
                    return rx.redirect("/")
                else:
                    # ĐĂNG NHẬP THẤT BẠI
                    self.error_message = "Tên đăng nhập hoặc mật khẩu không đúng."

        except Exception as e:
            self.error_message = "Lỗi kết nối database."
            print(f"Lỗi đăng nhập: {e}")

    def set_username(self, value: str):
        self.username = value
        self.error_message = ""

    def set_password(self, value: str):
        self.password = value
        self.error_message = ""
