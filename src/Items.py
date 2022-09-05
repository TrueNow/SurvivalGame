class Potion:
    def __init__(self, name, value):
        self.name = name
        self.health = value

    def __str__(self):
        return f'{self.health}'


class Weapon:
    def __init__(self, name, value):
        self.name = name
        self.attack = value

    def __str__(self):
        return f'{self.attack}'

    def was_broken(self):
        if self.attack > 0:
            return False
        return True


class Enemy:
    def __init__(self, name, value):
        self.name = name
        self.health = value

    def __str__(self):
        return f'{self.health}'

    def is_dead(self):
        if self.health > 0:
            return False
        return True
