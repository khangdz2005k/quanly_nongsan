import reflex as rx
from .images_ui import image_page as image_management_page

app = rx.App()
app.add_page(image_management_page, route="/")
