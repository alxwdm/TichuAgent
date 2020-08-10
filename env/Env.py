# Env class for Python Implementation of Tichu
# A wrapper for Game class to enable reinforcement learning

import numpy as np

from env.Cards import Cards
from env.Deck import Deck
from env.Game import Game

class Env():

    def __init__(self, train_mode=True):
        # set verbosity according to mode
        if train_mode:
            self.verbose = 0
        else:
            self.verbose = 1
        self.state_size = 0 # TODO
        self.action_size = 0 # TODO
        self.all_cards = Deck().all_cards
        """ 
        all_cards:
        [Spd_2 , Hrt_2 , Dia_2 , Clb_2,    
        Spd_3 , Hrt_3 , Dia_3 , Clb_3,
        Spd_4 , Hrt_4 , Dia_4 , Clb_4,
        Spd_5 , Hrt_5 , Dia_5 , Clb_5, 
        Spd_6 , Hrt_6 , Dia_6 , Clb_6, 
        Spd_7 , Hrt_7 , Dia_7 , Clb_7, 
        Spd_8 , Hrt_8 , Dia_8 , Clb_8,
        Spd_9 , Hrt_9 , Dia_9 , Clb_9,
        Spd_10 , Hrt_10 , Dia_10 , Clb_10,
        Spd_J , Hrt_J , Dia_J , Clb_J,
        Spd_Q , Hrt_Q , Dia_Q , Clb_Q,
        Spd_K , Hrt_K , Dia_K , Clb_K,
        Spd_A , Hrt_A , Dia_A , Clb_A,
        Phoenix, Dragon, Majong, Dog] 
        """
        [state, reward, done] = self.reset()
        return [state, reward, done]

    def reset(self):
        self.game = Game(verbose=self.verbose)
        return [state, reward, done]

    def step(self, action, player_id=None):
        # TODO
        return [state, reward, done]

    def _get_state(self):
        # TODO
        # state is always from perspective of active player
        # active_player:     [hand_size, tichu_flag, all_cards (0 / 1 if in hands)]
        # active_player + 1: [hand_size, tichu_flag, all_cards (0 / 1 if played)]
        # active_player + 2: [hand_size, tichu_flag, all_cards (0 / 1 if played)]
        # active_player + 3: [hand_size, tichu_flag, all_cards (0 / 1 if played)]
        return state

    def _cards_to_vec(self, cards):
        contains_list = [crd in cards for crd in self.all_cards]
        return np.asarray(contains_list, int)

    def _vec_to_cards(self, vec):
        # TODO
        return cards

    def _get_rewards_from_game(self):
        # TODO
        return reward
