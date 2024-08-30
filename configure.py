import kivy

from kivy.clock import Clock
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.vector import Vector
from kivy.uix.widget import Widget
from kivy.core.window import Window as wind
from kivy.config import Config

Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '800')
Config.write()

from kivy.graphics import Color, Ellipse, Rectangle

class Window():
    def __init__(self):
        self.height = list(wind.size)[1]
        self.wight = list(wind.size)[0]

