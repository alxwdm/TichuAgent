# Stack class for Python Implementation of Tichu

from env.Cards import Cards

BOMBS = ['four_bomb', 'straight_bomb']

class Stack():

    def __init__(self):
        
        self.cards_list = list()
        self.points = 0
        self.power = 0
        self.type = None
        self.dragon_flag = False

    def _set_power(self):
        self.power = self.cards_list[-1].power

    def _set_points(self):
        self.points = sum(crds.points for crds in self.cards_list)

    def _set_type(self):
        self.type = self.cards_list[-1].type

    def _set_dragon_flag(self):
        name_list = [crd.name for crds in self.cards_list for crd in crds.cards]
        if 'Dragon' in name_list:
            self.dragon_flag = True

    def _update(self):
        self._set_power()
        self._set_points()
        self._set_type()
        self._set_dragon_flag()

    def add(self, cards_to_add):
        # add cards to stack according to game rules
        if not self.cards_list and cards_to_add.type != 'hand':
            self.cards_list.append(cards_to_add)
            self._update()
            return True
        elif self.type == cards_to_add.type and self.power < cards_to_add.power:
            if self.type == 'straight' and len(self.cards) == len(cards_to_add.cards):
                self.cards_list.append(cards_to_add)
                self._update()
                return True
            else:
                 return False
        elif self.type == 'solo' and cards_to_add.phoenix_flag and self.power < 15:
            old_power = self.power
            self.cards_list.append(cards_to_add)
            self._update()
            self.power = old_power + 0.5           
            return True   
        elif cards_to_add.type in BOMBS and self.power < cards_to_add.power:
            self.cards_list.append(cards_to_add)
            self._update()      
            return True
        else: # illegal move
            return False 

    # check if new_cards is a valid move on old_cards
    @staticmethod
    def check_valid_move(old_cards, new_cards):
        if not(old_cards) and new_cards.type != 'hand':
            return True
        elif old_cards.type == new_cards.type and old_cards.power < new_cards.power:
            if self.type == 'straight' and len(self.cards) == len(cards_to_add.cards):
                return True
            else:
                return False
        elif old_cards.type == 'solo' and new_cards.phoenix_flag and old_cards.power < 15:
            return True 
        elif new_cards.type in BOMBS and old_cards.power < new_cards.power:
            return True
        else:
            return False
