import reflex as rx
from .change_password_ui import index as change_password_page


app = rx.App()
app.add_page(change_password_page, route = "/")
