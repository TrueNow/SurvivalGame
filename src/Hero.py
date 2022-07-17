class Hero:
    def __init__(self, name, health):
        self.name: str = name
        self.health: int = health
        self.max_health: int = 20
        # self.item: str = ''
        self.attack: int = 0
        self.money: int = 0

        self.lvl: int = 1
        self.kills: int = 0
        self.limit_kills = 10

    def __str__(self):
        if self.attack:
            return f"{self.name} {self.health}+{self.attack}"
        return f"{self.name} {self.health}"

    def have_weapon(self):
        return bool(self.attack)

    def lvl_up(self):
        self.lvl += 1
        self.max_health += 5
        self.limit_kills *= 2

    def is_alive(self):
        if self.health > 0:
            return True
        return False

    # __________ACTION__________

    def attack_enemy(self, enemy):
        if self.have_weapon():
            if enemy.health >= self.attack:
                enemy.health -= self.attack
                self.attack -= self.attack
                # self.item = ''
            else:
                self.attack -= enemy.health
                enemy.health -= enemy.health

        self.health -= enemy.health

        enemy.health -= enemy.health
        self.kills += 1

        if self.kills == self.limit_kills:
            self.lvl_up()

        return self.is_alive()

    def take_potion(self, potion):
        self.health += potion.health
        if self.health > self.max_health:
            self.health = self.max_health

    def take_weapon(self, weapon):
        # self.item = weapon.name
        self.attack = weapon.attack
