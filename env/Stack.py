# Stack class for Python Implementation of Tichu

from env.Cards import Cards

BOMBS = ['four_bomb', 'straight_bomb']

class Stack():

    def __init__(self):
        
        self.cards = list()
        self.points = 0
        self.power = 0
        self.type = None
        self.dragon_flag = False

    def _set_power(self):
        self.power = self.cards[-1].power

    def _set_points(self):
        self.points = sum(crds.points for crds in self.cards)

    def _set_type(self):
        self.type = self.cards[-1].type

    def _set_dragon_flag(self):
        name_list = [crd.name for crds in self.cards for crd in crds.cards]
        if 'Dragon' in name_list:
            self.dragon_flag = True

    def _update(self):
        self._set_power()
        self._set_points()
        self._set_type()
        self._set_dragon_flag()

    def add(self, cards_to_add):
        # add cards to stack according to game rules
        # all but hand and pass can be played on empty stack
        if not self.cards and cards_to_add.type != 'hand' and cards_to_add.type != 'pass':
            self.cards.append(cards_to_add)
            self._update()
            return True
        # if stack contains cards, must be same type and higher power
        elif self.type == cards_to_add.type and self.power < cards_to_add.power:
            # for straight and pair_seq, equal lengths are required
            if self.type == 'straight' and not(self.cards[-1].size == cards_to_add.size):
                return False
            elif self.type == 'pair_seq' and not(self.cards[-1].size == cards_to_add.size):
                return False
            # Dog can only be played as first card
            elif cards_to_add.cards[0].name == 'Dog':
                return False
            # append and update stack if successful move
            else:
                self.cards.append(cards_to_add)
                self._update()
                return True
        # special moves: Phoenix can be played on solo (except Dragon)
        elif self.type == 'solo' and cards_to_add.type == 'solo' and cards_to_add.phoenix_flag and self.power < 15:
            old_power = self.power
            self.cards.append(cards_to_add)
            self._update()
            self.power = old_power + 0.5           
            return True   
        # bombs can be played any time 
        elif cards_to_add.type in BOMBS and self.power < cards_to_add.power:
            self.cards.append(cards_to_add)
            self._update()      
            return True
        # illegal move
        else:
            return False 

    # check if new_cards is a valid move on old_cards
    @staticmethod
    def check_valid_move(old_cards, new_cards):
        if not(old_cards) and new_cards.type != 'hand':
            return True
        elif old_cards.type == new_cards.type and old_cards.power < new_cards.power:
            if old_cards.type == 'straight' and not(len(old_cards.cards) == len(new_cards.cards)):
                return False
            else:
                return True
        elif old_cards.type == 'solo' and new_cards.type == 'solo' and new_cards.phoenix_flag and old_cards.power < 15:
            return True 
        elif new_cards.type in BOMBS and old_cards.power < new_cards.power:
            return True
        else:
            return False
