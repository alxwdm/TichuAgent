# Env class for Python Implementation of Tichu
# A wrapper for Game class to enable reinforcement learning

import numpy as np
from itertools import compress

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
        self.action_size = 56
        self.all_cards = Deck().all_cards
        """ 
        all_cards is a list containing:
        [Spd_2 , Hrt_2 , Dia_2 , Clb_2, Spd_3 , Hrt_3 , Dia_3 , Clb_3,
        Spd_4 , Hrt_4 , Dia_4 , Clb_4, Spd_5 , Hrt_5 , Dia_5 , Clb_5, 
        Spd_6 , Hrt_6 , Dia_6 , Clb_6, Spd_7 , Hrt_7 , Dia_7 , Clb_7, 
        Spd_8 , Hrt_8 , Dia_8 , Clb_8, Spd_9 , Hrt_9 , Dia_9 , Clb_9,
        Spd_10 , Hrt_10 , Dia_10 , Clb_10, Spd_J , Hrt_J , Dia_J , Clb_J,
        Spd_Q , Hrt_Q , Dia_Q , Clb_Q, Spd_K , Hrt_K , Dia_K , Clb_K,
        Spd_A , Hrt_A , Dia_A , Clb_A, Phoenix, Dragon, Majong, Dog] 
        """
        self.game = None
        self.state = None
        self.rewards = None
        self.done = False
        self.reset()
        return

    def reset(self):
        self.game = Game(verbose=self.verbose)
        self.state = self._reset_state()
        self.rewards = np.zeros(4)
        self.done = False
        return self.state, self.rewards, self.done

    def step(self, action, player_id=None):
        # TODO
        return self.state, self.rewards, self.done

    def _reset_state(self):
        """
        # initial game state
        # state is always from perspective of active player
        # active_player:     [hand_size, tichu_flag, all_cards (0 / 1 if in hands)]
        # active_player + 1: [hand_size, tichu_flag, played_cards (0)]
        # active_player + 2: [hand_size, tichu_flag, played_cards (0)]
        # active_player + 3: [hand_size, tichu_flag, played_cards (0)]
        """
        state = list()
        active_player = self.game.active_player
        for i in range(4):
            pid = (active_player + i)%4
            hand_size = self.game.players[pid].hand_size
            tichu_flag = self.game.players[pid].tichu_flag
            if pid == active_player:
                player_cards = self._cards_to_vec(self.game.players[pid].hand)
            else:
                player_cards = np.zeros(len(self.all_cards)).tolist()
            state.append([hand_size, tichu_flag, player_cards])
        self.state = state
        return 

    def _cards_to_vec(self, cards):
        contains_list = [crd in cards for crd in self.all_cards]
        return np.asarray(contains_list, int).tolist()

    def _vec_to_cards(self, vec):
        return Cards(list(compress(self.all_cards, vec)))

