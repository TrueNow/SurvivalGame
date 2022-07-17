import random

import pygame
from DATA.DATA import DATA
from src.Hero import Hero
from src.Items import Potion, Weapon, Enemy

HEALTH = 0
ATTACK = 0
SCORE = 0
KILLS = 0


class HeroSprite(pygame.sprite.Sprite):
    def __init__(self, screen_size, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f'GUI/{filename}').convert_alpha()
        self.rect = self.image.get_rect(x=screen_size[0], y=screen_size[1])

        self.hero = Hero(**{'name': 'Герой', 'health': 10})

    def identify_item(self, item):
        if isinstance(item, PotionGroup):
            score = 0
            self.hero.take_potion(item.potion)
        elif isinstance(item, WeaponGroup):
            score = 0
            self.hero.take_weapon(item.weapon)
        elif isinstance(item, EnemyGroup):
            score = item.enemy.health
            if self.hero.attack_enemy(item.enemy):
                self.hero.money += score
        else:
            print('Неопознанный предмет')
            score = 0
        return score


class StringSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 50)
        self.color = [255, 255, 255]


class HealthSprite(StringSprite):
    """to keep track of the health."""

    def __init__(self):
        StringSprite.__init__(self)
        self.update()
        self.rect = self.image.get_rect().move(100, 500)

    def update(self):
        """We only update the score in update() when it has changed."""
        msg = f'{HEALTH} HP'
        self.image = self.font.render(msg, False, self.color)


class AttackSprite(StringSprite):
    def __init__(self):
        StringSprite.__init__(self)
        self.update()
        self.rect = self.image.get_rect().move(175, 500)

    def update(self) -> None:
        msg = f'+ {ATTACK}'
        self.image = self.font.render(msg, False, self.color)


class ScoreSprite(StringSprite):
    """to keep track of the score."""

    def __init__(self):
        StringSprite.__init__(self)
        self.update()
        self.rect = self.image.get_rect().move(50, 80)

    def update(self):
        """We only update the score in update() when it has changed."""
        msg = f'{SCORE} очков'
        self.image = self.font.render(msg, False, self.color)


class KillsSprite(StringSprite):
    def __init__(self):
        StringSprite.__init__(self)
        self.update()
        self.rect = self.image.get_rect().move(50, 40)

    def update(self) -> None:
        msg = f'{KILLS} убийств'
        self.image = self.font.render(msg, False, self.color)


class PotionGroup(pygame.sprite.Group):
    def __init__(self, name, value, type, image, screen_size):
        pygame.sprite.Group.__init__(self)
        self.potion = Potion(name, value)

        self.image_sprite = StringSprite()
        self.image_sprite.image = pygame.image.load(f'GUI/{image}').convert_alpha()
        self.image_sprite.rect = self.image_sprite.image.get_rect(x=screen_size[0], y=screen_size[1])

        self.string_sprite = StringSprite()
        msg = f'{self.potion.health}'
        self.string_sprite.image = self.string_sprite.font.render(msg, False, [0, 0, 0])
        self.string_sprite.rect = self.image_sprite.rect


class WeaponGroup(pygame.sprite.Group):
    def __init__(self, name, value, type, image, screen_size):
        pygame.sprite.Group.__init__(self)
        self.weapon = Weapon(name, value)

        self.image_sprite = StringSprite()
        self.image_sprite.image = pygame.image.load(f'GUI/{image}').convert_alpha()
        self.image_sprite.rect = self.image_sprite.image.get_rect(x=screen_size[0], y=screen_size[1])

        self.string_sprite = StringSprite()
        msg = f'{self.weapon.attack}'
        self.string_sprite.image = self.string_sprite.font.render(msg, False, [0, 0, 0])
        self.string_sprite.rect = self.image_sprite.rect


class EnemyGroup(pygame.sprite.Group):
    def __init__(self, name, value, type, image, screen_size):
        pygame.sprite.Group.__init__(self)
        self.enemy = Enemy(name, value)

        self.image_sprite = StringSprite()
        self.image_sprite.image = pygame.image.load(f'GUI/{image}').convert_alpha()
        self.image_sprite.rect = self.image_sprite.image.get_rect(x=screen_size[0], y=screen_size[1])

        self.string_sprite = StringSprite()
        msg = f'{self.enemy.health}'
        self.string_sprite.image = self.string_sprite.font.render(msg, False, [0, 0, 0])
        self.string_sprite.rect = self.image_sprite.rect


class WorkspaceSprite(pygame.sprite.Sprite):
    def __init__(self, screen_size, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=screen_size.center)


def random_item(row, col):
    item = DATA[random.randint(a=0, b=len(DATA) - 1)]
    item['screen_size'] = (row, col)
    item_type = item['type']
    if item_type == 'potion':
        return PotionGroup(**item)
    elif item_type == 'weapon':
        return WeaponGroup(**item)
    elif item_type == 'enemy':
        return EnemyGroup(**item)


def main():
    global HEALTH
    global ATTACK
    global SCORE
    global KILLS

    pygame.init()

    SCREENRECT = start, end, width, height = pygame.Rect(0, 0, 450, 600)
    screen = pygame.display.set_mode(SCREENRECT.size)

    STEP = int((0.7 * min(SCREENRECT.size)) // 3)
    field_x, field_y = (width - STEP * 3) // 2, (height - STEP * 3) // 2

    work_screen = pygame.Rect(field_x, field_y, STEP * 3, STEP * 3)
    workspace = WorkspaceSprite(work_screen, 'GUI/img/background.png')

    box = {}
    for row in range(field_x, width - field_x - 1, STEP):
        box[row] = {}
        for col in range(field_y, height - field_y - 1, STEP):
            box[row][col] = random_item(row, col)

    hero_sprite = box[field_x][field_y] = HeroSprite((field_x, field_y), 'img/hero.png')
    HEALTH = hero_sprite.hero.health

    while hero_sprite.hero.is_alive():
        score = ScoreSprite()
        health = HealthSprite()
        kills = KillsSprite()
        attack = AttackSprite()

        health.rect.x = field_x

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                last_pos = hero_sprite.rect.x, hero_sprite.rect.y
                if event.key == pygame.K_LEFT:
                    if hero_sprite.rect.x - STEP >= 0 + field_x:
                        hero_sprite.rect.x -= STEP
                elif event.key == pygame.K_RIGHT:
                    if hero_sprite.rect.x + STEP < width - field_x - 1:
                        hero_sprite.rect.x += STEP
                elif event.key == pygame.K_UP:
                    if hero_sprite.rect.y - STEP >= 0 + field_y:
                        hero_sprite.rect.y -= STEP
                elif event.key == pygame.K_DOWN:
                    if hero_sprite.rect.y + STEP < height - field_y - 1:
                        hero_sprite.rect.y += STEP

                if last_pos[0] != hero_sprite.rect.x or last_pos[1] != hero_sprite.rect.y:
                    SCORE += hero_sprite.identify_item(box[hero_sprite.rect.x][hero_sprite.rect.y])
                    HEALTH = hero_sprite.hero.health
                    KILLS = hero_sprite.hero.kills
                    ATTACK = hero_sprite.hero.attack
                    box[hero_sprite.rect.x][hero_sprite.rect.y] = hero_sprite
                    box[last_pos[0]][last_pos[1]] = random_item(last_pos[0], last_pos[1])

        screen.blit(workspace.image, workspace.rect)
        screen.blit(health.image, health.rect)
        screen.blit(attack.image, attack.rect)
        screen.blit(score.image, score.rect)
        screen.blit(kills.image, kills.rect)

        for row, cols in box.items():
            for col, value in cols.items():
                if isinstance(value, HeroSprite):
                    screen.blit(hero_sprite.image, hero_sprite.rect)
                else:
                    screen.blit(value.image_sprite.image, value.image_sprite.rect)
                    screen.blit(value.string_sprite.image, value.string_sprite.rect)

        pygame.display.update()

    print(f'Врагов убито: {hero_sprite.hero.kills}, Очков заработано: {hero_sprite.hero.money}.')


if __name__ == "__main__":
    main()
    pygame.quit()
