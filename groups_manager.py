from guest_manager import Guest


class Group:
    def __init__(self, name):
        self.name = name
        self.members: list[Guest] = []

    def add_guest(self, guest: Guest):
        if guest not in self.members:
            self.members.append(guest)
            guest.add_group(self.name)

    def remove_guest(self, guest: Guest):
        if guest in self.members:
            self.members.remove(guest)
            guest.groups.remove(self.name)


class GroupList:
    def __init__(self):
        self.groups: list[Group] = []

    def load_default_groups(self, filename):
        with open(filename, encoding="utf-8") as f:
            for line in f:
                name = line.strip()
                if name:
                    group = Group(name)
                    self.groups.append(group)

    def add_group(self, group_name):
        if group_name not in self.groups:
            self.groups.append(Group(group_name))

    def list_groups(self):
        for group in self.groups:
            print(f"{group}:")
            for guest in group.members:
                print(f" - {guest.display_name}")
