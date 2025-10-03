import reflex as rx

data = [
    {
        "id": 1,
        "ma_hh": "SP001",
        "ten_hh": "Xe đạp",
        "loai": "Phương tiện",
        "hinh": "🚲",
    },
    {"id": 2, "ma_hh": "SP002", "ten_hh": "Laptop", "loai": "Điện tử", "hinh": "💻"},
    {"id": 3, "ma_hh": "SP003", "ten_hh": "Bàn học", "loai": "Nội thất", "hinh": "🪑"},
]

headers = ["Select", "ID", "Mã hàng hóa", "Tên hàng hóa", "Loại hàng", "Hình ảnh"]

keys = ["id", "ma_hh", "ten_hh", "loai", "hinh"]


def sidebar():
    return rx.vstack(
        # Logo
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
        # marginTop="10%",
        # width = "100%"
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
        # rx.spacer(),
        # User info
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
        rx.center(
            rx.hstack(
                rx.button(
                    "Phân loại hàng hóa",
                    bg="whitesmoke",
                    color="black",
                    padding="12px",
                    cursor="pointer",
                ),
                rx.button(
                    "Danh mục hàng hóa",
                    bg="red",
                    color="white",
                    padding="12px",
                    cursor="pointer",
                ),
                rx.button(
                    "Danh sách khách hàng",
                    bg="whitesmoke",
                    color="black",
                    padding="12px",
                    cursor="pointer",
                ),
                rx.button(
                    "Quản lý hình ảnh",
                    bg="whitesmoke",
                    color="black",
                    padding="12px",
                    cursor="pointer",
                ),
                spacing="0",
            ),
            width="100%",
            marginBottom="2%",
        ),
        rx.heading("Thêm hàng hóa", size="7"),
        rx.box(
            height="2px",
            bg="red",
            width="100%",
            marginTop="",
        ),
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text("Chọn loại hàng (*)", size="1"),
                    rx.select(
                        [
                            "Điện thoại",
                            "Máy tính",
                            "Tivi",
                            "Tủ lạnh",
                            " ",
                        ],  # danh sách lựa chọn
                        placeholder="-- Chọn loại hàng --",  # hint ban đầu
                        width="100%",
                        bg="black",
                        color="#F0F4F8",
                    ),
                ),
                rx.vstack(
                    rx.text("Mã hàng hóa", size="1"),
                    rx.input("", bg="whitesmoke", color="black"),
                ),
                rx.vstack(
                    rx.text("Tên hàng hóa", size="1"),
                    rx.input("", bg="whitesmoke", color="black", width="100%"),
                    width="20%",
                ),
                rx.vstack(
                    rx.text("Ngày hết hạn", size="1"),
                    rx.input("", bg="whitesmoke", color="black", width="100%"),
                    width="20%",
                ),
                rx.vstack(
                    rx.text("Ghi chú", size="1"),
                    rx.input("", bg="whitesmoke", color="black", width="100%"),
                    width="20%",
                ),
                width="100%",
            ),
            rx.vstack(
                rx.text("Ảnh sản phẩm", size="1"),
            ),
            rx.upload(
                rx.hstack(
                    rx.icon("upload", size=30),
                    rx.vstack(
                        rx.text("Drag and drop file here"),
                        rx.text("Limit 200MB per file . PNG, JPG, JPEG"),
                        align="start",
                    ),
                    rx.button("Browse files"),
                    justify="between",
                ),
                padding="12px",
                width="100%",
                border="0.5px solid whitesmoke",
                border_radius="12px",
                bg="whitesmoke",
            ),
            rx.button("Thêm loại hàng", bg="red", color="white"),
            rx.heading("Danh mục hàng hóa", size="7"),
            rx.box(
                height="2px",
                bg="red",
                width="100%",
                marginTop="",
            ),
            rx.vstack(
                rx.text("Gõ tìm kiếm và nhấn Enter", size="2"),
                rx.input(
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
                            for h in headers
                        ]
                    )
                ),
                rx.table.body(
                    *[
                        rx.table.row(
                            rx.table.cell(
                                rx.checkbox(),
                                border="0.5px solid #C1C1C1",
                            ),  # Select column
                            *[
                                rx.table.cell(
                                    str(item[k]),
                                    color="black",
                                    border="0.5px solid #C1C1C1",
                                )  # Data columns
                                for k in keys
                            ]
                        )
                        for item in data
                    ]
                ),
            ),
            width="100%",
        ),
        width="100%",
        height="100vh",
        bg="white",
        color="black",
        padding="14px",
        overflow_y="auto",
    )


def index() -> rx.Component:
    return rx.hstack(
        sidebar(),
        main_content(),
        gap="0",
        width="100%",
        height="100vh",
        # on_mount=State.load_products_type,
    )
