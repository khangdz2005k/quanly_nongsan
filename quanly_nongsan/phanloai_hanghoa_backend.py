"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import bcrypt
import reflex as rx
import pyodbc
import os
import datetime
from dotenv import load_dotenv
from rxconfig import config

load_dotenv()
# Lấy chuỗi kết nối từ biến môi trường đã được tải
CONNECTION_STRING = os.getenv("DATABASE_URL")


class State(rx.State):
    """The app state."""
    products: list[dict] = []
    new_product_type_name: str = ""
    new_product_type_code: str = ""
    def add_product(self):
        label = (self.new_product_type_name or "").strip()
        code = (self.new_product_type_code or "").strip()
        if not label: 
            return
        if not code:
            return 
        try:
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO ProductTypes VALUES (?, ?)", (label, code))
                conn.commit()
            self.load_products()
            self.new_product_type_name = ""
            self.new_product_type_code = ""
        except Exception as e:
            print(f"Lỗi {e}")

    def set_product_type_name(self, product: str):
        self.new_product_type_name = product

    def set_product_type_code(self, product: str):
        self.new_product_type_code = product


    def load_products_type(self):
        self.products = []
        try: 
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT ID, Code, Name, CreatedAt FROM ProductTypes ORDER BY CreatedAt")
                rows = cursor.fetchall()
                # tasks sẽ là list dict để dễ quản lý
                for row in rows:
                    self.products.append({"id": row.ID, "code": row.Code, "name": row.Name, "createdat": row.CreatedAt})
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu {e}")

    def search_products_type(self):
        self.products = []
        code = (self.new_product_type_code or "").strip()
        if not code:
            return
        try:
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT ID, Code, Name, CreatedAt FROM ProductTypes WHERE Code LIKE ?", code)
                rows = cursor.fetchall()
                for row in rows:
                    self.products.append({"id": row.ID, "code": row.Code, "name": row.Name, "createdat": row.CreatedAt.strftime("%Y-%m-%d %H-%M-%S")})
        except Exception as e:
            print(f"Lỗi khi tìm kiếm {e}")

    def delete_products_type(self, ids: list[int]):
        ids = [int(i) for i in ids]
        if not ids:
            return
        try:
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                placeholder = ",".join("?" for i in ids)
                cursor.execute(f"DELETE FROM ProductTypes WHERE ID IN ({placeholder})", tuple(ids))
                conn.commit()
            self.load_products_type()
        except Exception as e:
            print(f"Lỗi khi xoá {e}")

    def select_products_type(self, product_id: int):
        try:
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                cursor.excute("SELECT ID, Code, Name FROM ProductTypes WHERE ID = ?", product_id)
                rows = cursor.fetchone()
        except Exception as e:
            print(f"Lỗi khi chọn {e}")

    def update_products_type(self):

    def editing_products_type(self):



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
