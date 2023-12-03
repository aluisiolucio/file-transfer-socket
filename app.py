import flet as ft

from src.client import client_socket


if __name__ == "__main__":
    def init_page(page: ft.Page):
        page.title = "Cliente"
        page.padding = 50
        page.window_max_width = 700
        page.window_max_height = 550
        page.update()

        def button_clicked(e):
            client_socket(user_input.value.lower() + pass_input.value, file_input.value)

        def update_input(e):
            file_input.value = (
                ", ".join(map(lambda f: f.path, e.files)) if e.files else "Clique no botão para selecionar o arquivo"
            )
            file_input.update()
        
        user_input = ft.TextField(label="Usuário")
        file_input = ft.TextField(read_only=True, value="Clique no botão para selecionar o arquivo")
        pass_input = ft.TextField(label="Senha", password=True, can_reveal_password=True)

        pick_files_dialog = ft.FilePicker(on_result=update_input)
        page.overlay.append(pick_files_dialog)

        page.add(
            ft.Column([user_input, pass_input, file_input]),
            ft.Row([
                    ft.ElevatedButton(
                        "Selecione o arquivo",
                        icon=ft.icons.UPLOAD_FILE,
                        on_click=lambda _: pick_files_dialog.pick_files(
                            allow_multiple=True
                        ),
                    ),
                    ft.IconButton(
                        icon=ft.icons.DELETE_FOREVER_ROUNDED,
                        icon_color="pink600",
                        icon_size=40,
                        tooltip="Remover arquivo"
                    ),
                ]),
            ft.ElevatedButton(text="Enviar", on_click=button_clicked)
        )
    
    ft.app(target=init_page)