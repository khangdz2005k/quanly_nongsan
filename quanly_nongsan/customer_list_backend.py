import reflex as rx
import pyodbc
import os
from dotenv import load_dotenv
from rxconfig import config

load_dotenv()
CONNECTION_STRING = os.getenv("DATABASE_URL")

class State(rx.State):
    customers: list[dict] = []
    new_customer_user_name: str = ""
    new_customer_name: str = ""
    new_customer_phone_number: str = ""
    new_customer_address: str = ""
    new_customer_contact_info: str = ""
    selected_customer: dict | None = None

    edited_name: str = ""
    edited_phone_number: str = ""
    edited_address: str = ""
    edited_contact_info: str = ""


    def load_customers(self):
        self.selected_customer = None
        self.customers = []
        try:
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT ID, FullName, PhoneNumber, Address, ContactInfo FROM USER ORDER BY ID")
                rows = cursor.fetchall()
                for row in rows:
                    self.customers.append(
                        {
                            "id": row.ID,                           
                            "fullname": row.FullName,
                            "phonenumber": row.PhoneNumber,
                            "address": row.Address,
                            "contactinfo": row.ContactInfo                      
                        }
                    )
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu khách hàng {e}")

    def delete_customer(self):
        if self.selected_customer:
            try:
                with pyodbc.connect(CONNECTION_STRING) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "DELETE FROM Users WHERE ID = ?",
                        (self.selected_customer["id"],),
                    )
                    conn.commit()

                # *** SỬA LỖI: Reset trạng thái ngay lập tức ***
                self.selected_customer = None
                # Tải lại danh sách sau khi xóa
                self.load_customers()
            except Exception as e:
                print(f"Lỗi khi xóa khách hàng {e}")

    def set_customer_name(self, v: str):
        self.new_customer_name = v

    def set_customer_phone_number(self, v: str):
        self.new_customer_phone_number = v

    def set_customer_address(self, v: str):
        self.new_customer_address = v

    def set_customer_contact_info(self, v: str):
        self.new_customer_contact_info = v

    def add_customer(self):
        name = (self.new_customer_name or "").strip()
        address = (self.new_customer_address or "").strip()
        phone_number = (self.new_customer_phone_number or "").strip()
        contact_info = (self.new_customer_contact_info or "").strip()
        if not name or not address or not phone_number or not contact_info:
            return

        try:
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO Users (FullName, Address, PhoneNumber, ContactInfo) VALUES (?, ?, ?, ?)", (name, address, phone_number, contact_info)
                )
                conn.commit()
            self.new_customer_name = ""
            self.new_customer_address = ""
            self.new_customer_phone_number = ""
            self.new_customer_contact_info = ""
            self.load_customers()
        except Exception as e:
            print(f"Lỗi khi thêm khách hàng {e}")
    
    def select_customer(self, item: dict, checked: bool):
        if checked:
            self.selected_customer = item
            # Gán giá trị ban đầu cho các input chỉnh sửa
            self.edited_name = item["name"]
            self.edited_address = item["address"]
            self.edited_phone_number = item["phone_number"]
            self.edited_contact_info = item["contact_info"]
        else:
            self.selected_customer = None

    def set_edited_name(self, name: str):
        self.edited_name = name

    def set_edited_phone_number(self, phone_number: str):
        self.edited_phone_number = phone_number

    def set_edited_address(self, address: str):
        self.edited_address = address

    def set_edited_contact_info(self, contact_info: str):
        self.edited_contact_info = contact_info

    
    def update_customer(self):
        # Kiểm tra xem có sản phẩm nào được chọn không
        if not self.selected_customer:
            return

        # Lấy thông tin cần thiết
        customer_id = self.selected_customer["id"]
        updated_name = self.edited_name
        updated_address = self.edited_address
        updated_phone_number = self.edited_phone_number
        updated_contact_info = self.edited_contact_info

        try:
            # 1. Cập nhật vào cơ sở dữ liệu như cũ
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE Users SET FullName = ?, Address = ?, PhoneNumber = ?, ContactInfo = ?  WHERE ID = ?",
                    (updated_name, updated_address, updated_phone_number, updated_contact_info, customer_id),
                )
                conn.commit()

            # 2. Cập nhật trực tiếp vào danh sách 'products' trong State
            #    thay vì gọi lại self.load_products_type()
            for i, cust in enumerate(self.customers):
                if cust["id"] == customer_id:
                    self.customers[i]["name"] = updated_name
                    self.customers[i]["address"] = updated_address
                    self.customers[i]["phone_number"] = updated_phone_number
                    self.customers[i]["contact_info"] = updated_contact_info
                    break  # Dừng vòng lặp khi đã tìm thấy và cập nhật

            # 3. Xóa sản phẩm đang được chọn để ẩn form và bỏ check
            self.selected_customer = None

        except Exception as e:
            print(f"Lỗi khi cập nhật: {e}")

    def search_customer(self):
        username = (self.new_customer_user_name or "").strip()
        fullname = (self.new_customer_name or "").strip()
        if not username or not fullname:
            return 
        self.customers = []
        try:
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT ID, FullName, Address, PhoneNumber, ContactInfo FROM Users WHERE UserName LIKE ? OR FullName LIKE ? ",
                    (username, fullname,)
                )
                rows = cursor.fetchall()
                for row in rows:
                    self.customers.append(
                        {
                            "id": row.ID,                           
                            "fullname": row.FullName,
                            "phonenumber": row.PhoneNumber,
                            "address": row.Address,
                            "contactinfo": row.ContactInfo        
                        }
                    )
        except Exception as e:
            print(f"Lỗi khi tìm kiếm khách hàng {e}")

    def search_on_enter(self, key: str):
        if key == "Enter":
            return self.search_customer()