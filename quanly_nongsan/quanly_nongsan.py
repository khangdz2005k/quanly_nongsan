import reflex as rx
from .login import index as login_page
from .sidebar import index as manage_product_types

app = rx.App()
app.add_page(login_page, route="/")
app.add_page(manage_product_types, route='/manage_product_types')
