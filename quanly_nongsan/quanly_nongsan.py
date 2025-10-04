import reflex as rx


class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container()


app = rx.App()
app.add_page(index)
