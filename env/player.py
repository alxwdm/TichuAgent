# Player class for Python Implementation of Tichu

import random

class Player():

    def __init__(self):

        self.points = 0
        self.tichu_flag = False
        self.hand_size = 0
        self.hand_power = 0
        self.finished = False
        self.hand = None
        self.hand_rating = 0

    def assign_hand(self, cards):
        self.hand = cards
        self._update()
        self._set_hand_rating()
        return True

    def remove_cards(self, cards):
        if self.hand.contains(cards):
            for crd in cards.cards:
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
        flattened = [item for sublist in available_comb for item in sublist]
        random_comb = random.choice(flattened)
        suc = self.move(random_comb)
        if suc: # double-check, move should always return True
            return random_comb
        else:
            return False

    def call_tichu(self):
        if self.hand_size == 14:
            self.tichu_flag = True
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

    def _set_hand_rating(self):
        """
        This function sets the player's hand rating based on
        the individual cards and available combinations.
        A high rating can be achieved if the player has
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
