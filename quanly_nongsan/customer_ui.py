import reflex as rx
from .state import State

# THÊM CỘT "Hành động" cho nút Xóa
HEADERS = [
    "Select",
    "ID",
    "Username",
    "Tên khách hàng",
    "Vai trò",
    "Số điện thoại",
    "Địa chỉ",
]


def customers_rows():
    CELL_STYLE = {
        "border": "0.5px solid #C1C1C1",
        "color": "black",
        "padding": "8px",
    }

    SELECTED_ROW_STYLE = {
        "border": "0.5px solid #C1C1C1",
        "color": "black",
        "padding": "8px",
    }

    # Biến điều kiện kiểm tra ID hiện tại có khớp với ID đang chọn hay không.
    # Ta dùng rx.State.get() để truy cập an toàn vào dictionary.
    is_selected = lambda user: rx.cond(
        State.UserState.selected_user,
        # Nếu có user đang chọn, kiểm tra ID
        State.UserState.selected_user["id"] == user["id"],
        # Nếu không có user nào được chọn (None), trả về False
        False,
    )

    return rx.table.root(
        rx.table.header(
            rx.table.row(
                *[rx.table.column_header_cell(h, style=CELL_STYLE) for h in HEADERS],
            ),
        ),
        rx.table.body(
            rx.foreach(
                State.UserState.users,
                lambda user: rx.table.row(
                    rx.table.cell(
                        rx.checkbox(
                            checked=(
                                State.UserState.selected_user.is_not_none()
                                & (State.UserState.selected_user["id"] == user["id"])
                            ),
                            on_change=lambda checked: State.UserState.handle_user_selection(
                                checked, user
                            ),
                            cursor="pointer",
                        ),
                        style=SELECTED_ROW_STYLE,
                    ),
                    rx.table.cell(user["id"], style=CELL_STYLE),
                    rx.table.cell(user["username"], style=CELL_STYLE),
                    rx.table.cell(user["full_name"], style=CELL_STYLE),
                    rx.table.cell(user["role"], style=CELL_STYLE),
                    rx.table.cell(user["phone_number"], style=CELL_STYLE),
                    rx.table.cell(user["address"], style=CELL_STYLE),
                ),
            )
        ),
    )


def edit_delete_form():
    """Tạo form chỉnh sửa và các nút hành động, mô phỏng chính xác cấu trúc bảng."""

    # Định nghĩa lại các style bạn đã cung cấp trong customers_rows()
    CELL_STYLE = {
        "border": "0.5px solid #C1C1C1",
        "color": "black",
        "padding": "8px",
    }

    # Định nghĩa lại HEADERS (cần thiết cho Header của form)
    # Giả định HEADERS của bạn là: ["Select", "ID", "Username", "Tên khách hàng", "Vai trò", "Số điện thoại", "Địa chỉ"]
    HEADERS_FOR_DISPLAY = [
        "ID",
        "Username",
        "Tên khách hàng",
        "Vai trò",
        "Số điện thoại",
        "Địa chỉ",
    ]

    return rx.cond(
        State.UserState.selected_user,
        rx.vstack(  # Khối vstack chứa toàn bộ Form và Nút
            rx.heading(
                f"Thông tin khách hàng đang chọn: {State.UserState.selected_user.full_name}",
                size="5",
                color="black",
                margin_bottom="15px",
            ),
            # 1. BẢNG MÔ PHỎNG (Form chính)
            rx.table.root(
                # Header (Cần thiết để căn chỉnh cột)
                rx.table.header(
                    rx.table.row(
                        *[
                            rx.table.column_header_cell(h, style=CELL_STYLE)
                            for h in HEADERS_FOR_DISPLAY
                        ],
                    ),
                ),
                # Body (Chỉ có một hàng dữ liệu đang được chọn)
                rx.table.body(
                    rx.table.row(
                        # Cột 2-4: Dữ liệu cố định
                        rx.table.cell(
                            State.UserState.selected_user.id, style=CELL_STYLE
                        ),
                        rx.table.cell(
                            State.UserState.selected_user.username, style=CELL_STYLE
                        ),
                        rx.table.cell(
                            State.UserState.selected_user.full_name, style=CELL_STYLE
                        ),
                        rx.table.cell(
                            State.UserState.selected_user.role, style=CELL_STYLE
                        ),
                        # Cột 5: SĐT (Dữ liệu chỉnh sửa - Input)
                        rx.table.cell(
                            rx.input(
                                value=State.UserState.edited_phone_number,
                                on_change=State.UserState.set_edited_phone_number,
                                size="1",
                                width="100%",
                                bg="transparent",
                                color="black",
                            ),
                            style=CELL_STYLE,
                        ),
                        rx.table.cell(
                            rx.input(
                                value=State.UserState.edited_address,
                                on_change=State.UserState.set_edited_address,
                                size="1",
                                width="100%",
                                bg="transparent",
                                color="black",
                            ),
                            style=CELL_STYLE,
                        ),
                    ),
                ),
                width="100%",
                style={"border_collapse": "collapse", "border": "1px solid #C1C1C1"},
            ),
            # 2. KHỐI NÚT HÀNH ĐỘNG
            rx.hstack(
                rx.button(
                    rx.hstack(rx.icon("save"), rx.text("Cập nhật")),
                    on_click=State.UserState.update_user,
                    color_scheme="green",
                    size="2",
                    cursor="pointer",
                ),
                rx.button(
                    rx.hstack(rx.icon("trash-2"), rx.text("Xóa")),
                    on_click=State.UserState.delete_user,
                    color_scheme="red",
                    size="2",
                    cursor="pointer",
                ),
                margin_top="15px",
            ),
            width="100%",
            align_items="start",
            margin_y="20px",
        ),
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
        rx.center(
            rx.hstack(
                rx.button(
                    "Phân loại hàng hóa",
                    bg="whitesmoke",
                    color="black",
                    padding="12px",
                    cursor="pointer",
                    on_click=rx.redirect("/"),
                ),
                rx.button(
                    "Danh mục hàng hóa",
                    bg="whitesmoke",
                    color="black",
                    padding="12px",
                    cursor="pointer",
                    on_click=rx.redirect("/product_category"),
                ),
                rx.button(
                    "Danh sách khách hàng",
                    bg="red",
                    color="white",
                    padding="12px",
                    cursor="pointer",
                    on_click=rx.redirect("/customer"),
                ),
                rx.button(
                    "Quản lý hình ảnh",
                    bg="whitesmoke",
                    color="black",
                    padding="12px",
                    cursor="pointer",
                    on_click=rx.redirect("/image_page"),
                ),
                spacing="0",
            ),
            width="100%",
            marginBottom="2%",
        ),
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
                    rx.text("Tên khách hàng", size="1"),
                    rx.input(
                        value=State.UserState.new_user_full_name,
                        on_change=State.UserState.set_new_user_full_name,
                        bg="whitesmoke",
                        color="black",
                    ),
                ),
                rx.vstack(
                    rx.text("Địa chỉ", size="1"),
                    rx.input(
                        value=State.UserState.new_user_address,
                        on_change=State.UserState.set_new_user_address,
                        bg="whitesmoke",
                        color="black",
                        width="100%",
                    ),
                ),
                rx.vstack(
                    rx.text("SĐT", size="1"),
                    rx.input(
                        value=State.UserState.new_user_phone_number,
                        on_change=State.UserState.set_new_user_phone_number,
                        bg="whitesmoke",
                        color="black",
                        width="100%",
                    ),
                ),
                width="100%",
            ),
            rx.button(
                "Thêm khách hàng",
                bg="red",
                color="white",
                cursor="pointer",
                on_click=State.UserState.add_user,
            ),
            rx.box(marginTop="2%"),
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
                    value=State.UserState.search_query,
                    on_change=State.UserState.set_search_query,
                    on_key_down=State.UserState.search_on_enter,
                    width="100%",
                    bg="#f1f4f9",
                    color="black",
                ),
                width="100%",
            ),
            rx.heading("Kết quả tìm kiếm", size="3"),
            rx.box(
                customers_rows(),
                edit_delete_form(),  # Gọi trực tiếp hàm trả về bảng
                width="100%",
                overflow_x="auto",
                margin_top="10px",
            ),
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
        on_mount=State.UserState.load_users,
        gap="0",
        max_width="100%",
        height="100vh",
    )
