import flet as ft
from guest_manager import GuestList, Guest, Table


def main(page: ft.Page):
    page.title = "Planer stołów"

    # Załaduj listę gości
    gl = GuestList()
    gl.load_list("lista_gosci.txt")

    # lista stołów
    tables_list: list[Table] = []
    table_widgets: list[ft.Control] = []

    def update_tables_ui():
        table_column.controls = [table_controls] + table_widgets
        page.update()

    def on_create_round_table_click(e):
        new_table = Table(type="round")
        tables_list.append(new_table)

        table_widget = ft.Container(
            content=ft.Text(
                f"Stół {new_table.table_id}\n(okrągły)\n{new_table.free_seats} wolnych miejsc",
                text_align=ft.TextAlign.CENTER,
            ),
            padding=10,
            border=ft.border.all(1),
            width=150,
            height=150,
            border_radius=75,
        )
        table_widgets.append(table_widget)
        update_tables_ui()

    def on_create_square_table_click(e):
        new_table = Table(type="square")
        tables_list.append(new_table)

        table_widget = ft.Container(
            content=ft.Text(
                f"Stół {new_table.table_id}\n(prostokątny)\n{new_table.free_seats} wolnych miejsc",
                text_align=ft.TextAlign.CENTER,
            ),
            width=150,
            height=100,
            padding=10,
            border=ft.border.all(1),
        )
        table_widgets.append(table_widget)
        update_tables_ui()

    def on_delete_table_click(e):
        pass

    # Funkcja do obsługi kliknięcia gościa
    def on_guest_click(e):
        guest_id = e.control.data
        guest = next(g for g in gl.guests if g.id == guest_id)
        print(f"Kliknięto: {guest.display_name}")

        page.update()

    ## dodawanie i odejmowanie stołów
    table_controls = ft.Container(
        content=ft.Row(
            controls=(
                ft.TextButton(
                    text="Dodaj stół okrągły", on_click=on_create_round_table_click
                ),
                ft.TextButton(
                    text="Dodaj stół prostokątny", on_click=on_create_square_table_click
                ),
                ft.TextButton(text="Usuń stół", on_click=on_delete_table_click),
            )
        )
    )
    table_widgets_scroll = ft.Column(
        controls=table_widgets, scroll=ft.ScrollMode.AUTO, expand=True
    )

    table_column = ft.Column(
        controls=[table_controls, table_widgets_scroll],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    tables = ft.Container(content=table_column, expand=3)
    # Stwórz listę klikalnych przycisków gości
    guest_buttons = [
        ft.TextButton(text=guest.display_name, data=guest.id, on_click=on_guest_click)
        for guest in gl.guests
    ]

    # Przewijalna lista
    guest_list = ft.Container(
        content=ft.ListView(controls=guest_buttons, spacing=5, expand=True),
        padding=10,
        border=ft.border.all(1),
        width=250,
    )

    # Layout
    page.add(
        ft.Row(
            [
                tables,
                guest_list,
            ],
            expand=True,
        )
    )


ft.app(target=main)
