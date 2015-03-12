import pygame
import math
from pygame.locals import *
import random
import time
from abc import ABCMeta, abstractmethod
import planes
from planes import Plane
import planes.gui

from class_utils import Screen
from class_utils import Button
from class_utils import DropDisplay
from class_utils import ScreenText
from class_utils import DropZone

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

CARD_WIDTH = 200
CARD_HEIGHT = 100

top_margin = 50
left_margin = 50

space_horiz = ((3*WINDOW_WIDTH/4)-2*left_margin-3*CARD_WIDTH)/2

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255,0,0)

HOME = 0
GAME = 1

NOTIME = 0
EASY = 1
MEDIUM = 2
HARD = 3

colors = ['green', 'red', 'purple']
shapes = ['oval', 'diamond', 'squiggle']
numbers = [1,2,3]
shades = ['filled','shaded', 'empty']

def check_set (card1, card2, card3):
	color_check = all_same_or_all_diff (card1.color, card2.color, card3.color)
	shape_check = all_same_or_all_diff (card1.shape, card2.shape, card3.shape)
	num_check = all_same_or_all_diff (card1.number, card2.number, card3.number)
	shade_check = all_same_or_all_diff (card1.shade, card2.shade, card3.shade)
	return color_check and shape_check and num_check and shade_check

def all_same_or_all_diff (attr1, attr2, attr3):
	if attr1 == attr2 and attr2 == attr3:
		return True
	elif (attr1 != attr2) and (attr2 != attr3) and (attr3 != attr1):
		return True
	else:
		return False

def format_secs (secs):
	minutes = secs / 60
	seconds = secs % 60
	return str (minutes) + "m " + str (seconds) + "s"

class Card (planes.Plane):
	def __init__ (self, name, color, shape, number, shade):
		planes.Plane.__init__ (self, name, pygame.Rect (0,0,CARD_WIDTH,CARD_HEIGHT), False, False)
		self.color = color
		self.shape = shape
		self.number = number
		self.shade = shade
		self.been_clicked = False
		
	def __eq__ (self, other):
		return  self.color == other.color and \
				self.shape == other.shape and \
				self.number == other.number and \
				self.shade == other.shade

	def __ne__ (self, other):
		return not self.__eq__(other)
	
	def clicked (self, button_name):
		self.been_clicked = not self.been_clicked

	def update (self):
		pass

class TimeBox (planes.Plane):
	def __init__ (self, name, rect, speed):
		planes.Plane.__init__ (self, name, rect, False, False)
		# time is time for box to move to bottom of screen in seconds
		self.speed = speed
		self.image.fill ((100,100,100))

	def update (self):
		print "i go down"
		if self.rect.y < 0:
			self.rect.y += self.speed

class AddThreeCardsButton (Button):
	def __init__(self, name, rect, callback, model):
		Button.__init__ (self, name, rect, callback, model)
		self.image = pygame.image.load ("img/plus3_icon.png")

	def clicked (self, button_name):
		if self.model.paused_time_at == 0:
			if not self.model.check_if_any_sets:
				self.model.add_new_cards (3)

class HintButton (Button):
	def __init__(self, name, rect, callback, model):
		Button.__init__ (self, name, rect, callback, model)
		self.image = pygame.image.load ("img/hint_icon.png")

	def clicked (self, button_name):
		if self.model.paused_time_at == 0:
			if (self.model.hints_left > 0):
				self.model.hints_left -= 1
				for card1 in self.model.in_play_cards:
						for card2 in self.model.in_play_cards:
							for card3 in self.model.in_play_cards:
								if card1 != card2 and card2 != card3 and card1 != card3:
									if check_set (card1, card2, card3):
										if not card1.been_clicked:
											card1.been_clicked = True
											return
										elif not card2.been_clicked:
											card2.been_clicked = True
											return
										else:
											card3.been_clicked = True
											return
				self.model.add_new_cards (3)

class BackButton (Button):
	def __init__(self, name, rect, callback, model):
		Button.__init__ (self, name, rect, callback, model)
		self.image = pygame.image.load ("img/back_icon.png")

	def clicked (self, button_name):
		self.model.model.game = None
		self.model.model.mode = HOME

class PauseButton (Button):
	def __init__(self, name, rect, callback, model):
		Button.__init__ (self, name, rect, callback, model)
		self.image = pygame.image.load ("img/pause_icon.png")

	def clicked (self, button_name):
		if self.model.paused_time_at != 0: # game is already paused, act as play button
			self.model.pause_time += pygame.time.get_ticks () - self.model.paused_time_at
			self.model.paused_time_at = 0
		else:
			self.model.paused_time_at = pygame.time.get_ticks ()

class PlayButton (Button):
	def __init__(self, name, rect, callback, model):
		Button.__init__ (self, name, rect, callback, model)
		self.image = pygame.image.load ("img/start_icon.png")

	def clicked (self, button_name):
		if self.model.check_if_won () or self.model.check_if_lost (): # if game over act as restart button
			self.model.model.game = None
			self.model.model.game = Game (self.model.model.game_select, self.model.model)
		else:
			self.model.pause_time += pygame.time.get_ticks () - self.model.paused_time_at
			self.model.paused_time_at = 0


class RestartButton (Button):
	def __init__(self, name, rect, callback, model):
		Button.__init__ (self, name, rect, callback, model)
		self.image = pygame.image.load ("img/restart_icon.png")

	def clicked (self, button_name):
		self.model.model.game = None
		self.model.model.game = Game (self.model.model.game_select, self.model.model)

class StartButton (Button):
	### Starts a NEW game
	def __init__(self, name, rect, callback, model):
		Button.__init__ (self, name, rect, callback, model)
		self.image = pygame.image.load ("img/start_icon.png")
		self.clickbox = False

	def clicked (self, button_name):
		self.model.mode = GAME
		self.model.game = Game (self.model.game_select, self.model)

class NoTimeButton (Button):
	def __init__(self, name, rect, callback, model):
		Button.__init__ (self, name, rect, callback, model)
		self.image = pygame.image.load ("img/notime_icon.png")
		self.clickbox = True

	def clicked (self, button_name):
		self.model.game_select = NOTIME
		for button in self.model.homebuttons:
			button.clickbox = False
		self.clickbox = True

class EasyButton (Button):
	def __init__(self, name, rect, callback, model):
		Button.__init__ (self, name, rect, callback, model)
		self.image = pygame.image.load ("img/easy_icon.png")
		self.clickbox = False

	def clicked (self, button_name):
		self.model.game_select = EASY
		for button in self.model.homebuttons:
			button.clickbox = False
		self.clickbox = True

class MedButton (Button):
	def __init__(self, name, rect, callback, model):
		Button.__init__ (self, name, rect, callback, model)
		self.image = pygame.image.load ("img/med_icon.png")
		self.clickbox = False

	def clicked (self, button_name):
		self.model.game_select = MEDIUM
		for button in self.model.homebuttons:
			button.clickbox = False
		self.clickbox = True

class HardButton (Button):
	def __init__(self, name, rect, callback, model):
		Button.__init__ (self, name, rect, callback, model)
		self.image = pygame.image.load ("img/hard_icon.png")
		self.clickbox = False

	def clicked (self, button_name):
		self.model.game_select = HARD
		for button in self.model.homebuttons:
			button.clickbox = False
		self.clickbox = True

class StatsButton (Button):
	def __init__(self, name, rect, callback, model):
		Button.__init__ (self, name, rect, callback, model)
		self.image = pygame.image.load ("img/stats_icon.png")
		self.clickbox = False

	def clicked (self, button_name):
		if len (self.model.show_stats) > 0: # we are already showing stats
			self.model.show_stats = []
		else:
			num_games = str (len (self.model.times))
			best_time = "No Time Data Yet"
			avg_time = "No Time Data Yet"
			if len(self.model.times) > 0:
				best_time = format_secs (min (self.model.times))
				avg_time = format_secs (sum (self.model.times) / len (self.model.times))
			
			message_box = Plane ('message_box',
					pygame.Rect (left_margin, top_margin, 3*CARD_WIDTH + 2*space_horiz, 2*CARD_HEIGHT + 3*((WINDOW_HEIGHT - 4*CARD_HEIGHT - 2*top_margin) / 3)))
			message_box.image.fill ((0,0,0))

			win_stats = "Game Stats \n" + "Number of Games: " + num_games + "\nBest time: " + best_time + "\nAverage time: " + avg_time

			print win_stats

			message_texts = []
			lines = win_stats.split ("\n")
			box_width = 3*CARD_WIDTH + 2*space_horiz
			for line in lines:
				message_texts.append (ScreenText (line, line, 
									pygame.Rect(left_margin, top_margin + 60*(lines.index(line)+1) ,box_width, 45), pygame.font.SysFont ("Arial", 40)))
			# message_text = ScreenText ("message_text", win_stats,
			# 						pygame.Rect (left_margin, top_margin, 3*CARD_WIDTH + 2*space_horiz, 4*CARD_HEIGHT + 3*((WINDOW_HEIGHT - 4*CARD_HEIGHT - 2*top_margin) / 3)),
			# 						pygame.font.SysFont ("Arial", 40))
			

			#message_text.background_color = (255,0,0) #fixthis not transparent
			self.model.show_stats.append (message_box)
			self.model.show_stats += message_texts
        
class Game ():
	def __init__(self, game_select, model):
		########################
		# GAME SCREEN ELEMENTS #
		########################
		self.deck = []

		self.model = model
		self.game_select = game_select

		self.pause_time = 0
		self.paused_time_at = 0

		self.start_time = pygame.time.get_ticks ()
		self.end_time = 0

		#make 81 unique cards
		for color in colors:
			for shape in shapes:
				for number in numbers:
					for shade in shades:
						card_to_add = Card (color + shape + shade + str (number),
											color, shape, number, shade)
						self.deck.append (card_to_add)
						card_to_add.image = pygame.image.load ("img/" + card_to_add.name + ".png")
						
		self.actors = []

		self.in_play_cards = []
		self.clicked_cards = []
		self.out_of_play_cards = []

		self.sets_found = 0
		self.sets_wrong = 0
		self.hints_left = 100

		self.added_time = False

		font1 = pygame.font.SysFont ("Arial", 40)
		font2 = pygame.font.SysFont ("Arial", 20)
		self.sets_found_label = ScreenText ("sets_found_label", 
											"Sets: " + str (self.sets_found), 
											pygame.Rect (3*WINDOW_WIDTH/4, 290, WINDOW_WIDTH/4, 50), 
											font1)
		self.time_label = ScreenText ("time_label", 
									  "Time: " + format_secs (self.start_time / 1000),
									  pygame.Rect (3*WINDOW_WIDTH/4, 220, WINDOW_WIDTH/4, 100),
									  font1)
		self.left_in_deck_label = ScreenText ("left_in_deck_label", 
									  "Deck: " + str (len (self.deck) - (len (self.in_play_cards) + len (self.out_of_play_cards))),
									  pygame.Rect (3*WINDOW_WIDTH/4, 505, WINDOW_WIDTH/4, 25), 
									  font2)

		self.add3_button = AddThreeCardsButton ("add_three_cards_button",
												pygame.Rect (3*WINDOW_WIDTH/4 + (WINDOW_WIDTH/4 - 200)/2, 360, 100, 100),
												AddThreeCardsButton.clicked,
												self)
		self.hint_button = HintButton ("hint_button",
										pygame.Rect (3*WINDOW_WIDTH/4 + (WINDOW_WIDTH/4 - 200)/2 + 100, 360, 100, 100),
										HintButton.clicked,
										self)
		self.pause_button = PauseButton ("pause_button",
										pygame.Rect (3*WINDOW_WIDTH/4 + (WINDOW_WIDTH/4 - 200)/2 + 50, WINDOW_HEIGHT - 120, 100, 100),
										PauseButton.clicked,
										self)
		self.hints_left_label = ScreenText ("hints_left_label", 
											"Hints Remaining: " + str (self.hints_left), 
											pygame.Rect (3*WINDOW_WIDTH/4, 475, WINDOW_WIDTH/4, 25), 
											font2)
		self.logo = planes.Plane ("setlogo",
								  pygame.Rect (3*WINDOW_WIDTH/4, 50, 240, 162),
								  False, False)
		self.logo.image = pygame.image.load ("img/set.jpg")
		self.time_box = TimeBox ("time_box", pygame.Rect (0, -WINDOW_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT), game_select)


		#### PAUSE SCREEN BUTTONS ####
		message_width = 3*CARD_WIDTH + 2*space_horiz

		self.play_button = PlayButton ("play_button",
										pygame.Rect (2*message_width/5 - 50, WINDOW_HEIGHT - 300, 100, 100),
										PlayButton.clicked,
										self)
		self.restart_button = RestartButton ("restart_button",
										pygame.Rect (3*message_width/5 - 50, WINDOW_HEIGHT - 300, 100, 100),
										RestartButton.clicked,
										self)
		self.back_button = BackButton ("back_button",
										pygame.Rect (4*message_width/5 - 50, WINDOW_HEIGHT - 300, 100, 100),
										BackButton.clicked,
										self)
		#### CATEGORIES ####
		self.gamebuttons = [self.add3_button, self.hint_button, self.pause_button, self.logo]
		self.gamelabels = [self.sets_found_label, self.time_label, self.hints_left_label, self.left_in_deck_label]
		self.pausebuttons = [self.play_button, self.restart_button, self.back_button]

		# start the game
		self.add_new_cards (12)

	def add_new_cards (self, number, index=0):
		if not len (self.in_play_cards) + len (self.out_of_play_cards) == len (self.deck):
			i = 0
			while i < number:
				num = random.randint (0,len (self.deck)-1)
				card = self.deck[num]
				if card not in self.in_play_cards and card not in self.out_of_play_cards:
					self.in_play_cards.insert (index, card)
					i += 1

	def check_if_any_sets (self):
		for card1 in self.in_play_cards:
			for card2 in self.in_play_cards:
				for card3 in self.in_play_cards:
					if card1 != card2 and card2 != card3 and card1 != card3:
						if check_set (card1, card2, card3):
							return True
		return False

	def check_if_won (self):
		return (not self.check_if_any_sets ()) and \
			   (len (self.in_play_cards) + len (self.out_of_play_cards) == len (self.deck))

	def check_if_lost (self):
		return self.time_box.rect.y >= 0 

	def update (self):
		if self.check_if_won () or self.check_if_lost ():
			if self.check_if_won () and not self.added_time:
				self.model.times.append ((pygame.time.get_ticks () - self.start_time)/ 1000)
				self.added_time = True
			if self.end_time == 0:
				self.end_time = pygame.time.get_ticks ()

			#self.time_box.speed = self.game_select
			#self.time_box.update ()
			self.actors = [self.time_box]
			#self.actors = []

			for card in self.in_play_cards:
				self.actors.append (card)
				
			self.actors += self.gamelabels + self.gamebuttons
			self.hints_left_label.update_text ("Hints Remaining: " + str (self.hints_left))
			self.left_in_deck_label.update_text ("Deck: " + str (len (self.deck) - (len (self.in_play_cards) + len (self.out_of_play_cards))))

			message_box = Plane ('message_box',
				pygame.Rect (left_margin, top_margin, 3*CARD_WIDTH + 2*space_horiz, 4*CARD_HEIGHT + 3*((WINDOW_HEIGHT - 4*CARD_HEIGHT - 2*top_margin) / 3)))

			message_box.image.fill ((0,0,0))

			best_time = ""
			if len(self.model.times) == 0:
				best_time = format_secs ((self.end_time - self.start_time - self.pause_time)/ 1000)
			else:
				best_time = format_secs (min (self.model.times))

			win_stats = "Game Complete! \n" + "Total time: " + format_secs ((self.end_time - self.start_time - self.pause_time)/ 1000) + "\n" + \
						"Best time: " + best_time

			lose_stats = "Game Over!"

			stats = win_stats
			if self.check_if_lost ():
				stats = lose_stats

			message_texts = []
			lines = stats.split ("\n")
			box_width = 3*CARD_WIDTH + 2*space_horiz
			for line in lines:
				message_texts.append (ScreenText (line, line, 
									pygame.Rect(left_margin, top_margin + 50*(lines.index(line)+1) ,box_width, 45), pygame.font.SysFont ("Arial", 40)))
			# message_text = ScreenText ("message_text", win_stats,
			# 						pygame.Rect (left_margin, top_margin, 3*CARD_WIDTH + 2*space_horiz, 4*CARD_HEIGHT + 3*((WINDOW_HEIGHT - 4*CARD_HEIGHT - 2*top_margin) / 3)),
			# 						pygame.font.SysFont ("Arial", 40))
			

			#message_text.background_color = (255,0,0) #fixthis not transparent
			self.actors.append (message_box)
			self.actors += message_texts
			if self.check_if_lost ():
				pass
				#message_texts.update_text (lose_stats)
			self.actors += self.pausebuttons
		
		elif self.paused_time_at != 0: #game is paused
			#print self.time_box.rect.y
			#self.time_box.speed = self.game_select
			self.actors = []

			for card in self.in_play_cards:
				self.actors.append (card)
				
			self.actors += self.gamelabels + self.gamebuttons
			self.hints_left_label.update_text ("Hints Remaining: " + str (self.hints_left))
			self.left_in_deck_label.update_text ("Deck: " + str (len (self.deck) - (len (self.in_play_cards) + len (self.out_of_play_cards))))

			message_box = Plane ('message_box',
				pygame.Rect (left_margin, top_margin, 3*CARD_WIDTH + 2*space_horiz, 4*CARD_HEIGHT + 3*((WINDOW_HEIGHT - 4*CARD_HEIGHT - 2*top_margin) / 3)))

			message_box.image.fill ((0,0,0))

			message_text = ScreenText ("message_text", "Game Paused",
									pygame.Rect (left_margin, top_margin, 3*CARD_WIDTH + 2*space_horiz, 4*CARD_HEIGHT + 3*((WINDOW_HEIGHT - 4*CARD_HEIGHT - 2*top_margin) / 3)),
									pygame.font.SysFont ("Arial", 40))
			message_text.background_color = (255,0,0) #fixthis not transparent
			self.actors.append (message_box)
			self.actors.append (message_text)
			for button in self.pausebuttons:
				self.actors.append (button)

		else:
			print "iam updating"
			print self.time_box.rect.y
			self.time_box.speed = self.game_select
			self.time_box.update ()
			self.actors = [self.time_box]
			#self.actors = []

			#check which cards are clicked
			self.clicked_cards = []

			for card in self.in_play_cards:
				self.actors.append (card)
				if card.been_clicked:
					self.clicked_cards.append (card)
				card.update ()

			#add click boxes
			for card in self.clicked_cards:
				clicked_box = planes.Plane ("box" + card.name,
											pygame.Rect (card.rect.x-5,
														 card.rect.y-5,
														 card.rect.width + 10,
														 card.rect.height + 10),
											False, False)
				clicked_box.image = pygame.image.load ("img/clickbox.png")
				self.actors.insert (1, clicked_box)

			#check for sets
			if len (self.clicked_cards) == 3:
				is_set = check_set (self.clicked_cards[0], 
									self.clicked_cards[1],
									self.clicked_cards[2])
				if is_set:
					self.sets_found += 1
					self.sets_found_label.update_text ("Sets: " + str (self.sets_found))

					#remove cards and add new ones
					for card in self.clicked_cards:
						self.out_of_play_cards.append (card)
						index = self.in_play_cards.index (card)
						self.in_play_cards.remove (card)
						if len (self.in_play_cards) < 12:
							self.add_new_cards (1, index)

				else:
					if self.sets_found > 0:
						self.sets_wrong += 1
					self.sets_found_label.update_text ("Sets: " + str (self.sets_found))
				for card in self.clicked_cards:
					card.been_clicked = False

			self.actors += self.gamelabels + self.gamebuttons
			self.time_label.update_text ("Time: " + format_secs ((pygame.time.get_ticks () - self.start_time - self.pause_time)/ 1000))
			self.hints_left_label.update_text ("Hints Remaining: " + str (self.hints_left))
			self.left_in_deck_label.update_text ("Deck: " + str (len (self.deck) - (len (self.in_play_cards) + len (self.out_of_play_cards))))

class Model:
	def __init__ (self):
		self.background = (20,20,20)
		self.mode = HOME
		self.game_select = NOTIME

		self.game = None
		self.actors = []
		self.times = []
		self.show_stats = [] # a list of things for stats screen

		########################
		# HOME SCREEN ELEMENTS #
		########################

		#self.ok = planes.gui.OkBox('press okay')


		self.start_button = StartButton ("start_button",
										pygame.Rect (3*WINDOW_WIDTH/4 + (WINDOW_WIDTH/4 - 200)/2 + 100, 50, 100, 100),
										StartButton.clicked,
										self)

		self.notime_button = NoTimeButton ("notime_button",
										pygame.Rect (WINDOW_WIDTH/5 - 50, WINDOW_HEIGHT - 200, 100, 100),
										NoTimeButton.clicked,
										self)
		self.easy_button = EasyButton ("easy_button",
										pygame.Rect (2*WINDOW_WIDTH/5 - 50, WINDOW_HEIGHT - 200, 100, 100),
										EasyButton.clicked,
										self)
		self.med_button = MedButton ("med_button",
										pygame.Rect (3*WINDOW_WIDTH/5 - 50, WINDOW_HEIGHT - 200, 100, 100),
										MedButton.clicked,
										self)
		self.hard_button = HardButton ("hard_button",
										pygame.Rect (4*WINDOW_WIDTH/5 - 50, WINDOW_HEIGHT - 200, 100, 100),
										HardButton.clicked,
										self)
		self.stats_button = StatsButton ("stats_button",
										pygame.Rect (3*WINDOW_WIDTH/4 + (WINDOW_WIDTH/4 - 200)/2 + 100, 200, 100, 100),
										StatsButton.clicked,
										self)

		self.homebuttons = [self.start_button, self.notime_button, self.easy_button, self.med_button, self.hard_button, self.stats_button]
		

	def update (self):
		if self.mode == HOME:
			print self.times
			self.actors = self.homebuttons[:]# + self.scroll
			if self.show_stats != None:
				self.actors += self.show_stats
			#self.actors.append (self.ok)
			clicked_button = None
			#add click boxes
			for button in self.homebuttons:
				if button.clickbox:
					clicked_button = button

			print "hella", clicked_button.name
			clicked_box = planes.Plane ("box" + clicked_button.name,
										pygame.Rect (clicked_button.rect.x-5,
													 clicked_button.rect.y-5,
													 clicked_button.rect.width + 10,
													 clicked_button.rect.height + 10),
										False, False)

			#clicked_box.image = pygame.image.load ("img/clickbox.png")
			self.actors.insert (1, clicked_box)
		
		else:
			self.game.update ()
			self.actors = self.game.actors[:]


class View:
	def __init__ (self, model, screen):
		self.model = model
		self.screen = screen

	def draw (self):
		space_vert = 50
		screen.remove_all ()
		if isinstance (self.model.background, str):
			self.screen.image = pygame.transform.scale (pygame.image.load (self.model.background),
													   (WINDOWWIDTH,WINDOWHEIGHT))
		else:
			self.screen.image.fill (self.model.background)

		#put cards in play into a grid:

		if model.game != None:

			if len (self.model.game.in_play_cards) == 12:
				space_vert = (WINDOW_HEIGHT - 4*CARD_HEIGHT - 2*top_margin) / 3
			elif len (self.model.game.in_play_cards) == 15:
				space_vert = (WINDOW_HEIGHT - 5*CARD_HEIGHT - 2*top_margin) / 4
			elif len (self.model.game.in_play_cards) == 18:
				space_vert = (WINDOW_HEIGHT - 6*CARD_HEIGHT - 2*top_margin) / 5
			elif len (self.model.game.in_play_cards) == 21:
				space_vert = (WINDOW_HEIGHT - 7*CARD_HEIGHT - 2*top_margin) / 6

			positions =[(left_margin, top_margin), 
						(left_margin + CARD_WIDTH + space_horiz, top_margin), 
						(left_margin + 2*CARD_WIDTH + 2*space_horiz, top_margin),

						(left_margin, top_margin + CARD_HEIGHT + space_vert),
						(left_margin + CARD_WIDTH + space_horiz, top_margin + CARD_HEIGHT + space_vert),
						(left_margin + 2*CARD_WIDTH + 2*space_horiz, top_margin + CARD_HEIGHT + space_vert),

						(left_margin, top_margin + 2*CARD_HEIGHT + 2*space_vert),
						(left_margin + CARD_WIDTH + space_horiz, top_margin + 2*CARD_HEIGHT + 2*space_vert),
						(left_margin + 2*CARD_WIDTH + 2*space_horiz, top_margin + 2*CARD_HEIGHT + 2*space_vert),

						(left_margin, top_margin + 3*CARD_HEIGHT + 3*space_vert),
						(left_margin + CARD_WIDTH + space_horiz, top_margin + 3*CARD_HEIGHT + 3*space_vert),
						(left_margin + 2*CARD_WIDTH + 2*space_horiz, top_margin + 3*CARD_HEIGHT + 3*space_vert),

						(left_margin, top_margin + 4*CARD_HEIGHT + 4*space_vert),
						(left_margin + CARD_WIDTH + space_horiz, top_margin + 4*CARD_HEIGHT + 4*space_vert),
						(left_margin + 2*CARD_WIDTH + 2*space_horiz, top_margin + 4*CARD_HEIGHT + 4*space_vert),

						(left_margin, top_margin + 5*CARD_HEIGHT + 5*space_vert),
						(left_margin + CARD_WIDTH + space_horiz, top_margin + 5*CARD_HEIGHT + 5*space_vert),
						(left_margin + 2*CARD_WIDTH + 2*space_horiz, top_margin + 5*CARD_HEIGHT + 5*space_vert),

						(left_margin, top_margin + 6*CARD_HEIGHT + 6*space_vert),
						(left_margin + CARD_WIDTH + space_horiz, top_margin + 6*CARD_HEIGHT + 6*space_vert),
						(left_margin + 2*CARD_WIDTH + 2*space_horiz, top_margin + 6*CARD_HEIGHT + 6*space_vert) ]
							
			for i in range (len (self.model.game.in_play_cards)):
				self.model.game.in_play_cards[i].rect.x = positions[i][0]
				self.model.game.in_play_cards[i].rect.y = positions[i][1]

		for actor in self.model.actors:
			self.screen.sub (actor)

if __name__ == "__main__":
	pygame.init ()
	size = (WINDOW_WIDTH, WINDOW_HEIGHT)
	screen = planes.Display (size)
	screen.grab = False
	screen.image.fill (BLACK)
	model = Model ()
	view = View (model, screen)
	running = True

	for actor in model.actors:
		screen.sub (actor)

	while running:
		events = pygame.event.get ()
		for event in events:
			if event.type == pygame.QUIT:
				raise SystemExit

		screen.process (events)
		model.update ()
		screen.update ()
		screen.render ()
		
		view.draw ()
		pygame.display.flip ()
		time.sleep (.001)

	pygame.quit ()

# win condition
# avg time per set
# hints
# start new game on back button_name
# currently is pause button - make one?
# save score in txt file