class Guest:
    _id_counter = 1

    def __init__(self, names):
        self.id = Guest._id_counter
        Guest._id_counter += 1

        self.names = names
        self.pair, self.persons = self.get_full_names()
        self.one_family, self.family_name = self.is_one_family()
        self.display_name = self.get_display_name()
        self.groups = []

    def get_full_names(self):
        names = self.names
        if " i " in self.names.lower():
            pair = True
            persons = names.split(" i ")

            full_names = []
            for person in persons:
                full_name = self.extract_surname(person)
                full_names.append(full_name)
            return pair, full_names

        else:
            pair = False
            full_name = [self.extract_surname(names)]
            return (
                pair,
                full_name,
            )

    def extract_surname(self, name):
        if name.lower() == "osoba towarzysząca":
            return {"name": "Osoba towarzysząca", "surname": None}
        name = name.split()
        person = {}

        person["name"] = name[0]
        if len(name) == 2:
            person["surname"] = name[1]
        else:
            person["surname"] = None
        return person

    def is_one_family(self):
        surnames = []
        for person in self.persons:
            surname = person["surname"]
            if surname is not None:
                surnames.append(surname)
        family_names = sorted(set(surnames))
        if len(family_names) == 1:
            return True, family_names[0]
        else:
            return False, (", ".join(family_names))

    def get_display_name(self):
        display_names = []
        for person in self.persons:
            name = person["name"]
            if self.one_family == True or person["surname"] is None:
                display_names.append(name)
            else:
                surname = person["surname"]
                display_names.append(f"{name} {surname[0]}.")

        display_name = " i ".join(display_names)
        if self.one_family == True:
            display_name += f" {self.family_name[0]}."

        if "Osoba towarzysząca" in display_name:
            display_name = display_name.replace(" i Osoba towarzysząca", "")
            display_name += " (+1)"
        return display_name

    def add_group(self, group_name: str):
        if group_name not in self.groups:
            self.groups.append(group_name)


class GuestList:
    def __init__(self):
        self.guests = []

    def load_list(self, filename):
        with open(filename, encoding="utf-8") as f:
            for line in f:
                name = line.strip()
                if name:
                    guest = Guest(name)
                    self.guests.append(guest)


class Table:
    _id_counter = 1

    def __init__(self, type="square"):
        self.table_id = Table._id_counter
        Table._id_counter += 1
        self.type = type
        self.max_seats = self.get_max_seats()

        self.guests = []
        self.occupied_seats = 0

    def get_max_seats(self):
        if self.type == "square":
            return 60
        if self.type == "round":
            return 12
        else:
            return 60

    @property
    def free_seats(self):
        free_seats = self.max_seats - self.occupied_seats
        return free_seats

    def add_guest(self, guest: Guest):
        if self.can_add_guest(guest):
            self.guests.append(guest)
            if guest.pair:
                self.occupied_seats += 2
            else:
                self.occupied_seats += 1
            print(f"{guest.display_name} przypisany do stołu {self.table_id}")
        else:
            print(f"Not enough free seats for {guest.display_name}")

    def can_add_guest(self, guest: Guest):
        if guest.pair:
            seats_required = 2
        else:
            seats_required = 1
        if self.free_seats >= seats_required:
            return True
        else:
            return False
