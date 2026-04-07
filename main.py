import sys
import pathlib
from settings import *
from tetris import Tetris, Text


class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Pytris')
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.set_timer()

        pg.key.set_repeat(200, 50)

        self.images = self.load_images()
        self.load_sfx()
        self.tetris = Tetris(self)
        self.text = Text(self)

    def load_sfx(self):
        pg.mixer.init()
        self.sfx_clear = pg.mixer.Sound(SFX_CLEAR_PATH)
        self.sfx_gameover = pg.mixer.Sound(SFX_GAMEOVER_PATH)

        pg.mixer.music.load(BGM_PATH)
        pg.mixer.music.set_volume(0.6)

    def load_images(self):
        files = [item for item in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png') if item.is_file()]
        images = [pg.image.load(file).convert_alpha() for file in files]
        images = [pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)) for image in images]
        return images

    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.anim_trigger = False
        self.fast_anim_trigger = False
        pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_event, FAST_ANIM_TIME_INTERVAL)

    def update(self):
        if not self.tetris.game_over:
            self.tetris.update()
        self.clock.tick(FPS)

    def draw(self):
        if self.tetris.retro_mode:
            self.screen.fill(color=(40, 40, 35))
            self.screen.fill(color=(30, 30, 25), rect=(0, 0, *FIELD_RES))
        else:
            self.screen.fill(color=BG_COLOR)
            self.screen.fill(color=FIELD_COLOR, rect=(0, 0, *FIELD_RES))

        self.tetris.draw()
        self.text.draw()

        if self.tetris.game_over:
            self.tetris.draw_game_over()

        pg.display.flip()

    def check_events(self):
        self.anim_trigger = False
        self.fast_anim_trigger = False

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.tetris.game_over and event.button == 1:
                    if self.tetris.btn_restart.collidepoint(event.pos):
                        self.tetris.__init__(self)
                    elif self.tetris.btn_exit.collidepoint(event.pos):
                        pg.quit()
                        sys.exit()

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    self.tetris.__init__(self)
                elif not self.tetris.game_over:
                    self.tetris.control(pressed_key=event.key)

            elif event.type == pg.KEYUP:
                if event.key == pg.K_DOWN:
                    self.tetris.speed_up = False

            elif event.type == self.user_event:
                self.anim_trigger = True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    app = App()
    app.run()