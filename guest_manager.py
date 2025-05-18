class Guest:
    def __init__(self, names):
        self.names = names
        self.pair, self.persons = self.get_full_names()
        self.one_family, self.family_name = self.is_one_family()

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
        family_names = set(surnames)
        if len(family_names) == 1:
            return True, *family_names
        else:
            return False, (", ".join(family_names))
