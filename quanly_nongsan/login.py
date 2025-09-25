import reflex as rx

def index() -> rx.Component:
    return rx.center(
        rx.hstack(
            rx.vstack(
                rx.heading("Login", size= "7"),
                rx.text("Username", size="1"),
                rx.input(placeholder="username", type= "name", width = "100%", bg = "#F0F4F8"),
                rx.text("Password", size="1"),
                rx.input(placeholder="password", type= "password", width = "100%", bg = "#F0F4F8"),
                rx.button("Login", color="black", border = "2px solid #F5F5F5", bg = "white"),
                width = "100%",
                bg = "white",
                color="black",
                padding = "10px",
                border = "3px solid #F5F5F5",
                border_radius = "8px"
            ),
            width = "80%"
        ),
        bg = "white",
        width = "100%",
        height = "100vh"
    )