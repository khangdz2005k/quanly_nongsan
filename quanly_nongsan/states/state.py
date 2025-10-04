# state.py
import reflex as rx
from .product_types_backend import State as productState
from .product_category_backend import State as productState2
from .customer_backend import UserState as UserState
from .images_backend import ImageState as ImageState
from .login_backend import State as LoginState

class State(rx.State):
    productState = productState
    productState2 = productState2
    UserState = UserState
    ImageState = ImageState
    LoginState = LoginState