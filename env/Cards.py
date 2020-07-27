# Cards class for Python Implementation of Tichu
# Sources:
#  - https://github.com/hundredblocks/ticher
#  - https://github.com/sylee421/TichuRL

import random
from collections import defaultdict

from env.Card import Card

class Cards():

    size = None
    cards = None
    phoenix_flag = None

    def __init__(self, card_list):

        self.phoenix_flag = False

        self.cards = list()
        for i in card_list:
            self.cards.append(i)
            if i.name == 'Phoenix':
                self.phoenix_flag = True
        self.cards.sort()

        self.size = len(self.cards)

        self.set_type_and_power()

    # a nice visualization of all cards in the set
    def show(self):
        if self.size == 0:
            print('  PASS')
        else:
            for i in range(5):
                for crd in range(self.size):
                    print(self.cards[crd].image[i], end='')
                print()	

    # set number of game points of this card set
    def set_points(self):
        self.points = sum([crd.points for crd in self.cards])

    # determine which combination (if any) is this card set
    def set_type_and_power(self):
        card_set = self.cards
        card_set.sort()
        self.type = 'unk'

        # pass
        if len(card_set)==0:
            self.type = 'pass'
            self.power = 0
            return
        # solo
        if len(card_set)==1:
            self.type = 'solo'
            self.power = card_set[0].power
            return
        # pair
        if len(card_set)==2:
            if card_set[0].power == card_set[1].power:
                self.type = 'pair'
                self.power = card_set[0].power
                return
            # phoenix pair
            elif self.phoenix_flag:
                self.type = 'pair'
                self.power = card_set[1].power
                return
        # triple
        if len(card_set)==3:
            if card_set[0].power == card_set[1].power and card_set[1].power == card_set[2].power:
                self.type = 'triple'
                self.power = card_set[0].power
                return
            # phoenix triple
            elif self.phoenix_flag and card_set[1].power == card_set[2].power:
                self.type = 'triple'
                self.power = card_set[1].power
                return
        # four (BOMB)
        if len(card_set)==4 and card_set[0].power == card_set[1].power and card_set[1].power == card_set[2].power and card_set[2].power == card_set[3].power:
            self.type = 'four_bomb'
            self.power = card_set[0].power
            return
        # full house 
        if len(card_set)==5:
            if card_set[0].power == card_set[1].power and card_set[1].power == card_set[2].power and card_set[3].power == card_set[4].power:
                self.type = 'full'
                self.power = card_set[0].power
                return
            elif card_set[0].power == card_set[1].power and card_set[2].power == card_set[3].power and card_set[3].power == card_set[4].power:
                self.type = 'full'
                self.power = card_set[2].power
                return
            # phoenix full house with phoenix triple
            elif self.phoenix_flag and card_set[1].power == card_set[2].power and card_set[3].power == card_set[4].power:
                self.type = 'full'
                self.power = card_set[3].power
                return
            # phoenix full house with phoenix pair
            elif self.phoenix_flag:
                if card_set[1].power == card_set[2].power and card_set[2].power == card_set[3].power:
                    self.type = 'full'
                    self.power = card_set[1].power
                    return
                elif card_set[2].power == card_set[3].power and card_set[3].power == card_set[4].power:
                    self.type = 'full'
                    self.power = card_set[2].power
                    return
        # straight and straight bomb
        if len(card_set)>=5:
            is_straight = True
            is_flush = True
            for i in range(len(card_set)-1):
                if card_set[i].power + 1 == card_set[i+1].power:
                    if card_set[i].suit == card_set[i+1].suit:
                        pass
                    else:
                        is_flush = False
                else:
                    is_straight = False
                    break
            if is_straight == True and is_flush == True:
                self.type = 'straight_bomb'
                self.power = card_set[0].power
                return
            if is_straight:
                self.type = 'straight'
                self.power = card_set[-1].power
                return
            # phoneix straight
            if self.phoenix_flag:
                phoenix_used = False
                phoenix_idx = -1
                is_straight = True
                for i in range(len(card_set)-2):
                    if card_set[i+1].power + 1 == card_set[i+2].power:
                        pass
                    elif not(phoenix_used):
                        phoenix_used = True
                        phoenix_idx = i+1
                    else:
                        is_straight = False
                if is_straight:
                    self.type = 'straight'
                    if phoenix_idx == len(card_set): # phoenix is last card of straight
                        self.power = card_set[-1].power+1
                    else:
                        self.power = card_set[-1].power
                    return
        # pair sequence
        if len(card_set) >= 4 and len(card_set) % 2 == 0:
            is_pair_seq = True
            for i in range(len(card_set)-1):
                if i % 2 == 0 and card_set[i].power == card_set[i+1].power:
                    pass
                elif i % 2 == 1 and card_set[i].power + 1 == card_set[i+1].power:
                    pass
                else:
                    is_pair_seq = False
                    break
            # phoenix pair sequence
            # TODO: Does not work yet
            if self.phoenix_flag:
                phoenix_used = False
                for i in range(len(card_set)-2):
                    if i % 2 == 0 and card_set[i+1].power == card_set[i+2].power:
                        pass
                    elif i % 2 == 1 and card_set[i+1].power + 1 == card_set[i+2].power:
                        pass
                    elif phoenix_used:
                        is_pair_seq = False
                        break
                    else:
                        phoenix_used = True
            if is_pair_seq == True:
                self.type = 'pair_seq'
                self.power = card_set[-1].power
                return
        # no combination must be a hand
        if self.type == 'unk':
            self.type = 'hand'
            self.power = 0

    # get all available combinations from this card set
    def get_available_combinations(self):
        # TODO
        return
       