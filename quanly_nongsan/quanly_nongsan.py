import reflex as rx
from .components.change_password_ui import index as change_password_page
from .components.login_ui import index as login_page


app = rx.App()
app.add_page(login_page, route = "/")
app.add_page(login_page, route = "/login_page")
app.add_page(change_password_page, route = "/change_password")
