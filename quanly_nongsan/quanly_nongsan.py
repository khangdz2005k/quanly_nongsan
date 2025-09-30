"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config


# from quanly_nongsan.login import index
# from quanly_nongsan.sidebar import index
# from quanly_nongsan.phanloaihanghoa import index
from quanly_nongsan.danhmuc_sanpham import index

app = rx.App()
app.add_page(index)
