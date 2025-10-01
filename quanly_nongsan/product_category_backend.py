import reflex as rx
import pyodbc
import os
from dotenv import load_dotenv
import datetime
import asyncio

load_dotenv()
CONNECTION_STRING = os.getenv("DATABASE_URL")


class State(rx.State):
    products: list[dict] = []
    product_types_options: list[str] = []
    selected_product: int | None = None

    # --- Biến cho form "Thêm" ---
    selected_type_code: str = ""
    new_product_code: str = ""
    new_product_name: str = ""
    new_expiry_date: str = ""
    new_notes: str = ""
    new_image_url: str = ""
    uploaded_image_preview: str = ""

    # --- Biến cho form "Sửa" ---
    selected_product: dict | None = None
    edited_code: str = ""
    edited_name: str = ""
    edited_type_code: str = ""
    edited_expiry_date: str = ""
    edited_notes: str = ""
    edited_image_url: str = ""

    search_query: str = ""

    # Biến cho dialog xác nhận xóa
    show_delete_confirm_dialog: bool = False

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Xử lý việc tải file lên.

        Args:
            files: Danh sách các file được tải lên.
        """
        if not files:
            return

        # Chỉ xử lý file đầu tiên được chọn
        file = files[0]
        upload_data = await file.read()
        outfile = f".web/public/{file.filename}"

        # Lưu file vào thư mục public của web
        with open(outfile, "wb") as file_object:
            file_object.write(upload_data)

        # Cập nhật state với đường dẫn của file và ảnh preview
        self.new_image_url = f"/{file.filename}"
        self.uploaded_image_preview = self.new_image_url
        yield

    def on_page_load(self):
        self.load_products()
        self.load_product_types_code()

    def load_products(self):
        self.products = []
        try:
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT ID, ProductCode, Name, ProductType, ExpiryDate, ImageURL, Notes FROM Products ORDER BY ID DESC"
                )
                rows = cursor.fetchall()
                for row in rows:
                    expiry_date_str = (
                        row.ExpiryDate.strftime("%Y-%m-%d")
                        if isinstance(row.ExpiryDate, datetime.date)
                        else ""
                    )
                    self.products.append(
                        {
                            "id": row.ID,
                            "code": row.ProductCode,
                            "name": row.Name,
                            "producttype": row.ProductType,
                            "expirydate": expiry_date_str,
                            "imageurl": row.ImageURL,
                            "notes": row.Notes,
                        }
                    )
        except Exception as e:
            print(f"Lỗi khi tải sản phẩm {e}")

    def load_product_types_code(self):
        self.product_types_options = []
        try:
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Code FROM ProductTypes ORDER BY Code")
                rows = cursor.fetchall()
                for row in rows:
                    self.product_types_options.append(row.Code)
        except Exception as e:
            print(f"Lỗi khi tải mã loại hàng {e}")

    def handle_selection(self, checked: bool, product: dict):
        """
        Xử lý khi một checkbox được check hoặc uncheck.
        Đây là logic mới để sửa lỗi TypeError.
        """
        if checked:
            # Nếu checkbox được check, chọn sản phẩm này
            self.selected_product = product
            # Đồng thời điền thông tin vào form sửa
            self.edited_code = product.get("code", "")
            self.edited_name = product.get("name", "")
            self.edited_type_code = product.get("producttype", "")
            self.edited_expiry_date = product.get("expirydate", "")
            self.edited_notes = product.get("notes", "")
            self.edited_image_url = product.get("imageurl", "")
        else:
            # Nếu checkbox được uncheck, bỏ chọn sản phẩm
            self.selected_product = None

    def unselect_product(self):
        self.selected_product = None

    def change_delete_dialog_state(self, show: bool):
        self.show_delete_confirm_dialog = show

    def delete_product(self):
        if self.selected_product is not None:
            try:
                with pyodbc.connect(CONNECTION_STRING) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "DELETE FROM Products WHERE ID = ?",
                        (self.selected_product["id"],),
                    )
                    conn.commit()
                self.selected_product = None
                self.load_products()
            except Exception as e:
                print(f"Lỗi khi xóa: {e}")

    def search_products(self):
        query = f"%{self.search_query.strip()}%"

        self.products = []
        try:
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT ID, ProductCode, Name, ProductType,ExpiryDate, ImageURL, Notes FROM Products WHERE ProductCode LIKE ? OR Name LIKE ? ORDER BY ID DESC",
                    (query, query),
                )
                rows = cursor.fetchall()
                for row in rows:
                    expiry_date_str = (
                        row.ExpiryDate.strftime("%Y-%m-%d")
                        if isinstance(row.ExpiryDate, datetime.date)
                        else ""
                    )
                    self.products.append(
                        {
                            "id": row.ID,
                            "code": row.ProductCode,
                            "name": row.Name,
                            "producttype": row.ProductType,
                            "expirydate": expiry_date_str,
                            "imageurl": row.ImageURL,
                            "notes": row.Notes,
                        }
                    )
        except Exception as e:
            print(f"Lỗi khi tìm kiếm {e}")

    def update_product(self):
        if self.selected_product is None:
            return

        try:
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE Products SET Name = ?, ProductCode = ?, ProductType = ?, ImageURL = ?, Notes = ?, ExpiryDate = ? WHERE ID = ?",
                    (
                        self.edited_name,
                        self.edited_code,
                        self.edited_type_code,
                        self.edited_image_url,
                        self.edited_notes,
                        self.edited_expiry_date or None,
                        self.selected_product["id"],
                    ),
                )
                conn.commit()
            self.selected_product = None
            self.load_products()
        except Exception as e:
            print(f"Lỗi khi cập nhật: {e}")

    def add_products(self):
        if not self.new_product_name.strip() or not self.selected_type_code:
            return rx.window_alert("Vui lòng chọn loại hàng và nhập tên hàng hóa.")

        product_type_id = None
        try:
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT ID FROM ProductTypes WHERE Code = ?",
                    self.selected_type_code,
                )
                row = cursor.fetchone()
                if not row:
                    return rx.window_alert("Loại hàng không hợp lệ")
                product_type_id = row.ID

                cursor.execute(
                    """
                    INSERT INTO Products (ProductCode, Name, ProductType, ExpiryDate, ImageURL, Notes, ProductTypeID)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    self.new_product_code.strip() or None,
                    self.new_product_name.strip(),
                    self.selected_type_code,
                    self.new_expiry_date or None,
                    self.new_image_url.strip() or None,
                    self.new_notes.strip() or None,
                    product_type_id,
                )
                conn.commit()

                # Reset form
                self.new_product_name = ""
                self.new_product_code = ""
                self.new_expiry_date = ""
                self.new_notes = ""
                self.new_image_url = ""
                self.selected_type_code = ""
                self.load_products()
        except Exception as e:
            print(f"Lỗi khi thêm sản phẩm {e}")
            return rx.window_alert(f"Đã xảy ra lỗi: {e}")

    # --- Event Handlers for input changes ---
    def set_selected_type_code(self, code: str):
        self.selected_type_code = code

    def set_new_product_code(self, code: str):
        self.new_product_code = code

    def set_new_product_name(self, name: str):
        self.new_product_name = name

    def set_new_expiry_date(self, date: str):
        self.new_expiry_date = date

    def set_new_notes(self, notes: str):
        self.new_notes = notes

    def set_new_image_url(self, url: str):
        self.new_image_url = url

    def set_edited_type_code(self, code: str):
        self.edited_type_code = code

    def set_edited_code(self, code: str):
        self.edited_code = code

    def set_edited_name(self, name: str):
        self.edited_name = name

    def set_edited_expiry_date(self, date: str):
        self.edited_expiry_date = date

    def set_edited_notes(self, notes: str):
        self.edited_notes = notes

    def set_edited_image_url(self, url: str):
        self.edited_image_url = url

    def set_search_query(self, query: str):
        self.search_query = query

    def search_on_enter(self, key: str):
        if key == "Enter":
            return self.search_products()
