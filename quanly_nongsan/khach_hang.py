import reflex as rx

# THÊM CỘT "Hành động" cho nút Xóa
HEADERS = [
    "Select",
    "Mã khách hàng",
    "Tên khách hàng",
    "Địa chỉ",
    "Người liên hệ",
    "Số điện thoại",
    "Email",
    "Hành động",  # Đã thêm cột này
]


class State(rx.State):
    selected_customer: dict | None = None
    search_query: str = ""

    # Dữ liệu mẫu (giữ nguyên)
    customers = [
        {
            "id": 1,
            "code": "KH1",
            "name": "Công ty sờ ki bi đi",
            "address": "Quận L, Đường ribidi, TP.SKB",
            "contact_person": "TrẦN NGuyễN RuDIBi",
            "phone": "616516131",
            "email": "Rdib.Tran@gmail.com",
        },
        {
            "id": 2,
            "code": "KH2",
            "name": "Cửa hàng Brainpro chuyên bán lẻ PRoBrot",
            "address": "Quận R, Đường Trlatungten, TP.SKB",
            "contact_person": "Lê HUy TRalero",
            "phone": "32131516",
            "email": "brian.lee@gmail.com",
        },
    ]

    new_customer_code: str = ""
    new_customer_name: str = ""
    new_customer_address: str = ""
    new_customer_contact_person: str = ""
    new_customer_phone: str = ""
    new_customer_email: str = ""

    # Các hàm set_new_customer... (giữ nguyên)
    def set_new_customer_code(self, value: str):
        self.new_customer_code = value

    def set_new_customer_name(self, value: str):
        self.new_customer_name = value

    def set_new_customer_address(self, value: str):
        self.new_customer_address = value

    def set_new_customer_contact_person(self, value: str):
        self.new_customer_contact_person = value

    def set_new_customer_phone(self, value: str):
        self.new_customer_phone = value

    def set_new_customer_email(self, value: str):
        self.new_customer_email = value

    def set_search_query(self, value: str):
        self.search_query = value

    def select_customer(self, customer_id: int, checked: bool):
        """Chọn hoặc hủy chọn khách hàng. Chỉ cho phép một khách hàng được chọn."""
        if checked:
            # Tìm khách hàng theo ID
            customer = next((c for c in self.customers if c["id"] == customer_id), None)
            self.selected_customer = customer
        else:
            # Nếu bỏ chọn (chỉ xảy ra nếu nó đang được chọn), thì reset
            if self.selected_customer and self.selected_customer["id"] == customer_id:
                self.selected_customer = None

    def delete_selected_customer(self):
        """Xóa khách hàng đang được chọn (từ nút trên Selected Info)."""
        if self.selected_customer is None:
            return

        customer_id_to_delete = self.selected_customer["id"]
        self.customers = [c for c in self.customers if c["id"] != customer_id_to_delete]
        self.selected_customer = None

    def delete_customer_by_id(self, customer_id: int):
        """Xóa khách hàng dựa trên ID truyền vào (từ nút Xóa trên hàng)."""
        self.customers = [c for c in self.customers if c["id"] != customer_id]
        if self.selected_customer and self.selected_customer["id"] == customer_id:
            self.selected_customer = None

    def add_customer(self):
        """Thêm khách hàng mới và reset form."""
        if not (self.new_customer_code.strip() and self.new_customer_name.strip()):
            return

        try:
            new_id = max(c["id"] for c in self.customers) + 1
        except ValueError:
            new_id = 1

        new_customer = {
            "id": new_id,
            "code": self.new_customer_code.strip(),
            "name": self.new_customer_name.strip(),
            "address": self.new_customer_address.strip(),
            "contact_person": self.new_customer_contact_person.strip(),
            "phone": self.new_customer_phone.strip(),
            "email": self.new_customer_email.strip(),
        }
        self.customers.append(new_customer)

        # SỬA LỖI: Reset biến trạng thái phải gán chuỗi rỗng ("")
        self.new_customer_code = ""
        self.new_customer_name = ""
        self.new_customer_address = ""
        self.new_customer_contact_person = ""
        self.new_customer_phone = ""
        self.new_customer_email = ""


def customers_rows():
    CELL_STYLE = {
        "border": "0.5px solid #C1C1C1",
        "color": "black",
        "padding": "8px",
    }
    return rx.foreach(
        State.customers,
        lambda customer: rx.table.row(
            # CỘT 1: CHECKBOX (CHỌN KHÁCH HÀNG)
            rx.table.cell(
                rx.checkbox(
                    on_change=lambda checked: State.select_customer(
                        customer["id"], checked
                    ),
                    # Logic để chỉ check nếu selected_customer tồn tại và ID trùng
                    is_checked=rx.cond(
                        State.selected_customer,
                        State.selected_customer["id"] == customer["id"],
                        False,
                    ),
                ),
                style=CELL_STYLE,
            ),
            # CÁC CỘT DỮ LIỆU
            rx.table.cell(customer["code"], style=CELL_STYLE),
            rx.table.cell(customer["name"], style=CELL_STYLE),
            rx.table.cell(customer["address"], style=CELL_STYLE),
            rx.table.cell(customer["contact_person"], style=CELL_STYLE),
            rx.table.cell(customer["phone"], style=CELL_STYLE),
            rx.table.cell(customer["email"], style=CELL_STYLE),
            # CỘT CUỐI: NÚT XÓA TRỰC TIẾP (Dùng rx.window_confirm)
            rx.table.cell(
                rx.button(
                    "Xóa",
                    # Dùng rx.window_confirm để yêu cầu xác nhận trước khi gọi hàm xóa
                    on_click=State.delete_customer_by_id(customer["id"]),
                    size="1",
                    color_scheme="red",
                ),
                style=CELL_STYLE,
            ),
            key=customer["id"],
        ),
    )


def selected_customer_info() -> rx.Component:
    """Hiển thị thông tin chi tiết khách hàng đã chọn và nút xóa."""
    return rx.cond(
        State.selected_customer,
        rx.vstack(
            rx.heading("Khách hàng đang chọn", size="6", color="blue"),
            rx.box(
                rx.vstack(
                    rx.text(
                        f"Mã khách hàng: ", rx.code(State.selected_customer["code"])
                    ),
                    rx.text(
                        f"Tên khách hàng: ", rx.code(State.selected_customer["name"])
                    ),
                    rx.text(f"Địa chỉ: ", rx.code(State.selected_customer["address"])),
                    rx.text(
                        f"Người liên hệ: ",
                        rx.code(State.selected_customer["contact_person"]),
                    ),
                    rx.text(
                        f"Số điện thoại: ", rx.code(State.selected_customer["phone"])
                    ),
                    rx.text(f"Email: ", rx.code(State.selected_customer["email"])),
                    spacing="2",
                    align_items="flex-start",
                ),
                border="1px solid blue",
                padding="10px",
                border_radius="8px",
                width="100%",
            ),
            # Nút xóa dành riêng cho khách hàng đang được chọn
            rx.button(
                "Xóa khách hàng đã chọn (Checkbox)",
                # Dùng rx.window_confirm để yêu cầu xác nhận trước khi gọi hàm xóa
                on_click=State.delete_selected_customer,
                bg="red",
                color="white",
                margin_top="10px",
            ),
            width="100%",
            align_items="flex-start",
            margin_bottom="20px",
        ),
        rx.box(),
    )


def sidebar():
    # Sidebar code (giữ nguyên)
    return rx.vstack(
        rx.hstack(
            rx.spacer(), rx.icon("x", cursor="pointer"), width="100%", align="center"
        ),
        rx.image(
            src="/logo.png",
            max_width="40%",
            height="20%",
            border="2px solid none",
            boxShadow="0 0 10px rgba(255, 0, 0, 0.75)",
            marginTop="10%",
        ),
        rx.box(
            height="1px", bg="black", width="100%", marginTop="5%", marginBottom="5%"
        ),
        rx.vstack(
            rx.heading(
                rx.hstack(
                    rx.icon("house"),
                    rx.text("Tồn kho và bán hàng"),
                    spacing="2",
                    align="center",
                ),
            ),
            rx.box(height="1px", bg="black", width="100%", marginTop="2px"),
            rx.box(
                rx.hstack(
                    rx.icon("user-round-check", color="orange"),
                    rx.text("Khai báo", color="white", font_weight="bold"),
                    width="100%",
                    bg="red",
                    padding="4px",
                    border_radius="4px",
                ),
                width="100%",
            ),
            rx.box(
                rx.hstack(
                    rx.icon("package", color="orange"),
                    rx.text("Quản lí kho"),
                    width="100%",
                    bg="none",
                    padding="4px",
                    border_radius="4px",
                ),
            ),
            rx.box(
                rx.hstack(
                    rx.icon("dollar-sign", color="orange"),
                    rx.text("Bán hàng"),
                    width="100%",
                    bg="none",
                    padding="4px",
                    border_radius="4px",
                )
            ),
            rx.box(
                rx.hstack(
                    rx.icon("bar-chart", color="orange"),
                    rx.text("Báo Cáo"),
                    width="100%",
                    bg="none",
                    padding="4px",
                    border_radius="4px",
                )
            ),
            rx.box(
                rx.hstack(
                    rx.icon("users", color="orange"),
                    rx.text("Tài khoản"),
                    width="100%",
                    bg="none",
                    padding="4px",
                    border_radius="4px",
                )
            ),
            width="95%",
            spacing="2",
            border="3px solid #cac8c6",
            bg="#cac8c6",
            border_radius="4px",
            padding="8px",
            text_align="left",
        ),
        rx.vstack(
            rx.heading("Xin chào: KD Educode (kdevn)", size="5", text_align="left"),
            rx.button("Đăng xuất", bg="lightgray", color="black", border="1px solid"),
            marginTop="5%",
        ),
        width="25%",
        height="100vh",
        padding="10px",
        bg="#f0f4f8",
        color="black",
        align="center",
    )


def main_content():
    return rx.vstack(
        rx.heading("Thêm khách hàng", size="7"),
        rx.box(
            height="2px",
            bg="red",
            width="100%",
            marginTop="",
        ),
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text("Mã khách hàng", size="1"),
                    rx.input(
                        value=State.new_customer_code,
                        on_change=State.set_new_customer_code,
                        bg="whitesmoke",
                        color="black",
                    ),
                ),
                rx.vstack(
                    rx.text("Tên khách hàng", size="1"),
                    rx.input(
                        value=State.new_customer_name,
                        on_change=State.set_new_customer_name,
                        bg="whitesmoke",
                        color="black",
                    ),
                ),
                rx.vstack(
                    rx.text("Địa chỉ", size="1"),
                    rx.input(
                        value=State.new_customer_address,
                        on_change=State.set_new_customer_address,
                        bg="whitesmoke",
                        color="black",
                        width="100%",
                    ),
                ),
                rx.vstack(
                    rx.text("Người liên hệ", size="1"),
                    rx.input(
                        value=State.new_customer_contact_person,
                        on_change=State.set_new_customer_contact_person,
                        bg="whitesmoke",
                        color="black",
                        width="100%",
                    ),
                ),
                rx.vstack(
                    rx.text("SĐT", size="1"),
                    rx.input(
                        value=State.new_customer_phone,
                        on_change=State.set_new_customer_phone,
                        bg="whitesmoke",
                        color="black",
                        width="100%",
                    ),
                ),
                rx.vstack(
                    rx.text("Email", size="1"),
                    rx.input(
                        value=State.new_customer_email,
                        on_change=State.set_new_customer_email,
                        bg="whitesmoke",
                        color="black",
                        width="100%",
                    ),
                    width="20%",
                ),
                width="100%",
            ),
            rx.button(
                "Thêm khách hàng", bg="red", color="white", on_click=State.add_customer
            ),
            rx.box(marginTop="5%"),
            # Khối thông tin khách hàng đang chọn
            rx.heading("Danh sách khách hàng", size="7"),
            rx.box(
                height="2px",
                bg="red",
                width="100%",
                marginTop="",
            ),
            rx.vstack(
                rx.text("Gõ tìm kiếm và nhấn Enter", size="2"),
                rx.input(
                    # Cần thêm logic tìm kiếm tại đây
                    width="100%",
                    bg="#f1f4f9",
                    color="black",
                ),
                width="100%",
            ),
            rx.heading("Kết quả tìm kiếm", size="3"),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        *[
                            rx.table.column_header_cell(
                                h,
                                color="black",
                                border="0.5px solid #C1C1C1",
                                bg="#E4E6E7",
                            )
                            for h in HEADERS
                        ]
                    )
                ),
                rx.table.body(
                    customers_rows(),
                ),
            ),
            selected_customer_info(),
            width="100%",
            overflow_x="auto",
            margin_top="10px",
        ),
        width="100%",
        height="100vh",
        bg="white",
        color="black",
        padding="14px",
    )


def index() -> rx.Component:
    return rx.hstack(
        sidebar(),
        main_content(),
        gap="0",
        max_width="100%",
        height="100vh",
    )
