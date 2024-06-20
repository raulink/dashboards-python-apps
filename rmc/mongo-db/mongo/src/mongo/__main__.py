import flet as ft

import requests

def main(page:ft.Page):
    
    def registrar_usuario(e):
        user_data = {
            "name": name_field.value,
            "email": email_field.value,
            "password": password_field.value
        }
        
        response = requests.post("http://192.168.0.5:8000/api/users/",json=user_data)
        if response.status_code == 200:
            dialog.content = ft.Text("User registered successfully!")   
        else:
            dialog.content = ft.Text("Failed to register user.")
        page.dialog = dialog
        dialog.open = True
        page.update()
                    
        
    page.title = "Registro de usuarios"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    name_field = ft.TextField(label="Nombre")
    email_field = ft.TextField(label="Correo")
    password_field = ft.TextField(label="Contraseña",password=True)

    def handle_close(e):
        #page.close(dialog)
        page.close_dialog()
        page.add(ft.Text(f"Modal dialog closed with action: {e.control.text}"))


    dialog = ft.AlertDialog(
        modal=True,        
        title=ft.Text("Registration Result"),
        content=ft.Text(""),
        actions=[            ft.TextButton("Yes", on_click=handle_close)],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        #on_dismiss=lambda e: page.add(ft.Text("Se salio de cuadro"))

    )

    register_button= ft.ElevatedButton("Registrar", on_click=registrar_usuario)

    page.add(name_field,email_field,password_field,register_button)

ft.app(target=main)