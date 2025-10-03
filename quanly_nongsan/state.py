# state.py
import reflex as rx
from dotenv import load_dotenv
import bcrypt
import pyodbc
import os
from .phanloai_hanghoa_backend import State as productState
from .product_category_backend import State as productState2

load_dotenv()
# Lấy chuỗi kết nối từ biến môi trường đã được tải
CONNECTION_STRING = os.getenv("DATABASE_URL")


class State(rx.State):
    username: str = ""
    password: str = ""
    error_message: str = ""
    productState = productState
    productState2 = productState2

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
                    return rx.redirect("/manage_product_types")
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


# class ProductState(rx.State):
#     """The app state."""

#     products: list[dict] = []
#     new_product_type_name: str = ""
#     new_product_type_code: str = ""

#     # Biến trạng thái mới để lưu sản phẩm đang được chọn
#     selected_product: dict | None = None
#     # Biến để lưu giá trị đang chỉnh sửa
#     edited_code: str = ""
#     edited_name: str = ""

#     def add_product(self):
#         label = (self.new_product_type_name or "").strip()
#         code = (self.new_product_type_code or "").strip()
#         if not label or not code:
#             return

#         try:
#             with pyodbc.connect(CONNECTION_STRING) as conn:
#                 cursor = conn.cursor()
#                 cursor.execute(
#                     "INSERT INTO ProductTypes (Name, Code) VALUES (?, ?)", (label, code)
#                 )
#                 conn.commit()
#             self.new_product_type_name = ""
#             self.new_product_type_code = ""
#             self.load_products_type()
#         except Exception as e:
#             print(f"Lỗi khi thêm loại hàng {e}")

#     def set_product_type_name(self, v: str):
#         self.new_product_type_name = v

#     def set_product_type_code(self, v: str):
#         self.new_product_type_code = v

#     def load_products_type(self):
#         # Đảm bảo bỏ chọn khi tải lại danh sách
#         self.selected_product = None
#         self.products = []
#         try:
#             with pyodbc.connect(CONNECTION_STRING) as conn:
#                 cursor = conn.cursor()
#                 cursor.execute(
#                     "SELECT ID, Code, Name, CreatedAt FROM ProductTypes ORDER BY CreatedAt"
#                 )
#                 rows = cursor.fetchall()
#                 # tasks sẽ là list dict để dễ quản lý
#                 for row in rows:
#                     # Lấy giá trị datetime
#                     created_at_val = getattr(row, "CreatedAt", None)
#                     # Định dạng lại nếu giá trị tồn tại, nếu không thì là chuỗi rỗng
#                 for row in rows:
#                     created_at_val = getattr(row, "CreatedAt", None)
#                     formatted_date = (
#                         created_at_val.strftime("%Y-%m-%d %H:%M:%S")
#                         if created_at_val
#                         else ""
#                     )
#                     self.products.append(
#                         {
#                             "id": row.ID,
#                             "code": row.Code,
#                             "name": row.Name,
#                             "createdat": formatted_date,  # Sử dụng giá trị đã định dạng
#                         }
#                     )
#         except Exception as e:
#             print(f"Lỗi khi tải dữ liệu {e}")

#     # Hàm mới để xử lý việc chọn/bỏ chọn
#     def select_product(self, item: dict, checked: bool):
#         if checked:
#             self.selected_product = item
#             # Gán giá trị ban đầu cho các input chỉnh sửa
#             self.edited_code = item["code"]
#             self.edited_name = item["name"]
#         else:
#             self.selected_product = None

#     # Hàm setter cho các input chỉnh sửa
#     def set_edited_code(self, code: str):
#         self.edited_code = code

#     def set_edited_name(self, name: str):
#         self.edited_name = name

#     # Hàm để cập nhật thông tin
#     # Trong class State của file phanloai_hanghoa_backend.py

#     def update_product(self):
#         # Kiểm tra xem có sản phẩm nào được chọn không
#         if not self.selected_product:
#             return

#         # Lấy thông tin cần thiết
#         product_id = self.selected_product["id"]
#         updated_code = self.edited_code
#         updated_name = self.edited_name

#         try:
#             # 1. Cập nhật vào cơ sở dữ liệu như cũ
#             with pyodbc.connect(CONNECTION_STRING) as conn:
#                 cursor = conn.cursor()
#                 cursor.execute(
#                     "UPDATE ProductTypes SET Code = ?, Name = ? WHERE ID = ?",
#                     (updated_code, updated_name, product_id),
#                 )
#                 conn.commit()

#             # 2. Cập nhật trực tiếp vào danh sách 'products' trong State
#             #    thay vì gọi lại self.load_products_type()
#             for i, prod in enumerate(self.products):
#                 if prod["id"] == product_id:
#                     self.products[i]["code"] = updated_code
#                     self.products[i]["name"] = updated_name
#                     break  # Dừng vòng lặp khi đã tìm thấy và cập nhật

#             # 3. Xóa sản phẩm đang được chọn để ẩn form và bỏ check
#             self.selected_product = None

#         except Exception as e:
#             print(f"Lỗi khi cập nhật: {e}")

#     # Hàm để xóa
#     def delete_product(self):
#         if self.selected_product:
#             try:
#                 with pyodbc.connect(CONNECTION_STRING) as conn:
#                     cursor = conn.cursor()
#                     cursor.execute(
#                         "DELETE FROM ProductTypes WHERE ID = ?",
#                         (self.selected_product["id"],),
#                     )
#                     conn.commit()

#                 # *** SỬA LỖI: Reset trạng thái ngay lập tức ***
#                 self.selected_product = None
#                 # Tải lại danh sách sau khi xóa
#                 self.load_products_type()
#             except Exception as e:
#                 print(f"Lỗi khi xóa: {e}")

#     def search_products_type(self):
#         code = (self.new_product_type_code or "").strip()
#         if not code:
#             return self.load_products_type()

#         self.products = []

#         self.products = []
#         try:
#             with pyodbc.connect(CONNECTION_STRING) as conn:
#                 cursor = conn.cursor()
#                 cursor.execute(
#                     "SELECT ID, Code, Name, CreatedAt FROM ProductTypes WHERE Code LIKE ? ORDER BY CreatedAt DESC",
#                     ("%" + code + "%",),
#                 )
#                 rows = cursor.fetchall()
#                 for row in rows:
#                     created_at_val = getattr(row, "CreatedAt", None)
#                     formatted_date = (
#                         created_at_val.strftime("%Y-%m-%d %H:%M:%S")
#                         if created_at_val
#                         else ""
#                     )
#                     self.products.append(
#                         {
#                             "id": row.ID,
#                             "code": row.Code,
#                             "name": row.Name,
#                             "createdat": formatted_date,
#                         }
#                     )
#         except Exception as e:
#             print(f"Lỗi khi tìm kiếm {e}")

#     def search_on_enter(self, key: str):
#         if key == "Enter":
#             return self.search_products_type()
