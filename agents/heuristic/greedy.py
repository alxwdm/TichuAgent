# A non-AI greedy Tichu Agent
# Always tries to win a stack except teammate is leading

import random
import numpy as np
from itertools import compress

from tichuagent.env.cards import Cards 
from tichuagent.env.deck import Deck

COMB_TYPES = {'solo': 0,
              'pair': 1,
              'triple': 2,
              'four_bomb': 3,
              'full': 4,
              'straight': 5,
              'straight_bomb': 6,
              'pair_seq': 7}

class greedyAgent():

    def __init__(self):
        self.all_cards = Deck().all_cards

    def act(self, state_vec):
        # get info from state
        hand_size = state_vec[0][0]
        hand_cards = self._vec_to_cards(state_vec[0][2])
        opp_cards_0 = self._vec_to_cards(state_vec[1][2])
        teammate_cards = self._vec_to_cards(state_vec[2][2])
        opp_cards_1 = self._vec_to_cards(state_vec[3][2])
        # get available combinations and types from hand cards
        # returns [solo, pair, triple, four_bomb, full, straight, straight_bomb, pair_seq]
        available_comb = hand_cards.get_available_combinations()
        available_types = self._get_available_types(available_comb)
        # pass if player has already finished
        if hand_size < 1:
            action = self._cards_to_vec(Cards([]))
            return action
        # pass if teammate is leading
        elif teammate_cards.power > max(opp_cards_0.power, opp_cards_1.power):
            action = self._cards_to_vec(Cards([]))
            return action
        # if stack is empty, play lowest power of a random combination type
        elif teammate_cards.type == 'pass' and opp_cards_0.type == 'pass' and opp_cards_1.type == 'pass':
            random_type = COMB_TYPES[random.choice(available_types)]
            action = self._cards_to_vec(available_comb[random_type][0])
            return action
        # else try to beat opponent 
        else:
            # determine leading opponent type and power
            if (opp_cards_0.power > opp_cards_0.power) or (opp_cards_1.type == 'pass'):
                leading_type = opp_cards_0.type
                leading_size = opp_cards_0.size
                leading_power = opp_cards_0.power
            else:
                leading_type = opp_cards_1.type
                leading_size = opp_cards_1.size
                leading_power = opp_cards_1.power 
            type_index = COMB_TYPES[leading_type]
            # check if leading type is available and can be beaten
            if available_comb[type_index]:
                for crds in available_comb[type_index]:
                    if crds.cards[0].name == 'Dog': # Dog can only be played alone
                        pass
                    elif crds.power > leading_power and crds.size == leading_size:
                        action = self._cards_to_vec(crds)
                        return action
                # pass if no higher combination available
                action = self._cards_to_vec(Cards([]))
                return action
            # if no combination exists, try to four bomb or straight bomb
            elif available_comb[COMB_TYPES['four_bomb']] and not(leading_type == 'straight_bomb'):
                bomb = available_comb[COMB_TYPES['four_bomb']][0]
                action = self._cards_to_vec(bomb)
                return action
            elif available_comb[COMB_TYPES['straight_bomb']]:
                bomb = available_comb[COMB_TYPES['straight_bomb']][0]
                action = self._cards_to_vec(bomb)
                return action
            # pass if opponent cannot be beaten
            else:
                action = self._cards_to_vec(Cards([]))
                return action

    def _get_available_types(self, available_comb):
        available_types = list()
        for key, value in COMB_TYPES.items():
            if available_comb[value]:
                available_types.append(key)
        return available_types

    def _cards_to_vec(self, cards):
        vec = np.zeros(len(self.all_cards), int)
        for i in range(len(self.all_cards)):
            crd = Cards([self.all_cards[i]])
            if cards.contains(crd):
                vec[i] = 1
        return vec.tolist()

    def _vec_to_cards(self, vec):
        return Cards(list(compress(self.all_cards, vec)))
