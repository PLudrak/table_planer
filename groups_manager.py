from guest_manager import Guest


class Group:
    def __init__(self, name):
        self.name = name
        self.members = []

    def add_guest(self, guest: Guest):
        if guest not in self.members:
            self.members.append(guest)
            guest.add_group(self.name)

    def remove_guest(self, guest: Guest):
        if guest in self.members:
            self.members.remove(guest)
            guest.groups.remove(self.name)


class GuestList:
    def __init__(self):
        self.guests = []
        self.groups = {}

    def add_group(self, group_name):
        if group_name not in self.groups:
            self.groups[group_name] = Group(group_name)

    def assign_guest_to_group(self, guest: Guest, group_name: str):
        self.add_group(group_name)
        self.groups[group_name].add_guest(guest)

    def list_groups(self):
        for group_name, group in self.groups.items():
            print(f"{group_name}: {[guest.display_name for guest in group.members]}")
