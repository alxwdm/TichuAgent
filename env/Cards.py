# Cards class for Python Implementation of Tichu
# Sources:
#  - https://github.com/hundredblocks/ticher
#  - https://github.com/sylee421/TichuRL

import random
from collections import defaultdict

from env.Card import Card

BOMBS = ['four_bomb', 'straight_bomb']

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

        self._set_type_and_power()
        self._set_points()

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
    def _set_points(self):
        if self.type != 'pass':
            self.points = sum([crd.points for crd in self.cards])
        else:
            self.points = 0

    # determine which combination (if any) is this card set
    def _set_type_and_power(self):
        card_set = self.cards
        card_set.sort()
        phoenix_flag = self.phoenix_flag
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
            elif phoenix_flag and not (card_set[1].name == 'Dragon'):
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
            elif phoenix_flag and card_set[1].power == card_set[2].power:
                self.type = 'triple'
                self.power = card_set[1].power
                return
        # four (BOMB)
        if len(card_set)==4 and card_set[0].power == card_set[1].power and card_set[1].power == card_set[2].power and card_set[2].power == card_set[3].power:
            self.type = 'four_bomb'
            self.power = 50 + card_set[0].power
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
            elif phoenix_flag and card_set[1].power == card_set[2].power and card_set[3].power == card_set[4].power:
                self.type = 'full'
                self.power = card_set[3].power
                return
            # phoenix full house with phoenix pair
            elif phoenix_flag:
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
                self.power = 100 + card_set[-1].power
                return
            if is_straight:
                self.type = 'straight'
                self.power = card_set[-1].power
                return
            # phoneix straight
            if phoenix_flag:
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
        if len(card_set) >= 4 and len(card_set) % 2 == 0 and not(any((crd.name == 'Dog' or crd.name == 'Dragon') for crd in card_set)):
            is_pair_regular = True
            for i in range(len(card_set)-1):
                if i % 2 == 0 and card_set[i].power == card_set[i+1].power:
                    pass
                elif i % 2 == 1 and card_set[i].power + 1 == card_set[i+1].power:
                    pass
                else:
                    is_pair_regular = False
                    break
            if is_pair_regular:
                self.type = 'pair_seq'
                self.power = card_set[-1].power
                return  
            # phoenix pair sequence (quite complicated to get all valid cases)
            if phoenix_flag:
                # first, check if it is an increasing by +1 sequence
                unique_power = sorted(set([crd.power for crd in card_set]))
                unique_power.pop(0) # remove phoenix
                if all(x+1==y for x, y in zip(unique_power, unique_power[1:])) and len(unique_power)>1:
                    phoenix_used = False
                    is_pair_equal = True
                    is_pair_unequal = True
                    # check for phoenix use in 'unequal' index
                    toggle = 1
                    antitoggle = 0
                    for i in range(1,len(card_set)-1):
                        if i % 2 == toggle and card_set[i].power == card_set[i+1].power:
                            pass
                        elif i % 2 == antitoggle and card_set[i].power + 1 == card_set[i+1].power:
                            if i+1 >= len(card_set)-1 and not(phoenix_used):
                                # phoenix is used as the highest pair of sequence
                                phoenix_used = True
                        elif phoenix_used: # phoenix cannot be used twice
                            is_pair_unequal = False
                            break
                        else:
                            # phoenix is used in the middle of the sequence 
                            # -> set consequence of i % 2 accordingly by toggling 1 and 0
                            phoenix_used = True
                            toggle = 0
                            antitoggle = 1
                    # check for phoenix use in 'equal' index (only if unequal is False)
                    if not(is_pair_unequal):
                        phoenix_used = False
                        for i in range(1,len(card_set)-1):
                            if i % 2 == 0 and card_set[i].power == card_set[i+1].power:
                                pass
                            elif i % 2 == 1 and card_set[i].power + 1 == card_set[i+1].power:
                                # check if phoenix is used as first card of the sequence
                                if i == 1:
                                    phoenix_used = True
                            elif phoenix_used: # phoenix cannot be used twice
                                is_pair_equal = False
                                break
                            else:
                                phoenix_used = True            
                    if is_pair_unequal or is_pair_equal:
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
        return # list of cards

    def contains(self, other):
        this_cards = [(crd.name, crd.suit) for crd in self.cards]
        other_cards = [(crd.name, crd.suit) for crd in other.cards]
        return all([elem in this_cards for elem in other_cards])

    def remove(self, card):
        try:
            self.cards.remove(card)
        except: # if card is not in cards, return False
            return False
        self.cards.sort()
        if card.name == 'Phoenix':
            self.phoenix_flag = False
        self.size = self.size - 1
        self._set_type_and_power()
        self._set_points()
        return True

    def __add__(self, card_list_to_add):
        this_card_list = self.cards
        this_card_list.append(card_list_to_add)
        new_cards = Cards(card_list=this_card_list)
        return new_cards

    def __sub__(self, cards):
        this_card_list = self.cards
        for crd in cards:
            this_card_list.remove(crd)
        new_cards = Cards(card_list=this_card_list)
        return new_cards

    def __ge__(self, other):
        # equal types or bombs, compare power
        if (self.type == other.type and self.size == other.size) or self.type in BOMBS or other.type in BOMBS: 
            return self.power >= other.power
        # unequal types, return False (opt: raise error)
        else: 
            return False

    def __le__(self, other):
        # equal types or bombs, compare power
        if (self.type == other.type and self.size == other.size) or self.type in BOMBS or other.type in BOMBS:
            return self.power <= other.power
        # unequal types, return False (opt: raise error)
        else: 
            return False

    def __gt__(self, other):
        # equal types or bombs, compare power
        if (self.type == other.type and self.size == other.size) or self.type in BOMBS or other.type in BOMBS:
            return self.power > other.power
        # unequal types, return False (opt: raise error)
        else: 
            return False

    def __lt__(self, other):
        # equal types or bombs, compare power
        if (self.type == other.type and self.size == other.size) or self.type in BOMBS or other.type in BOMBS:
            return self.power < other.power
        # unequal types, return False (opt: raise error)
        else: 
            return False

    def __eq__(self, other):
        return self.type == other.type and self.size == other.size and self.power == other.power

    def __ne__(self, other):
        return self.type != other.type and self.size != other.size and self.power != other.power

    def __repr__(self):
        card_str = ''
        for crd in self.cards:
            card_str = card_str + str(crd.name) + ' ' + str(crd.suit) + ' ,'
        return str({'type': self.type,
                    'size': self.size,
                    'cards': card_str})
