import pygame


class Item:
    def __init__(self, name, value, type):
        self.name = name
        self.value = value
        self.type = type

    def __str__(self):
        return f'{self.name} {self.value}'


class Potion:
    def __init__(self, name, value):
        self.name = name
        self.health = value

    def __str__(self):
        return f'{self.name} {self.health}'

class Potion_Sprite(pygame.sprite.Sprite):
    def __init__(self, name, value, type, image, screen_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f'GUI/{image}').convert_alpha()
        self.rect = self.image.get_rect(x=screen_size[0], y=screen_size[1])
        self.potion = Potion(name, value)


class Weapon:
    def __init__(self, name, value):
        self.name = name
        self.attack = value

    def __str__(self):
        return f'{self.name} {self.attack}'

    def was_broken(self):
        if self.attack > 0:
            return False
        return True


class Weapon_Sprite(pygame.sprite.Sprite):
    def __init__(self, name, value, type, image, screen_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f'GUI/{image}').convert_alpha()
        self.rect = self.image.get_rect(x=screen_size[0], y=screen_size[1])
        self.weapon = Weapon(name, value)


class Enemy:
    def __init__(self, name, value):
        self.name = name
        self.health = value

    def __str__(self):
        return f'{self.name} {self.health}'

    def is_dead(self):
        if self.health > 0:
            return False
        return True


class Enemy_Sprite(pygame.sprite.Sprite):
    def __init__(self, name, value, type, image, screen_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f'GUI/{image}').convert_alpha()
        self.rect = self.image.get_rect(x=screen_size[0], y=screen_size[1])
        self.enemy = Enemy(name, value)
