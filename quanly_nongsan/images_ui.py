import reflex as rx
from .images_backend import ImageState


# --- Component Sidebar ---
def sidebar():
    return rx.vstack(
        rx.hstack(
            rx.spacer(), rx.icon("x", cursor="pointer"), width="100%", align="center"
        ),
        rx.image(
            src="/logo.png",
            max_width="40%",
            height="20%",
            border="2px solid none",
            boxShadow="0 0 10px rgba(255, 0, 0, 0.75)",
            marginTop="10%",
        ),
        rx.box(
            height="1px", bg="black", width="100%", marginTop="5%", marginBottom="5%"
        ),
        rx.vstack(
            rx.heading(
                rx.hstack(
                    rx.icon("house"),
                    rx.text("Tồn kho và bán hàng"),
                    spacing="2",
                    align="center",
                ),
            ),
            rx.box(height="1px", bg="black", width="100%", marginTop="2px"),
            rx.box(
                rx.hstack(
                    rx.icon("user-round-check", color="orange"),
                    rx.text("Khai báo", color="white", font_weight="bold"),
                    width="100%",
                    bg="red",
                    padding="4px",
                    border_radius="4px",
                ),
                width="100%",
            ),
            rx.box(
                rx.hstack(
                    rx.icon("package", color="orange"),
                    rx.text("Quản lí kho"),
                    width="100%",
                    bg="none",
                    padding="4px",
                    border_radius="4px",
                ),
            ),
            rx.box(
                rx.hstack(
                    rx.icon("dollar-sign", color="orange"),
                    rx.text("Bán hàng"),
                    width="100%",
                    bg="none",
                    padding="4px",
                    border_radius="4px",
                )
            ),
            rx.box(
                rx.hstack(
                    rx.icon("bar-chart", color="orange"),
                    rx.text("Báo Cáo"),
                    width="100%",
                    bg="none",
                    padding="4px",
                    border_radius="4px",
                )
            ),
            rx.box(
                rx.hstack(
                    rx.icon("users", color="orange"),
                    rx.text("Tài khoản"),
                    width="100%",
                    bg="none",
                    padding="4px",
                    border_radius="4px",
                )
            ),
            width="95%",
            spacing="2",
            border="3px solid #cac8c6",
            bg="#cac8c6",
            border_radius="4px",
            padding="8px",
            text_align="left",
        ),
        rx.vstack(
            rx.heading("Xin chào: KD Educode (kdevn)", size="5", text_align="left"),
            rx.button("Đăng xuất", bg="lightgray", color="black", border="1px solid"),
            marginTop="5%",
        ),
        width="25%",
        height="100vh",
        padding="10px",
        bg="#f0f4f8",
        color="black",
        align="center",
    )


# --- Nội dung chính ---
def main_content() -> rx.Component:
    return rx.vstack(
        # Tiêu đề trang và form thêm ảnh
        rx.center(
            rx.hstack(
                rx.button(
                    "Phân loại hàng hóa",
                    bg="whitesmoke",
                    color="black",
                    padding="12px",
                    cursor="pointer",
                ),
                rx.button(
                    "Danh mục hàng hóa",
                    bg="whitesmoke",
                    color="black",
                    padding="12px",
                    cursor="pointer",
                ),
                rx.button(
                    "Danh sách khách hàng",
                    bg="whitesmoke",
                    color="black",
                    padding="12px",
                    cursor="pointer",
                ),
                rx.button(
                    "Quản lý hình ảnh",
                    bg="red",
                    color="white",
                    padding="12px",
                    cursor="pointer",
                ),
                spacing="0",
            ),
            width="100%",
            marginBottom="2%",
        ),
        rx.heading("Thêm ảnh", size="7"),
        rx.divider(border_color="rainbow"),
        rx.vstack(
            rx.text("Ảnh sản phẩm", align_self="flex-start", margin_bottom="-10px"),
            rx.upload(
                rx.hstack(
                    rx.icon("cloud_upload"),
                    rx.vstack(
                        rx.text("Drag and drop file here"),
                        rx.text("Limit 200MB per file • PNG, JPG, JPEG", size="2"),
                        align="start",
                        spacing="1",
                    ),
                    rx.spacer(),
                    rx.button("Browse files", cursor="pointer", bg="#FF0000"),
                    align="center",
                    width="100%",
                ),
                border="1px solid whitesmoke",
                bg="whitesmoke",
                border_radius="12px",
                padding="1.5em",
                width="100%",
                on_drop=ImageState.handle_upload(rx.upload_files()),
            ),
            rx.cond(
                ImageState.uploaded_image_preview != "",
                rx.image(
                    src=ImageState.uploaded_image_preview,
                    height="5em",
                    margin_top="10px",
                ),
            ),
            width="100%",
        ),
        rx.vstack(
            rx.text("Đặt tên ảnh", align_self="flex-start", margin_bottom="-10px"),
            rx.input(
                placeholder="Nhập tên file bạn muốn đặt (ví dụ: hinh-san-pham-moi)",
                value=ImageState.new_image_filename,
                on_change=ImageState.set_new_image_filename,
                width="100%",
                bg="whitesmoke",
                border="1px solid whitesmoke",
                style={"input::placeholder": {"color": "#ccc"}},
            ),
            width="100%",
        ),
        rx.button(
            "Thêm ảnh",
            on_click=ImageState.add_image,
            width="150px",
            align_self="flex-end",
            margin_top="1em",
            bg="#FF0000",
            cursor="pointer",
        ),
        # Phần thư viện ảnh, tìm kiếm và xóa
        rx.heading("Thư viện ảnh", size="5", margin_top="2em"),
        rx.divider(border_color="rainbow"),
        rx.hstack(
            rx.input(
                placeholder="Tìm ảnh theo đường dẫn (URL) và nhấn Enter...",
                value=ImageState.image_search_query,
                on_change=ImageState.set_image_search_query,
                on_key_down=ImageState.search_images_on_enter,
                width="100%",
                bg="whitesmoke",
                style={"input::placeholder": {"color": "#ccc"}},
            ),
            rx.cond(
                ImageState.selected_image,
                rx.button(
                    "Xóa ảnh đã chọn",
                    on_click=ImageState.delete_image,
                    color_scheme="red",
                ),
            ),
            spacing="4",
            width="100%",
            padding_y="1em",
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell(
                        "Chọn", color="black", border="1px solid #C1C1C1"
                    ),
                    rx.table.column_header_cell(
                        "STT", color="black", border="1px solid #C1C1C1"
                    ),
                    rx.table.column_header_cell(
                        "Ảnh", color="black", border="1px solid #C1C1C1"
                    ),
                    rx.table.column_header_cell(
                        "Đường dẫn", color="black", border="1px solid #C1C1C1"
                    ),
                    rx.table.column_header_cell(
                        "Mô tả (Alt Text)", color="black", border="1px solid #C1C1C1"
                    ),
                    rx.table.column_header_cell(
                        "Ngày tạo", color="black", border="1px solid #C1C1C1"
                    ),
                )
            ),
            rx.table.body(
                rx.foreach(
                    ImageState.images,
                    lambda image: rx.table.row(
                        rx.table.cell(
                            rx.checkbox(
                                checked=(
                                    ImageState.selected_image.is_not_none()
                                    & (ImageState.selected_image["stt"] == image["stt"])
                                ),
                                on_change=lambda checked: ImageState.handle_image_selection(
                                    checked, image
                                ),
                            ),
                            border="1px solid #C1C1C1",
                        ),
                        rx.table.cell(
                            image["stt"], color="black", border="1px solid #C1C1C1"
                        ),
                        rx.table.cell(
                            rx.image(src=image["image_url"], height="3em"),
                            border="1px solid #C1C1C1",
                        ),
                        rx.table.cell(
                            rx.code(image["image_url"], color="black"),
                            border="1px solid #C1C1C1",
                        ),
                        rx.table.cell(
                            image["alt_text"], color="black", border="1px solid #C1C1C1"
                        ),
                        rx.table.cell(
                            image["created_at"],
                            color="black",
                            border="1px solid #C1C1C1",
                        ),
                        bg=rx.cond(
                            ImageState.selected_image.is_not_none()
                            & (ImageState.selected_image["stt"] == image["stt"]),
                            "var(--accent-2)",
                            "transparent",
                        ),
                    ),
                )
            ),
            variant="surface",
            width="100%",
        ),
        # Style chung cho khu vực nội dung
        width="100%",
        height="100vh",
        bg="white",
        color="black",
        padding="2em",
        spacing="5",
        align="start",
        overflow_y="auto",
    )


# --- Trang Hoàn Chỉnh ---
def image_page() -> rx.Component:
    return rx.hstack(
        sidebar(),
        main_content(),
        gap="0",
        width="100%",
        height="100vh",
        on_mount=ImageState.load_images,
    )
