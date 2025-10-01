import reflex as rx
import pyodbc
import os
from dotenv import load_dotenv
from rxconfig import config

load_dotenv()
CONNECTION_STRING = os.getenv("DATABASE_URL")


class State(rx.State):
    products: list[dict] = []
    new_product_name: str = ""
    new_product_code: str = ""
    product_types_code: list = []
    selected_product: dict | None = None

    selected_product_type_code: str = ""  # Lưu loại hàng được chọn từ rx.select
    new_product_expiry_date: str = ""  # Lưu giá trị 'Ngày hết hạn'
    new_product_notes: str = ""  # Lưu giá trị 'Ghi chú'

    # Cần thêm các biến cho chức năng update/edit nếu bạn dùng
    edited_code: str = ""
    edited_name: str = ""
    edited_imageurl: str = ""
    edited_notes: str = ""

    uploaded_files: list[str] = [] 
    product_image_url: str = ""

    def set_selected_product_type_code(self, value: str):
        self.selected_product_type_code = value
        print(f"Loại hàng đã chọn: {self.selected_product_type_code}")
    
    def upload_complete(self, file_ig: list[str]):
        self.uploaded_files.extend(file_ig)
    def load_products(self):
        self.products = []
        try:
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT ID, ProductCode, Name, ExpiryDate, ImageURL, Notes FROM Products ORDER BY ID"
                )
                rows = cursor.fetchall()
                for row in rows:
                    self.products.append(
                        {
                            "id": row.ID,
                            "code": row.Code,
                            "name": row.Name,
                            "expirydate": row.ExpiryDate,
                            "imageurl": row.ImageURL,
                            "notes": row.Notes,
                        }
                    )
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu {e}")

    def load_product_types_code(self):
        try:
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                cursor.excute("SELECT Code FROM ProductTypes")
                rows = cursor.fetchall()
                for row in rows:
                    self.product_types_code.append(row.Code)
        except Exception as e:
            print(f"Lỗi khi tải mã loại hàng {e}")

    def select_product(self, item: dict, checked: bool):
        if checked:
            self.selected_product = item
            # Gán giá trị ban đầu cho các input chỉnh sửa
            self.edited_code = item["code"]
            self.edited_name = item["name"]
        else:
            self.selected_product = None

    def delete_product(self):
        if self.selected_product:
            try:
                with pyodbc.connect(CONNECTION_STRING) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "DELETE FROM Products WHERE ID = ?",
                        (self.selected_product["id"],),
                    )
                    conn.commit()

                # *** SỬA LỖI: Reset trạng thái ngay lập tức ***
                self.selected_product = None
                # Tải lại danh sách sau khi xóa
                self.load_products()
            except Exception as e:
                print(f"Lỗi khi xóa: {e}")

    def search_products_type(self):
        code = (self.new_products_code or "").strip()
        if not code:
            return self.load_products()

        self.products = []
        try:
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT ID, ProductCode, Name, ExpiryDate, ImageURL, Notes FROM Products WHERE Code LIKE ? ORDER BY ID",
                    ("%" + code + "%",),
                )
                rows = cursor.fetchall()
                for row in rows:
                    self.products.append(
                        {
                            "id": row.ID,
                            "code": row.Code,
                            "name": row.Name,
                            "expirydate": row.ExpiryDate,
                            "imageurl": row.ImageURL,
                            "notes": row.Notes,
                        }
                    )
        except Exception as e:
            print(f"Lỗi khi tìm kiếm {e}")

    def update_product(self):
        # Kiểm tra xem có sản phẩm nào được chọn không
        if not self.selected_product:
            return

        # Lấy thông tin cần thiết
        product_id = self.selected_product["id"]
        updated_code = self.edited_code
        updated_name = self.edited_name
        update_image_url = self.edited_imageurl
        updated_notes = self.edited_notes

        try:
            # 1. Cập nhật vào cơ sở dữ liệu như cũ
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE ProductTypes SET Name = ?, ProductCode = ?, ImageURL = ?, Notes = ? WHERE ID = ?",
                    (
                        updated_name,
                        updated_code,
                        update_image_url,
                        updated_notes,
                        product_id,
                    ),
                )
                conn.commit()

            # 2. Cập nhật trực tiếp vào danh sách 'products' trong State
            #    thay vì gọi lại self.load_products_type()
            for i, prod in enumerate(self.products):
                if prod["id"] == product_id:
                    self.products[i]["code"] = updated_code
                    self.products[i]["name"] = updated_name
                    break  # Dừng vòng lặp khi đã tìm thấy và cập nhật

            # 3. Xóa sản phẩm đang được chọn để ẩn form và bỏ check
            self.selected_product = None

        except Exception as e:
            print(f"Lỗi khi cập nhật: {e}")

    def add_products(self):
        name_product = (self.new_product_name or "").strip()
        code_product = (self.new_product_code or "").strip()
        type_code = self.selected_product_type_code
        expiry_date = self.new_product_expiry_date or None
        notes = (self.new_product_notes or "").strip()

        if not name_product or not code_product or not type_code:
            print("Tên, Mã và Loại hàng không được để trống")
            return

        try:
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO Products (Name, ProductCode, ProductType, ExpiryDate, Notes) VALUES (?, ?, ?, ?, ?)",
                    (name_product, code_product, type_code, expiry_date, notes),
                )
                conn.commit()
            print(f"Đã thêm sản phẩm mới: {name_product} ({code_product})")

            self.new_products_name = ""
            self.new_products_code = ""
            self.selected_product_type_code = ""
            self.new_product_notes = ""
            self.new_product_expiry_date = ""
            self.load_products()
        except Exception as e:
            print(f"Lỗi khi thêm loại hàng {e}")
