import reflex as rx
import pyodbc
import os
from dotenv import load_dotenv
from datetime import datetime

# Tải các biến môi trường từ file .env
load_dotenv()
CONNECTION_STRING = os.getenv("DATABASE_URL")

class ImageState(rx.State):
    """
    State để quản lý các hoạt động liên quan đến hình ảnh.
    """
    # --- Biến State ---
    # Danh sách tất cả hình ảnh
    images: list[dict] = []
    
    # Biến cho form thêm ảnh mới
    new_image_url: str = ""
    new_alt_text: str = ""
    uploaded_image_preview: str = ""
    
    new_image_filename: str = ""
    
    image_search_query: str = ""
    selected_image: dict | None = None

    # --- Phương thức tải danh sách ảnh ---
    def load_images(self):
        """Tải toàn bộ danh sách hình ảnh từ cơ sở dữ liệu."""
        self.images = []
        sql = "SELECT STT, ImageURL, AltText, CreatedAt FROM Images ORDER BY STT DESC"
        try:
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                cursor.execute(sql)
                rows = cursor.fetchall()
                for row in rows:
                    self.images.append({
                        "stt": row.STT,
                        "image_url": row.ImageURL or "",
                        "alt_text": row.AltText or "",
                        # Định dạng lại ngày giờ cho dễ đọc
                        "created_at": row.CreatedAt.strftime("%Y-%m-%d %H:%M:%S") if row.CreatedAt else ""
                    })
        except Exception as e:
            print(f"Lỗi khi tải danh sách ảnh: {e}")

    # --- Phương thức xử lý Upload ---
    async def handle_upload(self, files: list[rx.UploadFile]):
        """
        Xử lý khi người dùng upload file ảnh.
        Lưu file vào thư mục .web/public/ và cập nhật state để xem trước.
        """
        if not files:
            return

        file = files[0]
        
        original_filename = file.filename
        _, file_extension = os.path.splitext(original_filename)
        
        custom_name = self.new_image_filename.strip().replace(" ", "-")
        if custom_name:
            # Nếu người dùng có nhập tên, sử dụng tên đó + phần mở rộng
            final_filename = f"{custom_name}{file_extension}"
        else:
            # Nếu không, dùng tên file gốc
            final_filename = original_filename
        
        upload_data = await file.read()
        outfile_path = f".web/public/{file.filename}"

        # Lưu file vào thư mục public của web
        with open(outfile_path, "wb") as file_object:
            file_object.write(upload_data)

        # Cập nhật state với đường dẫn của file để hiển thị và lưu
        self.new_image_url = f"/{file.filename}"
        self.uploaded_image_preview = self.new_image_url
        yield

    # --- Phương thức thêm ảnh vào CSDL ---
    def add_image(self):
        """Lưu thông tin ảnh vào cơ sở dữ liệu."""
        if not self.new_image_url.strip():
            return rx.window_alert("Vui lòng upload một hình ảnh trước.")

        sql = """
            INSERT INTO Images (ImageURL, AltText, CreatedAt) 
            VALUES (?, ?, ?)
        """
        try:
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (
                    self.new_image_url,
                    self.new_alt_text.strip() or None, # Gửi NULL nếu trống
                    datetime.now() # Tự động lấy thời gian hiện tại
                ))
                conn.commit()

            # Reset form và tải lại danh sách
            self.new_image_url = ""
            self.new_alt_text = ""
            self.uploaded_image_preview = ""
            self.new_image_filename = ""
            self.load_images()

            return rx.window_alert("Thêm ảnh thành công!")
        except Exception as e:
            print(f"Lỗi khi thêm ảnh vào CSDL: {e}")
            return rx.window_alert(f"Đã xảy ra lỗi: {e}")
        
    def handle_image_selection(self, checked: bool, image: dict):
        """Xử lý khi checkbox của một ảnh được check hoặc uncheck."""
        if checked:
            self.selected_image = image
        else:
            if self.selected_image and self.selected_image["stt"] == image["stt"]:
                self.selected_image = None
                
    def delete_image(self):
        """Xóa ảnh đã chọn khỏi CSDL và thư mục public."""
        if not self.selected_image:
            return rx.window_alert("Vui lòng chọn một ảnh để xóa.")

        try:
            url_to_delete = self.selected_image["image_url"]
            
            # Bước 1: Xóa file vật lý khỏi server
            filename = url_to_delete.strip("/")
            filepath = f".web/public/{filename}"
            if os.path.exists(filepath):
                os.remove(filepath)

            # Bước 2: Xóa record khỏi CSDL
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Images WHERE ImageURL = ?", (url_to_delete,))
                conn.commit()
            
            # Bước 3: Cập nhật lại giao diện
            self.selected_image = None # Reset lựa chọn
            self.load_images()
            return rx.window_alert("Xóa ảnh thành công!")
        except Exception as e:
            print(f"Lỗi khi xóa ảnh: {e}")
            return rx.window_alert(f"Đã xảy ra lỗi: {e}")
        
    def search_images(self):
        """Tìm kiếm ảnh theo URL."""
        query = f"%{self.image_search_query.strip()}%"
        if not self.image_search_query.strip():
            self.load_images()
            return

        self.images = []
        sql = "SELECT STT, ImageURL, AltText, CreatedAt FROM Images WHERE ImageURL LIKE ? ORDER BY STT DESC"
        try:
            with pyodbc.connect(CONNECTION_STRING) as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (query,))
                rows = cursor.fetchall()
                for row in rows:
                    self.images.append({
                        "stt": row.STT, "image_url": row.ImageURL or "", "alt_text": row.AltText or "",
                        "created_at": row.CreatedAt.strftime("%Y-%m-%d %H:%M:%S") if row.CreatedAt else ""
                    })
        except Exception as e:
            print(f"Lỗi khi tìm kiếm ảnh: {e}")
            
    def search_images_on_enter(self, key: str):
        """Gọi hàm search_images khi người dùng nhấn phím Enter."""
        if key == "Enter":
            return self.search_images()
        
    def set_image_search_query(self, query: str):
        self.image_search_query = query
        
    def set_new_image_filename(self, filename: str):
        self.new_image_filename = filename

    # --- Setters cho các trường input ---
    def set_new_alt_text(self, text: str):
        """Cập nhật giá trị của ô AltText."""
        self.new_alt_text = text