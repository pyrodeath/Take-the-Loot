# Collect the Blocks
# Run around and collect the blocks

# TODO: time bonus
# TODO: powerups
# TODO: more mob features (different types, etc)
# TODO: Level designs (walls, gravity (black holes?))
#import C as C
import pygame
import sys

class MenuItem(pygame.font.Font):
    def __init__(self, text, font, font_size=30, color=(255, 255, 255), padding=0):
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.font_size = font_size
        self.color = color
        self.label = self.render(self.text, True, self.color)
        self.rect = self.label.get_rect()
        self.rect.inflate_ip(0, padding)
        self.width = self.rect.width
        self.height = self.rect.height
        self.size = (self.width, self.height)
        self.posx = 0
        self.posy = 0
        self.pos = (0, 0)

    def set_pos(self, x, y):
        self.pos = (x, y)
        self.posx = x
        self.posy = y

    def set_color(self, col):
        self.color = col
        self.label = self.render(self.text, True, self.color)

    def is_selected_mouse(self):
        posx, posy = pygame.mouse.get_pos()
        if (posx >= self.posx and posx <= self.posx + self.width) and \
           (posy >= self.posy and posy <= self.posy + self.height):
            return True
        return False

class GameMenu:
    def __init__(self, game, title, items, bg_color=(0, 0, 0), bg_image=None,
                 font=None, font_size=30, color=(255, 255, 255), hcolor=(255, 0, 0),
                 padding=40):
        self.game = game
        self.bg_image = bg_image
        self.title = title
        self.width = self.game.screen.get_width()
        self.height = self.game.screen.get_height()
        self.bg_color = bg_color
        self.color = color
        self.hcolor = hcolor
        self.items = []
        self.cur_item = None
        self.mouse_visible = True
        self.padding = padding


        for index, item in enumerate(items):
            menu_item = MenuItem(item, font, font_size, color, self.padding)
            total_height = len(items) * menu_item.height
            posx = (self.width / 2) - (menu_item.width / 2)
            posy = (self.height / 2) - (total_height / 2) + ((index * 2) + index * menu_item.height) + 50
            menu_item.set_pos(posx, posy)
            self.items.append(menu_item)

    def set_mouse_hover(self, item):
        # highlight the mouse hover item
        if item.is_selected_mouse():
            item.set_color(self.hcolor)
            self.cur_item = self.items.index(item)
            # item.set_italic(True)
        else:
            item.set_color(self.color)
            # item.set_italic(False)

    def set_keyb_selection(self, key):
        # highlight menu item by key selection
        for item in self.items:
            # item.set_italic(False)
            item.set_color(self.color)

        if self.cur_item is None:
            self.cur_item = 0
        else:
            if key == pygame.K_RETURN:
                self.go()
            elif key == pygame.K_UP:
                self.cur_item -= 1
            elif key == pygame.K_DOWN:
                self.cur_item += 1
            self.cur_item = self.cur_item % len(self.items)

        # self.items[self.cur_item].set_italic(True)
        self.items[self.cur_item].set_color(self.hcolor)

    def go(self):
        # execute the selected item's action
        if self.cur_item is None:
            return
        if self.items[self.cur_item].text == "Quit":
            pygame.quit()
            sys.exit()
        elif self.items[self.cur_item].text == "Play":
            self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.game.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN]:
                        self.mouse_visible = False
                        self.set_keyb_selection(event.key)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for item in self.items:
                        if item.is_selected_mouse():
                            self.go()
            # return mouse visibility if mouse moves
            if pygame.mouse.get_rel() != (0, 0):
                self.mouse_visible = True
                self.cur_item = None

            pygame.mouse.set_visible(self.mouse_visible)
            self.game.screen.fill((0, 0, 0))
            if self.bg_image:
               self.game.screen.blit(self.bg_image, (0, 0))

            if type(self.title) is str:
                self.game.draw_text(self.title, 40, self.game.screen.get_width()/2, 40)

            if self.bg_image:
                self.game.screen.blit(self.bg_image, self.bg_rect)
            for item in self.items:
                if self.mouse_visible:
                    self.set_mouse_hover(item)
                self.game.screen.blit(item.label, item.pos)
            pygame.display.flip()


# for testing
if __name__ == "__main__":
    class Game:
        def __init__(self):
            pygame.init()
            self.screen = pygame.display.set_mode((640, 480))
            self.clock = pygame.time.Clock()

        def draw_text(self, text, size, x, y, center=True):
            # utility function to draw text at a given location
            # TODO: move font matching to beginning of file (don't repeat)
            font_name = pygame.font.match_font('arial')
            font = pygame.font.Font(font_name, size)
            text_surface = font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            if center:
                text_rect.midtop = (x, y)
            else:
                text_rect.topleft = (x, y)
            return self.screen.blit(text_surface, text_rect)

    g = Game()
    font = pygame.font.match_font("Ubuntu Mono")
    # standard list of options and customized labels
    items = {"play": "Play", "opt": "Options", "quit": "Quit"}
    menu = GameMenu(g, "Take the Loot", ["Play", "Options", "Quit"], font=font, font_size=40)
    menu.run()
    print("starting game")

from turtledemo import clock

import pygame
import sys
import os
import random

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BGCOLOR = BLACK

WIDTH = 800
HEIGHT = 640
FPS = 60
TITLE = "Take The Loot"

#pygame.mixer.pre_init(44100,16,2,4096)


#pygame.mixer.music.load("8 bit music.mp3")
#pygame.mixer.music.set_volume(1)
#pygame.mixer.music.play(-1)

class Player(pygame.sprite.Sprite):
    # player sprite
    # realistic movement using equations of motion (pos, vel, accel)
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pygame.math.Vector2(WIDTH/2, HEIGHT/2)
        self.vel = pygame.math.Vector2(0, 0)
        self.accel = pygame.math.Vector2(0, 0)
        self.image = pygame.Surface((24, 24))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

    def update(self):
        self.accel = pygame.math.Vector2(0, 0)
        # keep accelerating as long as that dir key is down
        keystate = pygame.key.get_pressed()
        a = 1.5
        if FPS == 65:
            a = 0.7
        if keystate[pygame.K_LEFT]:
            self.accel.x = -a
        if keystate[pygame.K_RIGHT]:
            self.accel.x = a
        if keystate[pygame.K_UP]:
            self.accel.y = -a
        if keystate[pygame.K_DOWN]:
            self.accel.y = a
        if keystate[pygame.K_LSHIFT]:
            var = self.accel
        # fix diagonals so they are same speed as orthoganal directions
        if self.accel.x != 0 and self.accel.y != 0:
            self.accel *= 0.7071

        # friction (based on vel)
        self.accel += self.vel * -0.12
        # grav example (not going to use in this game, but fun to see)
        # self.accel.y += .7

        # equations of motion
        # for simplicity, using t=1 (change per timestep)
        # p' = 0.5 at**2 + vt + p
        # v' = at + v
        # Player speed
        self.vel += self.accel
        self.pos += self.accel * 3 + self.vel

        # move the sprite
        self.rect.x = int(self.pos.x)
        self.check_collisions('x')
        self.rect.y = int(self.pos.y)
        self.check_collisions('y')

    def check_collisions(self, dir):
        if dir == 'x':
            hit_list = pygame.sprite.spritecollide(self, g.walls, False)
            if hit_list:
                if self.vel.x > 0:
                    self.vel.x = 0
                    self.pos.x = hit_list[0].rect.left - self.rect.width
                    self.rect.right = hit_list[0].rect.left
                elif self.vel.x < 0:
                    self.vel.x = 0
                    self.pos.x = hit_list[0].rect.right
                    self.rect.left = hit_list[0].rect.right
        elif dir == 'y':
            hit_list = pygame.sprite.spritecollide(self, g.walls, False)
            if hit_list:
                if self.vel.y > 0:
                    self.vel.y = 0
                    self.pos.y = hit_list[0].rect.top - self.rect.height
                    self.rect.bottom = hit_list[0].rect.top
                elif self.vel.y < 0:
                    self.vel.y = 0
                    self.pos.y = hit_list[0].rect.bottom
                    self.rect.top = hit_list[0].rect.bottom
                self.speed_y = 0

    @classmethod
    def shape(cls, param):
        pass


class Box(pygame.sprite.Sprite):
    # simple static box
    # TODO: moving boxes?
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((24, 24))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Mob(pygame.sprite.Sprite):
    # bad guy!
    # will chase the player
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((24, 24))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.accel = pygame.math.Vector2(0, 0)
        # varied speeds (actually acceleration, but determines max speed)
        # TODO: different types of enemy based on speed?
        self.speed = random.choice([0.3, 0.4])
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

    def update(self):
        # friction (based on vel)
        self.accel += self.vel * -0.09

        # equations of motion - see Player class
        self.pos += self.accel * 0.5 + self.vel
        self.vel += self.accel

        # move the sprite
        self.rect.x = int(self.pos.x)
        self.check_collisions('x')
        self.rect.y = int(self.pos.y)
        self.check_collisions('y')

    def check_collisions(self, dir):
        if dir == 'x':
            hit_list = pygame.sprite.spritecollide(self, g.walls, False)
            if hit_list:
                if self.vel.x > 0:
                    self.vel.x = 0
                    self.pos.x = hit_list[0].rect.left - self.rect.width
                    self.rect.right = hit_list[0].rect.left
                elif self.vel.x < 0:
                    self.vel.x = 0
                    self.pos.x = hit_list[0].rect.right
                    self.rect.left = hit_list[0].rect.right
        elif dir == 'y':
            hit_list = pygame.sprite.spritecollide(self, g.walls, False)
            if hit_list:
                if self.vel.y > 0:
                    self.vel.y = 0
                    self.pos.y = hit_list[0].rect.top - self.rect.height
                    self.rect.bottom = hit_list[0].rect.top
                elif self.vel.y < 0:
                    self.vel.y = 0
                    self.pos.y = hit_list[0].rect.bottom
                    self.rect.top = hit_list[0].rect.bottom


class Wall(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()

    def new(self):
        # initialize for a new game
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.boxes = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.level = 1
        self.score = 0
        self.create_walls()
        self.create_enemies()
        self.create_boxes()

    def load_data(self):
        # load image and sound data
        game_dir = os.path.dirname(__file__)
        img_dir = os.path.join(game_dir, "img")
        wall_images = ["brick_blue32.png",
                       "brick_green32.png",
                       "brick_red32.png"]
        self.wall_images = []
        for img in wall_images:
            filename = os.path.join(img_dir, img)
            self.wall_images.append(pygame.image.load(filename).convert())

        # load level data from txt file
        self.level_data = [[]]
        with open(os.path.join(game_dir, "levels.txt"), 'rt') as f:
            lines = f.read().splitlines()
        for line in lines:
            if line[0] == ":":
                level = int(line[1])
                self.level_data.append([])
            else:
                self.level_data[level].append(line)

    def create_walls(self):
        # load level based on self.level
        # empty any old walls before creating new ones
        if self.level == len(self.level_data):
            self.running = False
        else:
            for wall in self.walls:
                self.all_sprites.remove(wall)
            self.walls.empty()
            img = random.choice(self.wall_images)
            for row, tiles in enumerate(self.level_data[self.level]):
                for col, tile in enumerate(tiles):
                    if tile == '1':
                        wall = Wall(img, col*16, row*32)
                        self.all_sprites.add(wall)
                        self.walls.add(wall)

    def create_enemies(self):
        # create number/type of enemies based on self.level
        self.enemies.empty()
        for i in range(self.level // 2):
            enemy = Mob(random.choice([35, WIDTH-60]),
                        random.choice([35, HEIGHT-60]))
            self.enemies.add(enemy)

    def create_boxes(self):
        # create number/type of boxes based on self.level
        self.boxes.empty()
        for i in range(self.level * 5):
            box = Box(random.randrange(35, WIDTH-59),
                      random.randrange(35, HEIGHT-59))
            # keep trying locs until we find an open one
            while pygame.sprite.spritecollide(box, self.walls, False):
                box.rect.topleft = (random.randrange(35, WIDTH-59),
                                    random.randrange(35, HEIGHT-59))
            self.boxes.add(box)
            self.all_sprites.add(box)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()  # check for events
            self.update()  # update the game state
            self.draw()    # draw the next frame

    def quit(self):
        pygame.quit()
        sys.exit()

    def events(self):
        # handle all events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()

    def update(self):
        # collide player w/boxes and remove them
        hit_list = pygame.sprite.spritecollide(self.player, self.boxes, True)
        self.score += len(hit_list)

        # if we level up
        if len(self.boxes) == 0:
            self.level += 1
            self.create_walls()
            self.create_boxes()
            self.create_enemies()
            self.player.vel = pygame.math.Vector2(0, 0)
            self.player.pos = pygame.math.Vector2(WIDTH/2, HEIGHT/2)

        # move mobs toward player
        for enemy in self.enemies:
            enemy.accel = pygame.math.Vector2(self.player.pos.x - enemy.pos.x,
                               self.player.pos.y - enemy.pos.y)
            enemy.accel = enemy.accel * (enemy.speed / enemy.accel.length())
            if pygame.sprite.collide_rect(enemy, self.player):
                self.running = False

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.update()
        self.enemies.update()
        self.all_sprites.draw(self.screen)
        self.enemies.draw(self.screen)
        score_txt = "Score: {:0}".format(self.score)
        self.draw_text(score_txt, 18, 33, 33)
        lvl_txt = "Level: {:0}".format(self.level)
        self.draw_text(lvl_txt, 18, 33, 53)
        # uncommment to show FPS (useful for troubleshooting)
        fps_txt = "{:.2f}".format(self.clock.get_fps())
        self.draw_text(str(fps_txt), 18, WIDTH-50, 10)
        pygame.display.flip()

    def draw_text(self, text, size, x, y):
        # utility function to draw text on screen
        font_name = pygame.font.match_font('arial')
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def start_screen(self):
        pass

    def go_screen(self):
        pass


game_over = True
running = True


def show_go_screen():



 while running:
    if game_over:
        show_go_screen()
        game_over = False
    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT():
            running = False

    def go_screen(self):
        pass

    def start_screen(self):
        pass

g = Game()


class GameMenu(object):
    pass


while True:
    g.new()
    g.run()
    g.go_screen()
