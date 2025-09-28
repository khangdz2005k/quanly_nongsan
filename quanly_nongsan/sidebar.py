import reflex as rx
from .phanloai_hanghoa_backend import State


def sidebar():
    return rx.vstack(
        # Logo
        rx.hstack(
            rx.image(src="/logo.png", width="140px", height="180px"),
            marginTop="20%",
            border="2px solid none",
            boxShadow="0 0 10px rgba(255, 0, 0, 0.75)",
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
    return rx.center(
        rx.vstack(
            rx.heading("Thêm loại hàng", size="7"),
            rx.box(
                style={
                    "height": "2px",  # Chiều cao của thanh gạch ngang
                    "backgroundColor": "blue",  # Màu của thanh gạch ngang
                    "width": "100%",  # Thanh chiếm toàn bộ chiều ngang
                    "marginTop": "3px",  # Khoảng cách từ tiêu đề đến thanh ngang
                }
            ),
            rx.hstack(
                rx.vstack(
                    rx.text("Mã loại hàng", size="2"),
                    rx.input(
                        bg="#f1f4f9",
                        color="black",
                        value=State.new_product_type_code,
                        on_change=State.set_product_type_code,
                    ),
                ),
                rx.vstack(
                    rx.text("Tên loại hàng", size="2"),
                    rx.input(
                        width="100%",
                        bg="#f1f4f9",
                        color="black",
                        value=State.new_product_type_name,
                        on_change=State.set_product_type_name,
                    ),
                    width="100%",
                ),
                width="100%",
            ),
            rx.button(
                "Thêm loại hàng",
                bg="red",
                color="white",
                on_click=State.add_product,
                cursor="pointer",
            ),
            rx.heading("Danh sách loại hàng", size="7", marginTop="3%"),
            rx.box(
                style={
                    "height": "2px",  # Chiều cao của thanh gạch ngang
                    "backgroundColor": "blue",  # Màu của thanh gạch ngang
                    "width": "100%",  # Thanh chiếm toàn bộ chiều ngang
                    "marginTop": "3px",  # Khoảng cách từ tiêu đề đến thanh ngang
                }
            ),
            rx.vstack(
                rx.text("Gõ tìm kiếm và nhấn Enter", size="2"),
                rx.input(
                    width="100%",
                    bg="#f1f4f9",
                    color="black",
                    value=State.new_product_type_code,
                    on_change=State.set_product_type_code,
                    on_key_down=State.search_on_enter,
                ),
                width="100%",
            ),
            rx.heading("Kết quả tìm kiếm", size="3"),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Select", color="black", border = "0.5px solid #C1C1C1", bg = "#E4E6E7"),
                        rx.table.column_header_cell("ID", color="black", border = "0.5px solid #C1C1C1", bg = "#E4E6E7"),
                        rx.table.column_header_cell("Mã loại hàng", color="black", border = "0.5px solid #C1C1C1", bg = "#E4E6E7"),
                        rx.table.column_header_cell("Tên loại hàng", color="black", border = "0.5px solid #C1C1C1", bg = "#E4E6E7"),
                        rx.table.column_header_cell("Thời gian tạo", color="black", border = "0.5px solid #C1C1C1", bg = "#E4E6E7"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(
                        State.products,
                        lambda item: rx.table.row(
                            rx.table.cell(rx.checkbox(), border = "0.5px solid #C1C1C1"),
                            rx.table.cell(item["id"], color="black", border = "0.5px solid #C1C1C1"),
                            rx.table.cell(item["code"], color="black", border = "0.5px solid #C1C1C1"),
                            rx.table.cell(item["name"], color="black", border = "0.5px solid #C1C1C1"),
                            rx.table.cell(
                                rx.cond(
                                    item["createdat"],  # điều kiện là Var
                                    rx.text(
                                        item["createdat"], color="black"
                                    ),  # case có giá trị
                                    rx.text(""),  # case rỗng
                                ),
                                border = "0.5px solid #C1C1C1"
                            ),
                        ),
                    ),
                ),
                border = "0.5px solid #C1C1C1",
                border_radius = "4px"
            ),
            width="100%",
            max_width="1400px",  # hoặc 800px tùy theo mong muốn
        ),
        width="100%",
        height="100vh",
        bg="white",
        color="black",
    )


def index() -> rx.Component:
    return rx.hstack(
        sidebar(),
        main_content(),
        gap="0",
        width="100%",
        height="100vh",
        on_mount=State.load_products_type,
    )
