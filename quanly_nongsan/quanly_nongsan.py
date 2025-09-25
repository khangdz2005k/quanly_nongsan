"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import bcrypt
import reflex as rx
import pyodbc
import os
from dotenv import load_dotenv
from rxconfig import config

load_dotenv()
# Lấy chuỗi kết nối từ biến môi trường đã được tải
CONNECTION_STRING = os.getenv("DATABASE_URL")


class State(rx.State):
    """The app state."""
    username: str = ""
    password: str = ""
    error_message: str = ""
    def handle_login(self):
        """Xử lý logic đăng nhập."""
        self.error_message = "" # Reset thông báo lỗi
        try:
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                # Tìm user dựa trên username
                cursor.execute("SELECT PasswordHash FROM Users WHERE Username = ?", self.username)
                user_row = cursor.fetchone()
                if user_row and bcrypt.checkpw(self.password.encode(), user_row.PasswordHash.encode()):
                    # ĐĂNG NHẬP THÀNH CÔNG!
                    # Thay vì alert, chúng ta chuyển hướng đến trang dashboard
                    return rx.redirect("/dashboard") 
                else:
                    # ĐĂNG NHẬP THẤT BẠI
                    self.error_message = "Tên đăng nhập hoặc mật khẩu không đúng."

        except Exception as e:
            self.error_message = "Lỗi kết nối database."
            print(f"Lỗi đăng nhập: {e}")

    def set_username(self, value:str):
        self.username = value
        self.error_message = ""

    def set_password (self, value:str):
        self.password = value
        self.error_message = ""

def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )


app = rx.App()
app.add_page(index)
