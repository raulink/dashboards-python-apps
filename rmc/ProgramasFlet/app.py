import flet as ft

def main(page: ft.Page):
    page.title = "Flet Dashboard"

    # Variable de estado para controlar la visibilidad del NavigationRail
    navigation_visible = ft.Ref[bool]
    
    # Función para alternar la visibilidad del NavigationRail
    def toggle_navigation(e):
        navigation_visible.current = not navigation_visible.current
        update_content()

    # Función para actualizar el contenido de la página
    def update_content():
        page.controls.clear()
        page.add(
            ft.Row(
                [
                    ft.IconButton(
                        icon=ft.icons.MENU,
                        on_click=toggle_navigation
                    ),
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        [
                            ft.Text("Body")
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        expand=True
                    )
                ] if not navigation_visible.current else
                [
                    barra(),
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        [
                            ft.IconButton(
                                icon=ft.icons.MENU,
                                on_click=toggle_navigation
                            ),
                            ft.Text("Body")
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        expand=True
                    )
                ],
                width=400,
                height=400
            )
        )
        page.update()

    # Llamar la función de actualización al inicio
    update_content()

# Definición de la barra de navegación
def barra():
    return ft.NavigationRail(
        selected_index=0,
        min_width=100,
        min_extended_width=400,
        #leading=ft.FloatingActionButton(icon=ft.icons.CREATE, text="Añadir"),
        group_alignment=-0.9,
        extended=False,
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.FAVORITE_BORDER, selected_icon=ft.icons.FAVORITE, label="Dashboards"),
            ft.NavigationRailDestination(icon=ft.icons.BOOKMARK_BORDER, selected_icon=ft.icons.BOOKMARK, label="Etiquetas"),
            ft.NavigationRailDestination(icon=ft.icons.SETTINGS_OUTLINED, selected_icon=ft.icons.SETTINGS, label="Configuración"),
        ],
        on_change=lambda e: print("Seleccionado", e.control.selected_index)
    )

if __name__ == "__main__":
    ft.app(target=main)
