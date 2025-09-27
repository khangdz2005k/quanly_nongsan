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
        if not label or not code:
            return

        try:
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO ProductTypes (Name, Code) VALUES (?, ?)", (label, code)
                )
                conn.commit()
            self.new_product_type_name = ""
            self.new_product_type_code = ""
            self.load_products_type()
        except Exception as e:
            print(f"Lỗi khi thêm loại hàng {e}")

    def set_product_type_name(self, v: str):
        self.new_product_type_name = v

    def set_product_type_code(self, v: str):
        self.new_product_type_code = v

    def load_products_type(self):
        self.products = []
        try:
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT ID, Code, Name, CreatedAt FROM ProductTypes ORDER BY CreatedAt"
                )
                rows = cursor.fetchall()
                # tasks sẽ là list dict để dễ quản lý
                for row in rows:
                    # Lấy giá trị datetime
                    created_at_val = getattr(row, "CreatedAt", None)
                    # Định dạng lại nếu giá trị tồn tại, nếu không thì là chuỗi rỗng
                    formatted_date = (
                        created_at_val.strftime("%Y-%m-%d %H:%M:%S")
                        if created_at_val
                        else ""
                    )
                    self.products.append(
                        {
                            "id": row.ID,
                            "code": row.Code,
                            "name": row.Name,
                            "createdat": formatted_date, # Sử dụng giá trị đã định dạng
                        }
                    )
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu {e}")

    def search_products_type(self):
        code = (self.new_product_type_code or "").strip()
        if not code:
            return self.load_products_type()

        self.products = []

        try:
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT ID, Code, Name, CreatedAt FROM ProductTypes WHERE Code LIKE ? ORDER BY CreatedAt DESC",
                    ("%" + code + "%",),
                )
                rows = cursor.fetchall()
                for row in rows:
                    # Lấy giá trị datetime
                    created_at_val = getattr(row, "CreatedAt", None)
                    # Định dạng lại nếu giá trị tồn tại, nếu không thì là chuỗi rỗng
                    formatted_date = (
                        created_at_val.strftime("%Y-%m-%d %H:%M:%S")
                        if created_at_val
                        else ""
                    )
                    self.products.append(
                        {
                            "id": row.ID,
                            "code": row.Code,
                            "name": row.Name,
                            "createdat": formatted_date, # Sử dụng giá trị đã định dạng
                        }
                    )
        except Exception as e:
            print(f"Lỗi khi tìm kiếm {e}")

    def search_on_enter(self, key: str):
        # Tên type có thể là KeyEvent/KeyboardEvent tùy phiên bản Reflex; nếu bạn không import được
        # cứ để tham số 'e' không gõ kiểu cũng được.
        if key == "Enter":
            return self.search_products_type()

    # def delete_products_type(self, ids: list[int]):
    #     ids = [int(i) for i in ids]
    #     if not ids:
    #         return
    #     try:
    #         with pyodbc.connect(CONNECTION_STRING) as conn:
    #             cursor = conn.cursor()
    #             placeholder = ",".join("?" for i in ids)
    #             cursor.execute(f"DELETE FROM ProductTypes WHERE ID IN ({placeholder})", tuple(ids))
    #             conn.commit()
    #         self.load_products_type()
    #     except Exception as e:
    #         print(f"Lỗi khi xoá {e}")

    # def select_products_type(self, product_id: int):
    #     try:
    #         with pyodbc.connect(CONNECTION_STRING) as conn:
    #             cursor = conn.cursor()
    #             cursor.excute("SELECT ID, Code, Name FROM ProductTypes WHERE ID = ?", product_id)
    #             rows = cursor.fetchone()
    #     except Exception as e:
    #         print(f"Lỗi khi chọn {e}")

    # def update_products_type(self):

    # def editing_products_type(self):