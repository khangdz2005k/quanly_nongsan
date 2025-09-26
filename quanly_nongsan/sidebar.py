import reflex as rx

import reflex as rx


def sidebar():
    return rx.vstack(
        # Logo
        rx.center(
            rx.image(src="/logo.png", width="120px"),
        ),
        # Heading
        # Menu buttons
        rx.vstack(
            rx.heading(
                rx.hstack(
                    rx.icon("house"),
                    rx.text("Tồn kho và bán hàng"),
                    spacing="2",
                    align="center",
                ),
                size="3",
            ),
            rx.button("Khai báo", rx.icon("user-round-check"), width = "100%", bg = "red"),
            rx.button(
                "Quản lí kho", rx.icon("package"), width = "100%", bg = "none"
            ),  # "warehouse" có thể lỗi, đổi "package"
            rx.button("Bán hàng", rx.icon("dollar-sign"), width = "100%", bg = "none"),
            rx.button("Báo Cáo", rx.icon("bar-chart"), width = "100%", bg = "none"),
            rx.button("Tài khoản", rx.icon("users"), width = "100%", bg = "none"),
            width="95%",
            spacing="2",
            border="3px solid #cac8c6",
            bg="#cac8c6",
            border_radius = "4px",
            padding = "8px",
            text_align = "left"
        ),
        rx.spacer(),
        # User info
        rx.heading("Xin chào: KD Educode (kdevn)", size="2"),
        rx.button("Đăng xuất"),
        width="22%",
        height="100vh",
        padding="10px",
        bg="#f0f4f8",
        color="black",
        align="center",
    )


def main_content():
    return rx.vstack(
        rx.heading("Thêm loại hàng", size="4"),
        rx.hstack(
            rx.vstack(
                rx.text("Mã loại hàng"),
                rx.input(placeholder="Nhập mã loại hàng"),
            ),
            rx.vstack(
                rx.text("Tên loại hàng"),
                rx.input(placeholder="Nhập tên loại hàng"),
            ),
            spacing="4",
        ),
        rx.button("Thêm loại hàng", bg="red", color="white"),
        spacing="4",
        width="80%",
        padding="20px",
    )


def index() -> rx.Component:
    return rx.hstack(
        sidebar(),
        main_content(),
        width="100%",
        height="100vh",
    )