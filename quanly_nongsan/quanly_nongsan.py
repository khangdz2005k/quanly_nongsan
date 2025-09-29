import reflex as rx
from .sidebar import index

app = rx.App()
app.add_page(index, route='/')
