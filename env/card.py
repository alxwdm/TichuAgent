""" This module contains a class to represent a Tichu Card. """

import hashlib

SUITS = {'Spade':'♠',
         'Heart':'♡',
         'Dia':'♢',
         'Club':'♣'}

CARD_VALUES = {'2': 2,
               '3': 3,
               '4': 4,
               '5': 5,
               '6': 6,
               '7': 7,
               '8': 8,
               '9': 9,
               '10': 10,
               'J': 11,
               'Q': 12,
               'K': 13,
               'A': 14,
               'Dragon': 15.1,
               'Phoenix': 0.5,
               'Majong': 1,
               'Dog': 0.9}

class Card():
    """
    A class to represent a Tichu Card.

    Inspired by the following sources:
    - https://github.com/hundredblocks/ticher
    - https://github.com/sylee421/TichuRL

    Attributes
    ----------
    name: str
      The name of the Card, i.e. '5', 'A', 'K' for regular cards
      and 'Dragon' etc. for special cards.
    suit: str
      One of the following: Spade, Heart, Dia(mond), Club or Special
    power: float
      The power (i.e. value) of the card.
    points: int
      The points of the card.
      In Tichu, only 5, 10, K, Phoenix and Dragon give points.
    image: str
      A nice visualization when printing the card.
      Depending on the device, this may need to be adapted.

    """

    def __init__(self, name=None, suit=None):
        """
        Constructs a Tichu card.

        Parameter
        ----------
        name: str
          The name of the Card, i.e. '5', 'A', 'K' for regular cards
          and 'Dragon' etc. for special cards.
        suit: str
          One of the following: Spade, Heart, Dia(mond), Club or Special.
        """
        self.name = name
        self.suit = suit
        self.special_card = (suit == 'Special')
        self.power = CARD_VALUES[self.name]
        self.points = 0

        # Tichu rules: only cards 5, 10 and K give points
        if self.name == '5':
            self.points = 5
        elif self.name == '10' or self.name == 'K':
            self.points = 10
        elif self.name == 'Dragon':
            self.points = 25
        elif self.name == 'Phoenix':
            self.points = -25

        # card image is used for visualization
        if name == '10':
            self.image = ['┍┄┄┄┑', '┆'+self.name+'   ┆',
                         '┆  '+SUITS[self.suit]+'  ┆', '┆   '+self.name+'┆',
                         '┖┄┄┄┚']
        elif name == 'Dragon':
            self.image = ['┍┄┄┄┑', '┆ '+'Dr'+'  ┆',
                          '┆ '+'ag'+'  ┆', '┆ '+'on'+'  ┆', '┖┄┄┄┚']
        elif name == 'Phoenix':
            self.image = ['┍┄┄┄┑', '┆ '+'Ph'+'  ┆',
                          '┆ '+'oe'+'  ┆', '┆ '+'nix'+' ┆', '┖┄┄┄┚']
        elif name == 'Dog':
            self.image = ['┍┄┄┄┑', '┆'+' '+'    ┆', '┆ '+'Dog'+' ┆',
                          '┆ '+' '+'   ┆', '┖┄┄┄┚']
        elif name == 'Majong':
            self.image = ['┍┄┄┄┑', '┆'+' '+'    ┆', '┆  '+'1'+'  ┆',
                          '┆  '+' '+'  ┆', '┖┄┄┄┚']
        else:
            self.image = ['┍┄┄┄┑', '┆ '+self.name+'   ┆',
                          '┆  '+SUITS[self.suit]+'  ┆', '┆   '+self.name+' ┆',
                          '┖┄┄┄┚']

    def __ge__(self, other):
        return self.power >= other.power

    def __le__(self, other):
        return self.power <= other.power

    def __gt__(self, other):
        return self.power > other.power

    def __lt__(self, other):
        return self.power < other.power

    def __eq__(self, other):
        if self.suit != 'Special':
            return self.power == other.power
        else:
            return self.name == other.name

    def __ne__(self, other):
        return self.power != other.power

    def __hash__(self):
        card_hash = hashlib.md5()
        card_hash.update(self.__repr__().encode())
        card_hash = card_hash.hexdigest()
        card_hash = int(card_hash, 16)
        return card_hash

    def __repr__(self):
        return str({'name': self.name,
                    'suit': self.suit,
                    'power': self.power,
                    'points': self.points})
  