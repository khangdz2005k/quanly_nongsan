import reflex as rx
from ..states.login_backend import State
from .sidebar_ui import sidebar


def main_content() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.center(
                rx.button("Password", bg="red", color="white", cursor="pointer"),
                width="100%",
            ),
            rx.vstack(
                rx.heading(
                    "Password",
                ),
                rx.text("Mật khẩu cũ", size="1"),
                rx.input(
                    value=State.old_password,
                    on_change=State.set_old_password,
                    width="100%",
                    bg="#F0F4F8",
                    color="black",
                    type="password",
                    style={"input::placeholder": {"color": "#ccc"}},
                ),
                rx.text("Mật khẩu mới", size="1"),
                rx.input(
                    value=State.new_password,
                    on_change=State.set_new_password,
                    width="100%",
                    bg="#F0F4F8",
                    color="black",
                    type="password",
                    style={"input::placeholder": {"color": "#ccc"}},
                ),
                rx.text("Xác nhận mật khẩu mới", size="1"),
                rx.input(
                    value=State.confirm_new_password,
                    on_change=State.set_confirm_new_password,
                    width="100%",
                    bg="#F0F4F8",
                    color="black",
                    type="password",
                    style={"input::placeholder": {"color": "#ccc"}},
                ),
                rx.button(
                    "Đổi mật khẩu",
                    on_click=State.change_password,
                    bg="red",
                    color="white",
                    cursor="pointer",
                ),
                width="100%",
            ),
            width="100%",
            padding="18px",
        ),
        width="100%",
        bg="white",
        color="black",
        height="100vh",
    )


def index() -> rx.Component:
    return rx.hstack(sidebar(), main_content(), gap="0")
