""" This module contains a class to represent a Tichu Player. """

import random

class Player():
    """
    A class to represent a Player in a Tichu game.

    Attributes
    ----------
    hand: Cards
      A Cards instance containing the hand cards of this Player.
    points: int
      The points this Player has achieved so far.
    tichu_flag: bool
      Whether The Player has called Tichu.
    hand_size: int
      The number of hand Cards of this Player.
    hand_power: int
      The power of the hand (only > 0 if it is a single combination).
    finished: bool
      Whether this Player has finished (i.e. no more hand Cards).
    hand_rating: float
      A rating of how good the hand is.

    Methods
    -------
    assign_hand(cards):
      Adds a Cards instance to the Players' hand.
    remove_cards(cards):
      Removes Cards from Players hand.
      Returns true if successfull.
    add_points(points):
      Adds points to the points the Players' achived so far.
    set_points(points):
      Sets Players points and overrides the points achieved so far.
    move(cards):
      Checks whether hand contains cards (i.e. if move is possible).
    random_move():
      Makes a random choice from all available combinations of hand.
    call_tichu():
      Sets tichu_flag if Player did not play any hand cards yet.
    has_finished():
      returns True if Player has played all hand cards.
    """

    def __init__(self):
        """
        Constructs a Player waiting to recieve a hand via assign_hand().
        """
        self.points = 0
        self.tichu_flag = False
        self.hand_size = 0
        self.hand_power = 0
        self.finished = False
        self.hand = None
        self.hand_rating = 0

    def assign_hand(self, cards):
        """ Assigns a Cards instance to the Players' hand. """
        self.hand = cards
        self._update()
        self._set_hand_rating()
        return True

    def remove_cards(self, cards):
        """ Removes all Card instances in Cards from Players' hand. """
        if self.hand.contains(cards):
            for crd in cards.cards:
                self.hand.remove(crd)
            self._update()
            return True
        else:
            return False

    def add_points(self, points):
        """ Add points to Players' points. """
        self.points += points

    def set_points(self, points):
        """ Sets (overrides) Players' points. """
        self.points = points

    def move(self, cards):
        """ Returns true if Cards is a valid move. """
        if self.hand.contains(cards):
            return True
        else:
            return False

    def random_move(self):
        """ Randomly play one available combination. """
        available_comb = self.hand.get_available_combinations()
        flattened = [item for sublist in available_comb for item in sublist]
        random_comb = random.choice(flattened)
        suc = self.move(random_comb)
        if suc: # double-check, move should always return True
            return random_comb
        else:
            return False

    def call_tichu(self):
        """ Calls Tichu if Player did not play any Cards yet. """
        if self.hand_size == 14:
            self.tichu_flag = True
            return True
        else:
            return False

    def has_finished(self):
        """ Checks whether the Player played all its Cards. """
        return self.finished

    def _update(self):
        """ Update Players' Attributes after a Card has been played. """
        self.hand_size = self.hand.size
        self.hand_power = self.hand.power
        if self.hand_size == 0:
            self.finished = True

    def _set_hand_rating(self):
        """
        Set hand rating of Players' hand based on a heuristic.

        The hand rating is based on the individual cards
        and available combinations of the Players' hand.
        A high rating can be achieved if the Player has
        a lot of high cards (Kings, Aces and Dragon or Phoenix)
        and a lot of good combinations (bomb, straight, triple, full).
        """
        good_cards = ['A', 'K', 'Dragon', 'Phoenix']
        bad_cards = {'Dog'}
        comb_types = {'solo': 0,
                      'pair': 1,
                      'triple': 2,
                      'four_bomb': 3,
                      'full': 4,
                      'straight': 5,
                      'straight_bomb': 6,
                      'pair_seq': 7}
        # initialize cards and score
        cards = self.hand
        score = 0
        # update score based on individual cards
        good_cards_list = [elem for elem in cards.cards
                            if elem.name in good_cards]
        for crd in good_cards_list:
            if crd.name == 'Dragon' or crd.name == 'A':
                score += 20
            else:
                score += 10
        bad_cards_list = [elem for elem in cards.cards
                            if elem.name in bad_cards]
        if bad_cards_list:
            score -= 40
        # update score based on combinations
        avail_combs = cards.get_available_combinations()
        if avail_combs[comb_types['four_bomb']]:
            for crds in avail_combs[comb_types['four_bomb']]:
                score += 40
                cards.remove(crds)
                avail_combs = cards.get_available_combinations()
        if avail_combs[comb_types['straight_bomb']]:
            for crds in avail_combs[comb_types['straight_bomb']]:
                score += 40
                cards.remove(crds)
                avail_combs = cards.get_available_combinations()
        if avail_combs[comb_types['full']]:
            max_fulls =  sum([full.power for full
                              in avail_combs[comb_types['full']]]
                             )/len(avail_combs[comb_types['full']])
            score += max_fulls
        if avail_combs[comb_types['triple']]:
            max_triple = sum([triple.power
                            for triple in avail_combs[comb_types['triple']]]
                            )/len(avail_combs[comb_types['triple']])
            score += max_triple
        if avail_combs[comb_types['straight']]:
            max_len = max([strt.size
                           for strt in avail_combs[comb_types['straight']]])
            score += max_len
        self.hand_rating = score
