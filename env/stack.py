""" This module contains a class to represent a Tichu Stack. """

BOMBS = ['four_bomb', 'straight_bomb']

class Stack():
    """
    A class to represent a Stack in a Tichu game.

    Attributes
    ----------
    cards: list of Cards
      A list of Cards that have been put on the stack.
      The highest combination is the last entry of the list.
    points: int
      The aggregated points of all Cards in this Stack.
    power: float
      The power of the highest combination in this Stack.
    type: str
      The type of combination in this Stack (e.g. pair, straight).
    dragon_flag: bool
      Whether the Stack contains the Dragon Card or not.

    Methods
    -------
    add(cards):
      Adds Cards to the stack if the move is valid.
    check_valid_move(old_cards, new_cards):
      Checks whether new_cards can be played on top of old_cards.
    """

    def __init__(self):
        """
        Constructs a Stack wit an empty list of cards.
        """
        self.cards = list()
        self.points = 0
        self.power = 0
        self.type = None
        self.dragon_flag = False

    def _set_power(self):
        """ Sets Stack power after Cards have been played on top. """
        self.power = self.cards[-1].power

    def _set_points(self):
        """ Sets Stack points after Cards have been played on top. """
        self.points = sum(crds.points for crds in self.cards)

    def _set_type(self):
        """ Sets Stack type after Cards have been played on top. """
        self.type = self.cards[-1].type

    def _set_dragon_flag(self):
        """ Sets dragon_flag after Cards have been played on top. """
        name_list = [crd.name for crds in self.cards for crd in crds.cards]
        if 'Dragon' in name_list:
            self.dragon_flag = True

    def _update(self):
        """ Updates all attributes after Cards have been played on top. """
        self._set_power()
        self._set_points()
        self._set_type()
        self._set_dragon_flag()

    def add(self, cards_to_add):
        """ Adds cards to stack according to game rules. """
        suc = bool()
        # all but hand and pass can be played on empty stack
        if (not(self.cards) and
              cards_to_add.type != 'hand' and
              cards_to_add.type != 'pass'):
            self.cards.append(cards_to_add)
            self._update()
            suc = True
        # if stack not empty, cards_to_add must be same type and higher power
        elif (self.type == cards_to_add.type and
              self.power < cards_to_add.power):
            # for straight and pair_seq, equal lengths are required
            if (self.type == 'straight' and
                  not self.cards[-1].size == cards_to_add.size):
                suc = False
            elif (self.type == 'pair_seq' and
                  not self.cards[-1].size == cards_to_add.size):
                suc = False
            # Dog can only be played as first card
            elif cards_to_add.cards[0].name == 'Dog':
                suc = False
            # append and update stack if successful move
            else:
                self.cards.append(cards_to_add)
                self._update()
                suc = True
        # special moves: Phoenix can be played on solo (except Dragon)
        elif (self.type == 'solo' and
              cards_to_add.type == 'solo' and
              cards_to_add.phoenix_flag and
              self.power < 15):
            old_power = self.power
            self.cards.append(cards_to_add)
            self._update()
            self.power = old_power + 0.5
            suc = True
        # bombs can be played any time
        elif cards_to_add.type in BOMBS and self.power < cards_to_add.power:
            self.cards.append(cards_to_add)
            self._update()
            suc = True
        # illegal move
        else:
            suc = False
        return suc

    def assert_valid_move(self, cards_to_add):
        """ Checks whether cards_to_add can be added to current stack. """
        suc = bool()
        # all but hand and pass can be played on empty stack
        if (not(self.cards) and
              cards_to_add.type != 'hand' and
              cards_to_add.type != 'pass'):
            suc = True
        # if stack not empty, cards_to_add must be same type and higher power
        elif (self.type == cards_to_add.type and
              self.power < cards_to_add.power):
            # for straight and pair_seq, equal lengths are required
            if (self.type == 'straight' and
                  not self.cards[-1].size == cards_to_add.size):
                suc = False
            elif (self.type == 'pair_seq' and
                  not self.cards[-1].size == cards_to_add.size):
                suc = False
            # Dog can only be played as first card
            elif cards_to_add.cards[0].name == 'Dog':
                suc = False
            # append and update stack if successful move
            else:
                suc = True
        # special moves: Phoenix can be played on solo (except Dragon)
        elif (self.type == 'solo' and
              cards_to_add.type == 'solo' and
              cards_to_add.phoenix_flag and
              self.power < 15):
            suc = True
        # bombs can be played any time
        elif cards_to_add.type in BOMBS and self.power < cards_to_add.power:
            suc = True
        # illegal move
        else:
            suc = False
        return suc

    @staticmethod
    def check_valid_move(old_cards, new_cards):
        """ Checks if new_cards is a valid move on old_cards. """
        if not(old_cards) and new_cards.type != 'hand':
            return True
        elif (old_cards.type == new_cards.type and
              old_cards.power < new_cards.power):
            if (old_cards.type == 'straight' and
                  not len(old_cards.cards) == len(new_cards.cards)):
                return False
            else:
                return True
        elif (old_cards.type == 'solo' and new_cards.type == 'solo' and
              new_cards.phoenix_flag and old_cards.power < 15):
            return True
        elif new_cards.type in BOMBS and old_cards.power < new_cards.power:
            return True
        else:
            return False
