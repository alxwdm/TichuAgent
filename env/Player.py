# Player class for Python Implementation of Tichu

import random
from env.Cards import Cards


class Player():

	def __init__(self, id):

		self.id = id
		self.points = 0
		self.called_tichu = False
		self.hand_size = 0
		self.hand_power = 0
		self.finished = False

	def assign_hand(self, cards):
		self.hand = cards
		self._update()
		return True

	def remove_cards(self, cards):
		if self.hand.contains(cards):
			for crd in cards:
				self.hand.remove(crd)
			self._update()
			return True
		else:
			return False

	def add_points(self, points):
		self.points += points

	def set_points(self, points):
		self.points = points

	def move(self, cards):
		if self.hand.contains(cards):
			return True
		else:
			return False

	def random_move(self):
		# randomly play one available combination
		available_comb = self.hand.get_available_combinations()
		random_comb = random.choice(available_comb)
		suc = self.move(random_comb)
		if suc:
			return random_comb

	def call_tichu(self):
		if self.hand_size == 14:
			self.called_tichu = True
			return True
		else:
			return False

	def has_finished(self):
		return self.finished

	def _update(self):
		self.hand_size = self.hand.size
		self.hand_power = self.hand.power
		if self.hand_size == 0:
			self.finished = True
