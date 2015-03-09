import pygame
import math
from pygame.locals import *
import random
import time
import planes
from planes import Plane
import planes.gui
from planes import *


BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


class Screen:
	def __init__(self, buttons, actors, background):
		self.buttons = buttons
		self.actors = actors
		self.background = background

	def update(self):
		for actor in self.actors:
			actor.update()

class Button(gui.Button):
	def __init__(self, label, rect, callback, model):
		gui.Button.__init__(self, label, rect, callback)
		planes.Plane.__init__(self,label,rect,draggable=False, grab=False)
		self.image.fill(WHITE)
		self.rect = rect
		self.model = model
	def update(self):
		pass

class DropDisplay(planes.Display):
    def dropped_upon(self, plane, coordinates):
         if isinstance(plane, planes.Plane):
             planes.Display.dropped_upon(self, plane, (plane.Xpos, plane.Ypos))

class ScreenText(gui.Label):
	def __init__ (self, name, text, rect, font):
		planes.Plane.__init__ (self, name, rect, False, False)

		self.background_color = (0,0,0,0)
		self.text_color = WHITE

		gui.Label.__init__(self, name, text, rect, self.background_color, self.text_color, font)
	
	def update_text(self, text):
		self.text = text

	def update_color(self, color):
		#print color
		self.text_color = color

	def update_background(self, color):
		self.background_color = color

