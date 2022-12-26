import pygame as pg
import os
import datetime


pg.init()
pg.font.init()


def main():
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    WIDTH, HEIGHT = 400, 500
    pg.display.set_caption("Virtual Assistant")
    load_icon = pg.image.load("blue_orb.ico")
    pg.display.set_icon(load_icon)

    font1 = pg.font.SysFont(None,  30)
    text1 = font1.render("Virtual Assistant", True, WHITE)
    text1_rect = text1.get_rect(center=(WIDTH / 2, 350))

    font2 = pg.font.SysFont(None, 28)
    d = datetime.datetime.now()
    text2 = font2.render(f"{d.strftime('%H: %M')}", True, WHITE)
    text2_rect = text2.get_rect(center=(WIDTH / 2, 400))

    font3 = pg.font.SysFont(None, 20)
    text3 = font3.render(f" {d.strftime('%a %d')}", True, WHITE)
    text3_rect = text2.get_rect(center=(WIDTH / 2, 430))

    win = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    sprite_dir_1 = "va_sprites/not_speaking"

    total_files_dir_1 = 0

    for _ in os.listdir(sprite_dir_1):
        total_files_dir_1 += 1

    not_speaking = [None] * total_files_dir_1

    count_file_1 = 0
    for f in os.listdir(sprite_dir_1):
        not_speaking[count_file_1] = pg.image.load(os.path.join(sprite_dir_1, f))
        count_file_1 += 1

    count = 0
    run = True

    while run:

        clock.tick(30)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        keys = pg.key.get_pressed()

        if keys[pg.K_ESCAPE]:
            run = False
            exit(0)

        win.fill(BLACK)

        count += 1
        if count >= count_file_1:
            count = 0

        win.blit(text1, text1_rect)
        win.blit(text2, text2_rect)
        win.blit(text3, text3_rect)

        win.blit(not_speaking[count], (0, 0))
        pg.display.update()

    pg.quit()


# if __name__ == "__main__":
#      main()
