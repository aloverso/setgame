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
BACKGROUND_COLOR = (150,150,150)


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
             planes.Display.dropped_upon(self, plane, (plane.rect.x, plane.rect.y))

class DropZone(planes.Plane):
    def __init__(self, name, rect):
        planes.Plane.__init__(self, name, rect, draggable = False, grab = True)
        self.name = name
        self.image.fill((0,0,255))
        self.rect = rect
        self.thingsDroppedOnMe = []

    def dropped_upon(self, plane, coordinates):
        planes.Plane.dropped_upon(self, plane, (coordinates[0]+self.rect.x, coordinates[1]+self.rect.y))
        plane.moving = False
      	self.thingsDroppedOnMe.append(plane)

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

def draw_border(plane, color):
    """Draw a border around plane.
    """
    pygame.draw.lines(plane.image,
                      color,
                      True,
                      ((0, 0),
                       (plane.rect.width - 1, 0),
                       (plane.rect.width - 1, plane.rect.height - 1),
                       (0, plane.rect.height - 1)))

    return

class ScrollingPlane(planes.Plane):
    """This class implements a fixed-dimension plane with a scroll bar to scroll its content plane.
       Subplane structure:

       ScrollingPlane
       |
       +---content
       |   |
       |   +---content_plane from __init__()
       |
       +---scrollbar_container
           |
           +---scrollbar
    """

    def __init__(self, name, rect, content_plane, draggable = False, grab = False, clicked_callback = None, dropped_upon_callback = None):
        """Initalise.
           rect states the dimensions without the scroll bar.
        """

        rect.width = rect.width + 12

        # Call base class
        #
        planes.Plane.__init__(self, name, rect, draggable, grab, clicked_callback, dropped_upon_callback)

        self.image.fill(BACKGROUND_COLOR)

        self.sub(planes.Plane("content", pygame.Rect((0, 0),
                                                         (self.rect.width - 12, self.rect.height))))

        content_plane.rect.topleft = (0, 0)
        self.content.sub(content_plane)

        scrollbar_container = planes.Plane("scrollbar_container",
                                               pygame.Rect((self.rect.width - 12, 0),
                                                           (12, self.rect.height)))

        scrollbar_container.image.fill(BACKGROUND_COLOR)
        draw_border(scrollbar_container, (0, 0, 0))

        def scrollbar_container_clicked(plane):
            """Clicked callback which repositions the content Plane and scrollbar according to the y-position of the mouse.
            """
            x, y = pygame.mouse.get_pos()

            new_y = y - self.rect.top

            # Align scrollbar at bottom
            #
            if new_y > self.rect.height - self.scrollbar_container.scrollbar.rect.height - 2:
                new_y = self.rect.height - self.scrollbar_container.scrollbar.rect.height - 2

            self.scrollbar_container.scrollbar.rect.top = new_y

            content_plane = self.content.subplanes[self.content.subplanes_list[0]]
            content_plane.rect.top = int(0 - new_y / self.rect.height * content_plane.rect.height)

            return

        scrollbar_container.clicked_callback = scrollbar_container_clicked

        self.sub(scrollbar_container)

        # Scrollbar height reflects the proportions
        #
        self.scrollbar_container.sub(planes.Plane("scrollbar", pygame.Rect((2, 2),
                                                                          (8, int(self.rect.height / content_plane.rect.height * self.rect.height)))))

        # Half-bright color taken from Button.clicked()
        #
        self.scrollbar_container.scrollbar.image.fill(list(map(lambda i : int(i * 0.5), BACKGROUND_COLOR)))

        return

