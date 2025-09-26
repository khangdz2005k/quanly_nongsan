import reflex as rx

def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Thêm loại hàng"),
            rx.hstack(
                rx.vstack(
                    rx.text("Mã loại hàng"),
                    rx.input(""),
                ),
                rx.vstack(
                    rx.text("Tên loại hàng"),
                    rx.input(""),
                ),
            ),
            rx.button("Thêm loại hàng")
        )
    )