import random

import pygame
from DATA.DATA import DATA
from src.Hero import Hero_Sprite
from src.Items import Potion_Sprite, Weapon_Sprite, Enemy_Sprite

SCORE = 0
HEALTH = 0


class Health(pygame.sprite.Sprite):
    """to keep track of the health."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 50)
        self.color = [255, 255, 255]
        self.last_score = -1
        self.update()
        self.rect = self.image.get_rect().move(100, 500)

    def update(self):
        """We only update the score in update() when it has changed."""
        if HEALTH != self.last_score:
            self.last_score = HEALTH
            msg = f"Health: {HEALTH}"
            self.image = self.font.render(msg, False, self.color)


class Score(pygame.sprite.Sprite):
    """to keep track of the score."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 50)
        self.color = [255, 255, 255]
        self.last_score = -1
        self.update()
        self.rect = self.image.get_rect().move(200, 50)

    def update(self):
        """We only update the score in update() when it has changed."""
        if SCORE != self.last_score:
            self.last_score = SCORE
            msg = f"Score: {SCORE}"
            self.image = self.font.render(msg, False, self.color)


class Workspace(pygame.sprite.Sprite):
    def __init__(self, screen_size, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=screen_size.center)


def random_item(row, col):
    item = DATA[random.randint(a=0, b=len(DATA) - 1)]
    item['screen_size'] = (row, col)
    item_type = item['type']
    if item_type == 'potion':
        return Potion_Sprite(**item)
    elif item_type == 'weapon':
        return Weapon_Sprite(**item)
    elif item_type == 'enemy':
        return Enemy_Sprite(**item)


def main():
    global SCORE
    global HEALTH

    pygame.init()

    SCREENRECT = start, end, width, height = pygame.Rect(0, 0, 450, 600)
    screen = pygame.display.set_mode(SCREENRECT.size)

    STEP = int((0.7 * min(SCREENRECT.size)) // 3)
    field_x, field_y = (width - STEP * 3) // 2, (height - STEP * 3) // 2

    work_screen = pygame.Rect(field_x, field_y, STEP * 3, STEP * 3)
    workspace = Workspace(work_screen, 'GUI/img/background.png')

    all = pygame.sprite.RenderUpdates()
    Hero_Sprite.containers = all

    box = {}
    print(field_x, width - field_x, STEP)
    for row in range(field_x, width - field_x - 1, STEP):
        box[row] = {}
        for col in range(field_y, height - field_y - 1, STEP):
            box[row][col] = random_item(row, col)

    box[field_x][field_y] = Hero_Sprite((field_x, field_y), 'img/hero.png')
    hero = box[field_x][field_y]

    if pygame.font:
        all.add(Score())
        all.add(Health())

    while hero.hero.is_alive():
        score = Score()
        health = Health()

        health.rect.x = field_x

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                last_pos = hero.rect.x, hero.rect.y
                if event.key == pygame.K_LEFT:
                    if hero.rect.x - STEP >= 0 + field_x:
                        hero.rect.x -= STEP
                elif event.key == pygame.K_RIGHT:
                    if hero.rect.x + STEP < width - field_x - 1:
                        hero.rect.x += STEP
                elif event.key == pygame.K_UP:
                    if hero.rect.y - STEP >= 0 + field_y:
                        hero.rect.y -= STEP
                elif event.key == pygame.K_DOWN:
                    if hero.rect.y + STEP < height - field_y - 1:
                        hero.rect.y += STEP

                if last_pos[0] != hero.rect.x or last_pos[1] != hero.rect.y:
                    SCORE += hero.identify_item(box[hero.rect.x][hero.rect.y])
                    HEALTH = hero.hero.health
                    box[hero.rect.x][hero.rect.y] = hero
                    box[last_pos[0]][last_pos[1]] = random_item(last_pos[0], last_pos[1])

        screen.blit(workspace.image, workspace.rect)
        screen.blit(score.image, score.rect)
        screen.blit(health.image, health.rect)
        for row, cols in box.items():
            for col, value in cols.items():
                screen.blit(value.image, value.rect)
        screen.blit(hero.image, hero.rect)

        pygame.display.update()
    print(f'Врагов убито: {hero.hero.kills}, Очков заработано: {hero.hero.money}.')


if __name__ == "__main__":
    main()
    pygame.quit()
