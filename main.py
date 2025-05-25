import flet as ft
from guest_manager import GuestList, Guest, Table
from tab_groups import get_tab_groups_content
from groups_manager import GroupList, Group


def main(page: ft.Page):
    page.title = "Planer stołów"
    page.theme_mode = ft.ThemeMode.LIGHT
    selected_guest: Guest | None = None

    # Załaduj listę gości
    gl = GuestList()
    gl.load_list("lista_gosci.txt")
    grl = GroupList()
    grl.load_default_groups("default_groups.txt")

    # lista stołów
    tables_list: list[Table] = []
    table_widgets: list[ft.Control] = []

    def update_tables_ui():
        table_widgets_scroll.controls = table_widgets
        table_widgets_scroll.update()

    def on_create_round_table_click(e):
        new_table = Table(type="round")
        tables_list.append(new_table)
        table_widget = build_table_widget(new_table)
        table_widgets.append(table_widget)
        update_tables_ui()

    def on_create_square_table_click(e):
        new_table = Table(type="square")
        tables_list.append(new_table)
        table_widget = build_table_widget(new_table)
        table_widgets.append(table_widget)
        update_tables_ui()

    def build_table_widget(table: Table):
        # Główna etykie stołu
        label = ft.Text(
            f"Stół {table.table_id}\n{table.free_seats} wolnych miejsc",
            text_align=ft.TextAlign.CENTER,
        )

        table_shape = ft.Container(
            content=label,
            padding=10,
            width=150,
            height=150 if table.type == "round" else 200,
            border=ft.border.all(1),
            border_radius=75 if table.type == "round" else 5,
            alignment=ft.alignment.center,
            data=table.table_id,
            on_click=on_table_click,
        )

        guest_buttons = [
            ft.ElevatedButton(text=g.display_name, disabled=True) for g in table.guests
        ]

        # uklad gosci przy stole
        max_per_column = 3 if table.type == "round" else 5
        guest_columns = []

        for i in range(0, len(table.guests), max_per_column):
            col_buttons = guest_buttons[i : i + max_per_column]
            guest_columns.append(ft.Column(controls=col_buttons, spacing=5))

        widget = ft.Row(
            controls=[table_shape] + guest_columns,
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
        )
        return widget

    def on_delete_table_click(e):
        pass

    # Funkcja do obsługi kliknięcia gościa
    def on_guest_click(e):
        nonlocal selected_guest
        guest_id = e.control.data
        selected_guest = next(g for g in gl.guests if g.id == guest_id)
        print(f"Kliknięto: {selected_guest.display_name}")

        page.update()

    def on_table_click(e):
        nonlocal selected_guest
        if selected_guest:
            table_id = e.control.data
            table = next(t for t in tables_list if t.table_id == table_id)
            if table.add_guest(selected_guest):
                remove_guest_from_list(selected_guest)
                idx = tables_list.index(table)
                table_widgets[idx] = build_table_widget(table)
                update_tables_ui()

            selected_guest = None

    def remove_guest_from_list(selected_guest):
        guest_buttons[:] = [b for b in guest_buttons if b.data != selected_guest.id]
        guest_list.content.controls = guest_buttons
        guest_list.update()

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
    )

    tables = ft.Container(content=table_column, expand=3)
    # Stwórz listę klikalnych przycisków gości
    guest_buttons = [
        ft.TextButton(
            content=ft.Container(
                content=ft.Text(guest.names, text_align=ft.TextAlign.LEFT),
                alignment=ft.alignment.center_left,
                expand=True,
            ),
            data=guest.id,
            on_click=on_guest_click,
            style=ft.ButtonStyle(alignment=ft.alignment.center_left),
            expand=True,
        )
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
    tab1_content = ft.Row(
        [tables, guest_list],
        expand=True,
    )

    tab2_content = ft.Container(
        content=ft.Text("Tutaj cos bedzie", size=20),
        alignment=ft.alignment.center,
        expand=True,
    )

    tabs = ft.Tabs(
        selected_index=0,
        expand=True,
        tabs=[
            ft.Tab(text="Stoły", content=tab1_content),
            ft.Tab(text="Grupy", content=get_tab_groups_content(gl, grl)),
        ],
    )

    page.add(tabs)


ft.app(target=main)
