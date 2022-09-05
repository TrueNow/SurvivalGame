import random
import pygame

from DATA.DATA import DATA
from src.Items import Enemy, Potion, Weapon
from src.Hero import Hero


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

    def identify_item(self, item_group):
        if isinstance(item_group.item, Potion):
            self.hero.take_potion(item_group.item)
        elif isinstance(item_group.item, Weapon):
            self.hero.take_weapon(item_group.item)
        elif isinstance(item_group.item, Enemy):
            self.hero.attack_enemy(item_group.item)
        else:
            print('Неопознанный предмет')


class StringSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 50)
        self.color = [0, 0, 0]

    def update(self, msg, x, y):
        self.image = self.font.render(msg, False, self.color)
        self.rect = self.image.get_rect().move(x, y)


class ItemGroup(pygame.sprite.Group):
    def __init__(self, item_name, item_value, item_type, image, screen_size):
        pygame.sprite.Group.__init__(self)

        if item_type == 'potion':
            self.item = Potion(item_name, item_value)
        elif item_type == 'weapon':
            self.item = Weapon(item_name, item_value)
        elif item_type == 'enemy':
            self.item = Enemy(item_name, item_value)

        self.image_sprite = StringSprite()
        self.image_sprite.image = pygame.image.load(f'GUI/{image}').convert_alpha()
        self.image_sprite.rect = self.image_sprite.image.get_rect(x=screen_size[0], y=screen_size[1])

        self.string_sprite = StringSprite()
        msg = f'{self.item}'
        self.string_sprite.image = self.string_sprite.font.render(msg, False, self.string_sprite.color)
        self.string_sprite.rect = self.image_sprite.rect
        self.string_sprite.rect.x += 5


class WorkspaceSprite(pygame.sprite.Sprite):
    def __init__(self, screen_size, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=screen_size.center)


def random_item(row, col):
    item = DATA[random.randint(a=0, b=len(DATA) - 1)]
    item['screen_size'] = (row, col)
    return ItemGroup(**item)


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
        score = hero_sprite.hero.money
        kills = hero_sprite.hero.kills
        health = hero_sprite.hero.health
        attack = hero_sprite.hero.attack

        score_sprite = StringSprite()
        score_sprite.update(f'{score} очков', field_x, 40)

        kills_sprite = StringSprite()
        kills_sprite.update(f'{kills} убийств', field_x, 80)

        health_sprite = StringSprite()
        if attack > 0:
            health_sprite.update(f'{health} HP + {attack}', field_x, 500)
        else:
            health_sprite.update(f'{health} HP', field_x, 500)

        for event in pygame.event.get():
            h_s = hero_sprite
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                last_pos = h_s.rect.x, h_s.rect.y
                if event.key == pygame.K_LEFT:
                    if h_s.rect.x - STEP >= 0 + field_x:
                        h_s.rect.x -= STEP
                elif event.key == pygame.K_RIGHT:
                    if h_s.rect.x + STEP < width - field_x - 1:
                        h_s.rect.x += STEP
                elif event.key == pygame.K_UP:
                    if h_s.rect.y - STEP >= 0 + field_y:
                        h_s.rect.y -= STEP
                elif event.key == pygame.K_DOWN:
                    if h_s.rect.y + STEP < height - field_y - 1:
                        h_s.rect.y += STEP

                if last_pos[0] != hero_sprite.rect.x or last_pos[1] != hero_sprite.rect.y:
                    hero_sprite.identify_item(box[hero_sprite.rect.x][hero_sprite.rect.y])
                    HEALTH = hero_sprite.hero.health
                    KILLS = hero_sprite.hero.kills
                    ATTACK = hero_sprite.hero.attack
                    box[hero_sprite.rect.x][hero_sprite.rect.y] = hero_sprite
                    box[last_pos[0]][last_pos[1]] = random_item(last_pos[0], last_pos[1])

        screen.blit(workspace.image, workspace.rect)
        screen.blit(score_sprite.image, score_sprite.rect)
        screen.blit(kills_sprite.image, kills_sprite.rect)
        screen.blit(health_sprite.image, health_sprite.rect)

        for row, cols in box.items():
            for col, value in cols.items():
                if isinstance(value, HeroSprite):
                    screen.blit(hero_sprite.image, hero_sprite.rect)
                else:
                    screen.blit(value.image_sprite.image, value.image_sprite.rect)
                    screen.blit(value.string_sprite.image, value.string_sprite.rect)

        pygame.display.update()

    print(f'Врагов убито: {KILLS}, Очков заработано: {SCORE}.')


if __name__ == "__main__":
    main()
    pygame.quit()
