import flet as ft

from client import client_socket


if __name__ == "__main__":
    def init_page(page: ft.Page):
        page.title = "Cliente"
        page.padding = 50
        page.window_max_width = 700
        page.window_max_height = 550
        page.update()

        def button_clicked(e):            
            msg = client_socket(user_input.value.lower() + pass_input.value, file_input.value)
            
            open_dlg(e, msg)
            
            file_input.value = "..."
            file_input.update()

            submit_button.disabled = True
            submit_button.update()

        def update_input(e):
            file_input.value = (
                ", ".join(map(lambda f: f.path, e.files)) if e.files else "..."
            )
            file_input.update()
            
            if user_input.value and pass_input.value and file_input.value != "...":
                submit_button.disabled = False
                submit_button.update()
        
        def button_clicked_remove(e):
            file_input.value = "..."
            file_input.update()
            
            submit_button.disabled = True
            submit_button.update()

        def open_dlg(e, msg):
            dlg.title = ft.Text(msg, size=20, text_align="center")
            page.dialog = dlg
            dlg.open = True
            page.update()

        dlg = ft.AlertDialog(on_dismiss=lambda e: print("Dialog descartado!"))
    
        user_input = ft.TextField(label="Usuário")
        file_input = ft.TextField(read_only=True, value="...")
        pass_input = ft.TextField(label="Senha", password=True, can_reveal_password=True)
        submit_button = ft.ElevatedButton(text="Enviar", on_click=button_clicked, disabled=True)

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
                        tooltip="Remover arquivo",
                        on_click=button_clicked_remove
                    ),
                ]),
            submit_button
        )
    
    ft.app(target=init_page)
