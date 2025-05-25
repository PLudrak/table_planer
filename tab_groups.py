import flet as ft
from guest_manager import GuestList, Guest
from groups_manager import GroupList, Group


def get_tab_groups_content(guest_list: GuestList, groups_list: GroupList):
    return ft.Row(
        controls=[
            build_main_display(None, guest_list),
            build_group_list(None),
            build_guest_list(guest_list.guests),
        ]
    )


def build_guest_list(guests: list[Guest]):
    guest_buttons = [
        ft.TextButton(
            content=ft.Container(
                content=ft.Text(guest.names, text_align=ft.TextAlign.LEFT),
                alignment=ft.alignment.center_left,
                expand=True,
            ),
            data=guest.id,
            on_click=on_guest_click,
            expand=True,
        )
        for guest in guests
    ]

    guest_list = ft.Container(
        content=ft.ListView(controls=guest_buttons, spacing=5, expand=True),
        padding=10,
        border=ft.border.all(1),
        width=250,
    )
    return guest_list


def build_main_display(selected_guest: Guest | None, guest_list: GuestList):
    if not selected_guest:
        selected_guest = guest_list.guests[0]

    header = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.Icons.CHEVRON_LEFT,
                on_click=on_previous_guest_click,
            ),
            ft.Text(selected_guest.names),
            ft.IconButton(
                icon=ft.Icons.CHEVRON_RIGHT,
                on_click=on_next_guest_click,
            ),
        ]
    )
    box = ft.Placeholder(expand=True)

    return ft.Column(controls=[header, box], expand=True)


def on_previous_guest_click(e):
    pass


def on_next_guest_click(e):
    pass


def build_group_list(group: Group | None):
    if group:
        members_list_items = [
            ft.ListTile(
                title=ft.Text(f" {member.display_name}"),
                trailing=ft.IconButton(
                    icon=ft.Icons.CLOSE_ROUNDED, on_click=on_remove_from_group_click
                ),
            )
            for member in group.members
        ]
        header = ft.Text(group.name)

        members_list = ft.Container(
            width=200,
            border=ft.border.all(1),
            content=ft.Column(
                controls=[header, *members_list_items],
            ),
        )
    else:
        members_list = ft.Container(
            width=200,
            expand=True,
            border=ft.border.all(1),
            content=ft.Text("Nie wybrano grupy"),
        )
    return members_list


def on_remove_from_group_click(e):
    pass


def on_guest_click(e):
    pass
