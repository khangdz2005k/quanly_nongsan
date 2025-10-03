import reflex as rx
from .danhmuc_sanpham import index as product_category_page
from rxconfig import config


app = rx.App()
app.add_page(product_category_page, route="/")