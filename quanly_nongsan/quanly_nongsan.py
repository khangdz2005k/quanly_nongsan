import reflex as rx
from .danhmuc_sanpham import index as product_category_page
from .sidebar import index as product_types_page
from rxconfig import config


app = rx.App()
app.add_page(product_types_page, route="/")
app.add_page(product_category_page, route="/product_category")