"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config

from quanly_nongsan.khach_hang import index

app = rx.App()
app.add_page(index)
