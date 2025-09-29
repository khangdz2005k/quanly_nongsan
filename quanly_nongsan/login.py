import reflex as rx
from .state import State


def index() -> rx.Component:
    return rx.center(
        rx.hstack(
            rx.vstack(
                rx.heading("Login", size="7"),
                rx.text("Username", size="1"),
                rx.input(
                    placeholder="username",
                    type="name",
                    width="100%",
                    bg="#F0F4F8",
                    value=State.username,
                    on_change=State.set_username,
                    color="black",
                    style={"input::placeholder": {"color": "#ccc"}},
                ),
                rx.text("Password", size="1"),
                rx.input(
                    placeholder="password",
                    type="password",
                    width="100%",
                    bg="#F0F4F8",
                    value=State.password,
                    on_change=State.set_password,
                    style={"input::placeholder": {"color": "#ccc"}},
                    color="black",
                ),
                rx.button(
                    "Login",
                    color="black",
                    border="2px solid #F5F5F5",
                    bg="white",
                    on_click=State.handle_login,
                    cursor="pointer",
                ),
                rx.text(State.error_message, color="red"),
                width="100%",
                bg="white",
                color="black",
                padding="10px",
                border="3px solid #F5F5F5",
                border_radius="8px",
            ),
            width="80%",
        ),
        bg="white",
        width="100%",
        height="100vh",
    )
