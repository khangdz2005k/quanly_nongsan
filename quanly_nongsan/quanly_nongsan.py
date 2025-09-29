"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import bcrypt
import reflex as rx
import pyodbc
import os
from dotenv import load_dotenv
from rxconfig import config
from .login import index as login_page


load_dotenv()
# Lấy chuỗi kết nối từ biến môi trường đã được tải
CONNECTION_STRING = os.getenv("DATABASE_URL")


app = rx.App()
app.add_page(login_page, route="/login")