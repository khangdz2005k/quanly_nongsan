import reflex as rx
from .login_backend import State
from .sidebar_ui import sidebar

def main_content() -> rx.Component:
    ...

def index() -> rx.Component:
    return rx.hstack(
        sidebar(),
        main_content()
    )