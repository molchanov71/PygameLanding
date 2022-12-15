from math import sin, cos
import os
from random import randrange
import sys
import pygame as pg


pg.init()
SIZE = WIDTH, HEIGHT = 750, 300
SCREEN = pg.display.set_mode(SIZE)
V = 5


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    if not os.path.isfile(fullname):
        print(f'Файл с изображением {fullname} не найден')
        sys.exit()
    image = pg.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def main():
    class Mountain(pg.sprite.Sprite):
        image = load_image("mountains.png")

        def __init__(self):
            super().__init__(all_sprites)
            self.image = Mountain.image
            self.rect = self.image.get_rect()
            self.mask = pg.mask.from_surface(self.image)
            self.rect.bottom = HEIGHT

    class Landing(pg.sprite.Sprite):
        image = load_image("pt.png")

        def __init__(self, pos):
            super().__init__(all_sprites)
            self.image = Landing.image
            self.rect = self.image.get_rect()
            # вычисляем маску для эффективного сравнения
            self.mask = pg.mask.from_surface(self.image)
            self.rect.x = pos[0]
            self.rect.y = pos[1]

        def update(self):
            if not pg.sprite.collide_mask(self, mountain):
                self.rect = self.rect.move(0, 1)

    clock = pg.time.Clock()
    pg.display.set_caption('Заголовок окна')
    all_sprites = pg.sprite.Group()
    mountain = Mountain()
    running = True
    while running:
        # внутри игрового цикла ещё один цикл
        # приёма и обработки сообщений
        for event in pg.event.get():
            # при закрытии окна
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                Landing(event.pos)
        # отрисовка и изменение свойств объектов
        SCREEN.fill("black")
        all_sprites.draw(SCREEN)
        all_sprites.update()
        clock.tick(60)  # 30 кадров в секунду
        pg.display.flip()
    pg.quit()


if __name__ == '__main__':
    main()
