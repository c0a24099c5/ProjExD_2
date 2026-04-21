import os
import sys
import pygame as pg
import random
import time

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 画面内にとどめる
def check_bound(rct: pg.Rect):
    """
    Rectが画面内かどうかを判定
    戻り値：(横方向, 縦方向) のタプル
    True：画面内 / False：画面外
    """
    yoko = True
    tate = True

    if rct.left < 0 or rct.right > WIDTH:
        yoko = False
    if rct.top < 0 or rct.bottom > HEIGHT:
        tate = False

    return yoko, tate

# gameover画面表示
def gameover(screen: pg.Surface) -> None:
    # 黒いSurface
    black = pg.Surface((WIDTH, HEIGHT))
    black.fill((0, 0, 0))
    black.set_alpha(150)

    # フォント
    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rct = text.get_rect(center=(WIDTH//2, HEIGHT//2))

    # こうかとん画像（泣いてる）
    kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    left_rct = kk_img.get_rect()
    left_rct.center = WIDTH//2 - 200, HEIGHT//2
    right_rct = kk_img.get_rect()
    right_rct.center = WIDTH//2 + 200, HEIGHT//2

    # 描画
    screen.blit(black, (0, 0))
    screen.blit(text, text_rct)
    screen.blit(kk_img, left_rct)
    screen.blit(kk_img, right_rct)

    pg.display.update()
    time.sleep(5)

# 爆弾拡大、加速
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    bb_accs = []
    # 爆弾Surfaceのlist
    for r in range(1, 11):
            bb_img = pg.Surface((20 * r, 20 * r))
            bb_img.set_colorkey((0, 0, 0))
            pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
            bb_imgs.append(bb_img)

    # 加速度のlist
    bb_accs = [a for a in range(1, 11)]

    return bb_imgs, bb_accs

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    # tmr = 0

    # 爆弾Surface
    bb_img = pg.Surface((20, 20))
    bb_img.set_colorkey((0, 0, 0))  # 黒を透明に

    # 赤い円
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)

    # 爆弾のRect
    bb_rct = bb_img.get_rect()

    # ランダムな初期位置
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)

    # 速度
    vx, vy = 5, 5

    init_bb_imgs()

    while True:
        screen.blit(bg_img, [0, 0]) 

        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        # キー入力
        key_lst = pg.key.get_pressed()

        DELTA = {
            pg.K_UP:   (0, -5),
            pg.K_DOWN: (0,  5),
            pg.K_LEFT: (-5, 0),
            pg.K_RIGHT:(5,  0),
        }

        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        
        # 爆弾
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)

        # こうかとん
        old_rct = kk_rct.copy()
        kk_rct.move_ip(sum_mv)
        yoko, tate = check_bound(kk_rct)
        if not yoko or not tate:
            kk_rct = old_rct
        screen.blit(kk_img, kk_rct)

        # 衝突
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        pg.display.update()
        clock.tick(50)
        




if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
