from settings import *
import math
from tetromino import Tetromino
import pygame.freetype as ft


class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)

    def get_color(self):
        time = pg.time.get_ticks() * 0.001
        n_sin = lambda t: (math.sin(t) * 0.5 + 0.5) * 255
        return n_sin(time * 0.5), n_sin(time * 0.2), n_sin(time * 0.9)

    def draw(self):
        self.font.render_to(self.app.screen, (WIN_W * 0.595, WIN_H * 0.02),
                            text='PYTRIS', fgcolor=self.get_color(),
                            size=TILE_SIZE * 1.5)
        self.font.render_to(self.app.screen, (WIN_W * 0.65, WIN_H * 0.12),
                            text='next', fgcolor='orange',
                            size=TILE_SIZE * 1.4)
        self.font.render_to(self.app.screen, (WIN_W * 0.65, WIN_H * 0.42),
                            text='hold', fgcolor='orange',
                            size=TILE_SIZE * 1.4)

        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.57),
                            text='level', fgcolor='orange',
                            size=TILE_SIZE * 1.4)
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.65),
                            text=f'{self.app.tetris.level}', fgcolor='white',
                            size=TILE_SIZE * 1.8)

        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.75),
                            text='score', fgcolor='orange',
                            size=TILE_SIZE * 1.4)
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.85),
                            text=f'{self.app.tetris.score}', fgcolor='white',
                            size=TILE_SIZE * 1.8)


class Tetris:
    def __init__(self, app):
        self.app = app
        self.sprite_group = pg.sprite.Group()
        self.field_array = self.get_field_array()
        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current=False)
        self.hold_tetromino = None
        self.can_hold = True
        self.speed_up = False
        self.game_over = False

        btn_w, btn_h = 220, 60
        center_x = WIN_W // 2 - btn_w // 2
        self.btn_restart = pg.Rect(center_x, WIN_H // 2, btn_w, btn_h)
        self.btn_exit = pg.Rect(center_x, WIN_H // 2 + 80, btn_w, btn_h)

        self.score = 0
        self.full_lines = 0
        self.points_per_lines = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

        self.retro_mode = False
        self.level = 1

        pg.time.set_timer(self.app.user_event, ANIM_TIME_INTERVAL)
        pg.mixer.music.play(-1)

    def get_score(self):
        if self.full_lines > 0:
            self.score += self.points_per_lines[self.full_lines]
            self.full_lines = 0

            new_level = (self.score // 1000) + 1
            if new_level > self.level:
                self.level = new_level
                new_speed = max(40, ANIM_TIME_INTERVAL - (self.level - 1) * 15)
                pg.time.set_timer(self.app.user_event, int(new_speed))

    def check_full_lines(self):
        row = FIELD_H - 1
        lines_cleared_now = 0
        trigger_mode_switch = False

        for y in range(FIELD_H - 1, -1, -1):
            for x in range(FIELD_W):
                self.field_array[row][x] = self.field_array[y][x]
                if self.field_array[y][x]:
                    self.field_array[row][x].pos = vec(x, row)

            if sum(map(bool, self.field_array[y])) < FIELD_W:
                row -= 1
            else:
                for x in range(FIELD_W):
                    if getattr(self.field_array[row][x], 'is_special', False):
                        trigger_mode_switch = True

                    self.field_array[row][x].alive = False
                    self.field_array[row][x] = 0

                self.full_lines += 1
                lines_cleared_now += 1

        if trigger_mode_switch:
            self.retro_mode = not self.retro_mode

        if lines_cleared_now > 0:
            self.app.sfx_clear.play()

    def put_tetromino_blocks_in_array(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block

    def get_field_array(self):
        return [[0 for x in range(FIELD_W)] for y in range(FIELD_H)]

    def is_game_over(self):
        if self.tetromino.blocks[0].pos.y == INIT_POS_OFFSET[1]:
            pg.mixer.music.stop()
            self.app.sfx_gameover.play()
            return True
        return False

    def draw_game_over(self):
        overlay = pg.Surface(WIN_RES, pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.app.screen.blit(overlay, (0, 0))

        font = self.app.text.font

        font.render_to(self.app.screen, (WIN_W // 2 - 170, WIN_H // 2 - 120),
                       text='GAME OVER', fgcolor='red', size=TILE_SIZE * 1.5)

        mouse_pos = pg.mouse.get_pos()

        color_restart = 'yellow' if self.btn_restart.collidepoint(mouse_pos) else 'white'
        pg.draw.rect(self.app.screen, color_restart, self.btn_restart, border_radius=10)
        font.render_to(self.app.screen, (self.btn_restart.x + 35, self.btn_restart.y + 20),
                       text='RESTART', fgcolor='black', size=TILE_SIZE * 0.6)

        color_exit = 'yellow' if self.btn_exit.collidepoint(mouse_pos) else 'white'
        pg.draw.rect(self.app.screen, color_exit, self.btn_exit, border_radius=10)
        font.render_to(self.app.screen, (self.btn_exit.x + 75, self.btn_exit.y + 20),
                       text='EXIT', fgcolor='black', size=TILE_SIZE * 0.6)

    def check_tetromino_landing(self):
        if self.tetromino.landing:
            if self.is_game_over():
                self.game_over = True
            else:
                self.speed_up = False
                self.can_hold = True
                self.put_tetromino_blocks_in_array()
                self.next_tetromino.current = True
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino(self, current=False)

    def hold(self):
        if not self.can_hold:
            return

        if self.hold_tetromino is None:
            self.hold_tetromino = Tetromino(self, current='hold', shape=self.tetromino.shape,
                                            image=self.tetromino.image, is_special=self.tetromino.is_special)
            for block in self.tetromino.blocks: block.kill()
            self.next_tetromino.current = True
            self.tetromino = self.next_tetromino
            self.next_tetromino = Tetromino(self, current=False)
        else:
            temp_shape = self.hold_tetromino.shape
            temp_image = self.hold_tetromino.image
            temp_special = self.hold_tetromino.is_special

            for block in self.tetromino.blocks: block.kill()
            for block in self.hold_tetromino.blocks: block.kill()

            self.hold_tetromino = Tetromino(self, current='hold', shape=self.tetromino.shape,
                                            image=self.tetromino.image, is_special=self.tetromino.is_special)
            self.tetromino = Tetromino(self, current=True, shape=temp_shape, image=temp_image, is_special=temp_special)

        self.can_hold = False

    def control(self, pressed_key):
        if pressed_key == pg.K_LEFT:
            self.tetromino.move(direction='left')
        elif pressed_key == pg.K_RIGHT:
            self.tetromino.move(direction='right')
        elif pressed_key == pg.K_UP:
            self.tetromino.rotate()
        elif pressed_key == pg.K_DOWN:
            self.speed_up = True
        elif pressed_key == pg.K_c:
            self.hold()

    def get_ghost_positions(self):
        ghost_positions = [vec(block.pos) for block in self.tetromino.blocks]
        while True:
            test_positions = [pos + vec(0, 1) for pos in ghost_positions]
            if self.tetromino.is_collide(test_positions):
                break
            ghost_positions = test_positions
        return ghost_positions

    def draw_ghost(self):
        for pos in self.get_ghost_positions():
            x, y = int(pos.x), int(pos.y)
            if y >= 0:
                rect = pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pg.draw.rect(self.app.screen, 'white', rect, 1)

    def draw_grid(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.app.screen, 'black',
                             (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    def update(self):
        trigger = [self.app.anim_trigger, self.app.fast_anim_trigger][self.speed_up]
        if trigger:
            self.check_full_lines()
            self.tetromino.update()
            self.check_tetromino_landing()
            self.get_score()
        self.sprite_group.update()

    def draw_retro_style(self):
        font = self.app.text.font

        for y in range(FIELD_H):
            font.render_to(self.app.screen, (-20, y * TILE_SIZE + 10), text='<!', fgcolor=(150, 150, 150),
                           size=TILE_SIZE * 0.8)
            font.render_to(self.app.screen, (FIELD_W * TILE_SIZE, y * TILE_SIZE + 10), text='!>',
                           fgcolor=(150, 150, 150), size=TILE_SIZE * 0.8)

            for x in range(FIELD_W):
                font.render_to(self.app.screen, (x * TILE_SIZE + 20, y * TILE_SIZE + 10), text='.',
                               fgcolor=(80, 80, 80), size=TILE_SIZE * 0.5)

        for block in self.sprite_group:
            x, y = block.rect.x, block.rect.y
            color = (255, 100, 100) if block.is_special else (200, 220, 200)
            font.render_to(self.app.screen, (x + 5, y + 10), text='[]', fgcolor=color, size=TILE_SIZE * 0.8)

    def draw(self):
        if self.retro_mode:
            self.draw_retro_style()
        else:
            self.draw_grid()
            if not self.game_over:
                self.draw_ghost()
            self.sprite_group.draw(self.app.screen)