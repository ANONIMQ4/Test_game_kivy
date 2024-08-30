from configure import *
import random
import math
from kivy.config import Config
from kivy.core.image import Image as CoreImage
from kivy.uix.button import Button

Clock._max_fps = 100
window = Window()


def draw_item(item): game.draw(item)


class PongApp(App):
    def build(self):
        Clock.schedule_interval(game.update, 0)
        return game


class Game(Widget):
    def __init__(self):
        super(Game, self).__init__()
        self.current_score = 0
        self.game_state = 'start_menu'
        self.game_time = 'day'
        self.touch_block = False
        self.pause = False

    def draw(self, item):
        self.add_widget(item)

    def update(self, dt):
        Update()

    def Touch_block(self, *args):
        self.touch_block = True

    def Un_Touch_block(self, *args):
        self.touch_block = False

    def set_pause(self, *args):
        self.Touch_block()
        self.pause = True - self.pause

    def del_all(self):
        try:
            game.remove_widget(pause_button)
            game.remove_widget(to_main_button)
            game.remove_widget(main_menu)
            game.remove_widget(label_lose)
            game.remove_widget(start_free_game_button)
            game.remove_widget(start_story_game_button)
        except:
            pass

    def set_default_st(self):
        self.pause = False
        main_ball.pos = absolute_num(cord=(50, 90))
        main_ball.update_canvas(main_ball.pos, main_ball.size)
        self.game_time = 'day'
        st_object.pos_x = window.wight
        st_object.siz = window.wight * 0.3
        st_object.pos_y = window.height * 0.6
        st_object.color_a = 0.02
        st_object.color_b = 0.51
        st_object.color_c = 0.62
        st_object.color_border = 1

    def to_main(self, *args):
        global current_borders
        self.Touch_block()
        try:
            game.remove_widget(main_ball)
            game.remove_widget(ball_light)
            game.remove_widget(st_object)
            game.remove_widget(pause_button)
            for border in current_borders:
                game.remove_widget(border)
            current_borders = []
            self.current_score = 0
        except:
            pass

        game.game_state = 'start_menu'
        game.remove_widget(to_main_button)
        self.set_default_st()
        draw_item(start_free_game_button)

    def start_free_game(self, *args):
        self.game_state = 'level'
        First_draw()
        self.del_all()

    def start_story_game(self,*args):
        self.game_state = 'story_game_0'
        self.del_all()
        #print('as')


    def on_touch_up(self, touch):
        if not self.touch_block:
            if self.game_state in ['lose']:
                if self.game_state == 'lose':
                    self.set_default_st()
                self.game_state = 'level'
                First_draw()
            if self.game_state == 'level':
                main_ball.on_touch_up(touch)

    def time_update(self):
        if self.game_time == "day":
            self.game_time = 'night'
            st_object.update_canvas()
        else:
            self.game_time = 'day'
            st_object.update_canvas()

    def check_game_state(self):
        self.del_all()
        if self.game_state == 'level':
            if not self.pause:
                main_ball.move()
                st_object.move()
                move_borders()
                game.remove_widget(ball_light)
                draw_item(ball_light)
                ball_light.update_canvas()
            try:
                draw_item(pause_button)
            except:
                pass
            if game.pause:
                try:
                    draw_item(to_main_button)
                except:
                    pass

        if self.game_state == 'lose':
            try:
                draw_item(label_lose)
            except:
                pass
            global current_borders
            try:
                game.remove_widget(main_ball)
                game.remove_widget(ball_light)
                game.remove_widget(st_object)
                for border in current_borders:
                    game.remove_widget(border)
                current_borders = []
                self.current_score = 0
            except:
                pass
        if self.game_state == 'start_menu':
            try:
                draw_item(main_menu)
                main_menu.update_canvas()
            except:
                pass
            try:
                draw_item(start_free_game_button)
                draw_item(start_story_game_button)
            except:
                pass
        if self.game_state == 'story_game_0':
            draw_item(to_main_button)
            try:
                draw_item(level_menu)
                draw_level_list()

            except:
                pass


def absolute_num(**kwargs):
    if 'size' in kwargs:
        num_1, num_2 = list(kwargs['size'])
        return num_1 / 100 * window.wight, num_2 / 100 * window.height
    if 'cord' in kwargs:
        num_1, num_2 = list(kwargs['cord'])
        return num_1 / 100 * window.wight, num_2 / 100 * window.height
    if 'num_x' in kwargs:
        return kwargs['num_x'] * window.wight / 100
    if 'num_y' in kwargs:
        return kwargs['num_y'] * window.height / 100


game = Game()
debug = False
border_img = CoreImage('border.png').texture
ball_img = CoreImage('ball.png').texture
ball_night_img = CoreImage('ball_.png').texture
horizont_img = CoreImage('horizont.png').texture
sun_img = CoreImage('sun.png').texture
luna_img = CoreImage('luna.png').texture
infinite_mode = CoreImage('infinite_mode.png').texture


class Ball(Widget):
    def __init__(self, **kwargs):
        super(Ball, self).__init__(**kwargs)
        self.pos_x = list(kwargs['pos'])[0]
        self.pos_y = list(kwargs['pos'])[1]
        self.size = list(kwargs['size'])[0], list(kwargs['size'])[0]
        self.update_canvas((self.pos_x, self.pos_y), kwargs['size'])
        self.move_ball = 0
        self.speed_rotate = 1 * 60 / Clock._max_fps
        self.speed_fall = 0.05 * 60 / Clock._max_fps
        self.collision_with_border = False
        self.right_block = False
        self.left_block = False
        self.down_block = False

    def check_collision(self, pos, size):
        border_x = list(pos)[0]
        border_y = list(pos)[1]
        border_wight = list(size)[0]
        border_height = list(size)[1]
        border_y = list(pos)[1]
        if self.pos_y > border_y + border_height or self.pos_y + list(self.size)[0] < border_y: pass
        #return False
        ball_center_x = self.pos_x + 0.5 * list(self.size)[0]
        ball_center_y = self.pos_y + 0.5 * list(self.size)[0]

        if border_x <= ball_center_x <= border_x + border_wight:
            if border_y <= self.pos_y <= border_y + border_height:
                self.down_block = True
                self.pos_y = border_y + border_height - absolute_num(num_y=0.5)
                return True
        if ball_center_y > border_y + border_height:
            if abs(math.dist([ball_center_x, ball_center_y], [border_x + border_wight, border_y + border_height]) -
                   list(self.size)[0] / 2) < (absolute_num(num_x=0.9) + absolute_num(num_y=0.9)) / 2:
                self.down_block = True
                self.left_block = True
                self.pos_x += abs(
                    math.dist([ball_center_x, ball_center_y], [border_x + border_wight, border_y + border_height]) -
                    list(self.size)[0] / 2)

            if abs(math.dist([ball_center_x, ball_center_y], [border_x, border_y + border_height]) - list(self.size)[
                0] / 2) < (absolute_num(num_x=0.9) + absolute_num(num_y=0.9)) / 2:
                self.down_block = True
                self.right_block = True
                self.pos_x -= abs(
                    math.dist([ball_center_x, ball_center_y], [border_x, border_y + border_height]) - list(self.size)[
                        0] / 2)
                return True
        if border_y <= ball_center_y <= border_y + border_height:
            if border_x + border_wight >= self.pos_x > border_x:
                self.left_block = True
                self.pos_x += border_x + border_wight - self.pos_x
                return True
            if border_x <= self.pos_x + list(self.size)[0] / 2 < border_x + border_wight:
                self.right_block = True
                self.pos_x -= self.pos_x + list(self.size)[0] / 2 - border_x
                return True

        return False

    def on_touch_down(self, touch):
        if list(touch.pos)[0] > window.wight / 2:
            self.move_ball = 1
        else:
            self.move_ball = -1

    def on_touch_up(self, touch):
        self.move_ball = 0

    def move(self):
        if self.pos_y + list(self.size)[0] >= window.height:
            game.game_state = 'lose'
        self.right_block = self.left_block = self.down_block = False
        for border in current_borders:
            if self.check_collision(border.pos, border.size):
                break
        if self.pos_y > 0 and not self.down_block:
            self.pos_y -= absolute_num(num_y=self.speed_fall)
        if self.down_block:
            self.pos_y += absolute_num(num_y=0.3)
        if (self.move_ball > 0 and not self.right_block) or (self.move_ball < 0 and not self.left_block):
            self.pos_x += self.move_ball * absolute_num(num_x=self.speed_rotate)
        self.update_canvas((self.pos_x, self.pos_y), self.size)

    def update_canvas(self, pos, size):
        self.canvas.clear()
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        with self.canvas:
            if game.game_time == "day":
                Color(1, 1, 1)
                Rectangle(pos=pos, size=size, texture=ball_img)
            else:
                Rectangle(pos=pos, size=size, texture=ball_img)


class Ball_Light(Widget):
    def __init__(self):
        super(Ball_Light, self).__init__()
        self.update_canvas()

    def update_canvas(self):
        self.canvas.clear()
        with self.canvas:
            if game.game_time == "night":
                Rectangle(pos=(main_ball.pos_x - main_ball.size[0], main_ball.pos_y - main_ball.size[0]),
                          size=(main_ball.size[0] * 3, main_ball.size[0] * 3), texture=ball_night_img,
                          color=Color(1, 1, 1))


class Border(Widget):
    def __init__(self, **kwargs):
        super(Border, self).__init__(**kwargs)
        self.pos_x = list(kwargs['pos'])[0]
        self.pos_y = list(kwargs['pos'])[1]
        self.pos = (self.pos_x, self.pos_y)
        self.size = kwargs['size']
        self.update_canvas()
        self.speed_up = (0.2 + math.sqrt(game.current_score * 0.0008)) * 60 / Clock._max_fps

    def move(self):
        self.pos_y += absolute_num(num_y=self.speed_up)
        self.pos = (self.pos_x, self.pos_y)
        self.speed_up = (0.2 + math.sqrt(game.current_score * 0.0008)) * 60 / Clock._max_fps
        self.update_canvas()

    def update_canvas(self):
        self.canvas.clear()
        with self.canvas:

            if self.pos_x != 0:
                Rectangle(pos=(self.pos_x - absolute_num(num_x=3), self.pos_y),
                          size=(window.wight, window.wight / 1539 * 400), texture=border_img,
                          color=Color(st_object.color_border, st_object.color_border, st_object.color_border))
            else:
                Rectangle(pos=(list(self.size)[0] - window.wight + absolute_num(num_x=3), self.pos_y),
                          size=(window.wight, window.wight / 1539 * 400), texture=border_img,
                          color=Color(st_object.color_border, st_object.color_border, st_object.color_border))


class Stable_object(Widget):
    def __init__(self):
        super(Stable_object, self).__init__()
        self.pos_x = window.wight
        self.siz = window.wight * 0.3
        self.pos_y = window.height * 0.6
        self.color_a = 0.02
        self.color_b = 0.51
        self.color_c = 0.62
        self.color_border = 1
        self.color = Color(self.color_a, self.color_b, self.color_c)
        self.lite_color = Color(self.color_a, self.color_b + 0.1, self.color_c + 0.1)
        self.update_canvas()

    def move(self):
        self.pos_x -= absolute_num(num_x=0.05) * 60 / Clock._max_fps
        if self.pos_x > (window.wight - self.siz) / 2:
            self.pos_y += absolute_num(num_y=0.01)
        else:
            self.pos_y -= absolute_num(num_y=0.01)
        if self.pos_x <= 0:
            if game.game_time == "day":
                self.color_b -= (0.51 - 0.01) * absolute_num(num_x=0.05) / (
                        (window.wight - self.siz) / 2) * 60 / Clock._max_fps
                self.color_c -= (0.62 - 0.05) * absolute_num(num_x=0.05) / (
                        (window.wight - self.siz) / 2) * 60 / Clock._max_fps
                self.color_border -= (1) * absolute_num(num_x=0.05) / (
                        (window.wight - self.siz) / 2) * 60 / Clock._max_fps
                #Color(0.02, 0.1, 0.2)
            else:
                self.color_b += (0.51 - 0.01) * absolute_num(num_x=0.05) / (
                        (window.wight - self.siz) / 2) * 60 / Clock._max_fps
                self.color_c += (0.62 - 0.05) * absolute_num(num_x=0.05) / (
                        (window.wight - self.siz) / 2) * 60 / Clock._max_fps
                self.color_border += (1) * absolute_num(num_x=0.05) / (
                        (window.wight - self.siz) / 2) * 60 / Clock._max_fps
        self.color = Color(self.color_a, self.color_b, self.color_c)
        self.lite_color = Color(self.color_a, self.color_b + 0.1, self.color_c + 0.1)

        if self.pos_x <= -self.siz:
            self.pos_y = window.height * 0.6
            self.pos_x = window.wight
            game.time_update()
        self.update_canvas()

    def update_canvas(self):
        self.canvas.clear()
        with self.canvas:
            self.color = Color(self.color_a, self.color_b, self.color_c)
            Rectangle(pos=(0, 0), size=(window.wight, window.height),
                      color=self.color)
            if game.game_time == 'night':
                Rectangle(pos=(-window.wight, -window.wight * 2),
                          size=(window.wight * 3, window.wight * 3),
                          texture=horizont_img, color=self.lite_color)
            if game.game_time == "day":
                Rectangle(pos=(self.pos_x, self.pos_y),
                          size=(window.wight * 0.3, window.wight * 0.3),
                          texture=sun_img,
                          color=Color(1, 1, 1))
            else:
                Rectangle(pos=(self.pos_x, self.pos_y),
                          size=(window.wight * 0.3, window.wight * 0.3),
                          texture=luna_img,
                          color=Color(1, 1, 1))


class Main_menu(Widget):
    def __init__(self):
        super(Main_menu, self).__init__()
        self.pos_inf_button = (0, window.height * 0.5)
        self.pos_story_button = (0, window.height * 0.25)
        self.update_canvas()

    def update_canvas(self):
        self.canvas.clear()
        with self.canvas:
            Rectangle(pos=(0, 0), size=(window.wight, window.height), color=Color(1, 1, 1))


class Level_button(Widget):
    def __init__(self, Id, x_l, y_l):
        super(Level_button,self).__init__()
        self.id = Id
        self.x_l = x_l
        self.y_l = y_l
        self.padding_x = 0
        self.padding_y = 0
        self.pos = (1,1)
        self.size = (1,1)
        self.color = Color(0.5, 0.5, 0.5)
        self.count_cord()
        self.update_canvas()

    def count_cord(self):
        self.size = (window.wight*0.2,window.wight*0.2)
        self.padding_x = (window.wight - self.size[0]*self.x_l)/(self.x_l+3)
        self.padding_y = (window.height - self.size[0]*self.y_l)/(self.y_l+5)
        self.pos = (self.padding_x*(2+(self.id-1)%self.x_l)+ (self.id-1)%self.x_l*self.size[0],self.padding_y*(3+(self.id-1)//self.x_l)+ (self.id-1)//self.x_l*self.size[0])

    def update_canvas(self):
        self.canvas.clear()
        with self.canvas:
            print(self.pos, self.size)
            Rectangle(pos=self.pos, size=self.size, color=Color(0.5, 0.5, 0.5))



class Level_menu(Widget):
    def __init__(self):
        super(Level_menu, self).__init__()
        self.x_l = 3
        self.y_l = 5
        self.buttons = []
        self.update_canvas()

    def update_canvas(self):
        self.canvas.clear()
        with self.canvas:
            counter = 0
            Rectangle(pos=(0, 0), size=(window.wight, window.height), color=Color(1, 1, 1))


def draw_level_list():
    counter = 0
    try:
        for button in level_menu.buttons:
            game.remove_widget(button)
        game.remove_widget(to_main_button)
        level_menu.buttons = []
    except:pass
    for y in range(level_menu.y_l):
        for x in range(level_menu.x_l):
            counter += 1
            current_l_button = Level_button(counter, level_menu.x_l, level_menu.y_l)
            level_menu.buttons.append(current_l_button)
            draw_item(current_l_button)
            current_l_button.update_canvas()
    draw_item(to_main_button)
    level_menu.buttons.append(to_main_button)

main_menu = Main_menu()
draw_item(main_menu)
main_ball = Ball(pos=absolute_num(cord=(50, 90)), size=absolute_num(size=(15, 15)))
ball_light = Ball_Light()
st_object = Stable_object()
level_menu = Level_menu()
label_lose = Label(text='Нажмите чтобы начать заново',
                   pos=(0, window.height * 0.4),
                   size=(window.wight, window.height * 0.2))
start_free_game_button = Button(on_press=game.start_free_game,
                                on_release=game.Un_Touch_block,
                                size=(window.wight, window.height * 0.2),
                                pos=main_menu.pos_inf_button,
                                background_normal='infinite_mode.png')
start_story_game_button = Button(on_press=game.start_story_game,
                                on_release=game.Un_Touch_block,
                                size=(window.wight, window.height * 0.2),
                                pos=main_menu.pos_story_button,
                                background_normal='story_mode.png')

pause_button = Button(text='Пауза',
                      font_size=24,
                      on_press=game.set_pause,
                      on_release=game.Un_Touch_block,
                      size=(absolute_num(num_x=15), absolute_num(num_x=15)),
                      pos=(absolute_num(num_x=1), window.height - absolute_num(num_x=16)))
to_main_button = Button(text='Выход',
                        font_size=24,
                        on_press=game.to_main,
                        on_release=game.Un_Touch_block,
                        size=(absolute_num(num_x=15), absolute_num(num_x=15)),
                        pos=(absolute_num(num_x=17), window.height - absolute_num(num_x=16)))


def Update():
    game.check_game_state()


current_borders = []


def move_borders():
    for border in current_borders:
        border.move()
        if border.pos_y > window.height + absolute_num(num_y=20):
            game.remove_widget(border)
            if border.pos_x == 0:
                game.current_score += 1
                to_down = (min(-random.randint(int(absolute_num(num_y=1 / 7 * 100)),
                                               int(absolute_num(num_y=2 / 7 * 100))) + min(
                    [i.pos_y for i in current_borders]), -int(absolute_num(num_y=4))))
                current_b = random.randint(int(absolute_num(num_x=20)), int(absolute_num(num_x=25)))
                left_padding = random.randint(0, int(absolute_num(num_x=75)))
                border_l = Border(pos=(0, to_down), size=(left_padding, absolute_num(num_y=3)))
                border_r = Border(pos=(left_padding + current_b, to_down),
                                  size=(window.wight, absolute_num(num_y=3)))
                draw_item(border_l)
                draw_item(border_r)
                current_borders.append(border_l)
                current_borders.append(border_r)
            current_borders.remove(border)


def draw_borders():
    n = 7
    for i in range(n):
        current_b = random.randint(int(absolute_num(num_x=20)), int(absolute_num(num_x=25)))
        left_padding = random.randint(0, int(absolute_num(num_x=75)))
        border_l = Border(pos=(0, -i * absolute_num(num_y=1 / n * 100)),
                          size=(left_padding, absolute_num(num_y=3)))
        border_r = Border(pos=(left_padding + current_b, -i * absolute_num(num_y=1 / n * 100)),
                          size=(window.wight, absolute_num(num_y=3)))
        draw_item(border_l)
        draw_item(border_r)
        current_borders.append(border_l)
        current_borders.append(border_r)


def First_draw():
    try:
        draw_item(st_object)
    except:
        pass
    draw_item(main_ball)
    draw_item(ball_light)
    draw_borders()

    if debug:
        draw_item(Label(text=f'{window.height} {window.wight}',
                        padding=[window.wight * 1.8, 0, 0, window.height * 1.8]))


if __name__ == '__main__':
    PongApp().run()
