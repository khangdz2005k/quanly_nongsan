import reflex as rx
from .danhmuc_sanpham import index as product_category_page
from .sidebar import index as product_types_page
from .customer_ui import index as customer

app = rx.App()
app.add_page(product_types_page, route="/")
app.add_page(customer, route="/customer")
app.add_page(product_category_page, route="/product_category")