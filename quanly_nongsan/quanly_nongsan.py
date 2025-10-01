import reflex as rx
from .danhmuc_sanpham import index as product_category
from rxconfig import config

from quanly_nongsan.danhmuc_sanpham import index

app = rx.App()
app.add_page(product_category, route="/")

