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
        self.state_size = 232
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
        self.state = [[None], [None], [None], [None]]
        self.rewards = [None, None, None, None]
        self.done = False
        self.reset()
        return

    def reset(self):
        self.game = Game(verbose=self.verbose)
        self._reset_all_states()
        self.rewards = [None, None, None, None]
        self.done = False
        return self.state, self.rewards, self.done

    def step(self, player_id, action):
        # TODO
        return self.state, self.rewards, self.done, self.game.active_player

    def _reset_all_states(self):
        """
        # initial game state of player i:
        # i:     [hand_size, tichu_flag, hand_cards (1/0 of all_cards)]
        # i + 1: [hand_size, tichu_flag, played_cards (0 initially)]
        # i + 2: [hand_size, tichu_flag, played_cards (0 initially)]
        # i + 3: [hand_size, tichu_flag, played_cards (0 initially)]
        """
        for i in range(4):
            this_player = i
            player_state = list()
            for i in range(4):
                pid = (this_player + i)%4
                hand_size = self.game.players[pid].hand_size
                tichu_flag = int(self.game.players[pid].tichu_flag)
                if pid == this_player:
                    player_cards = self._cards_to_vec(self.game.players[pid].hand)
                else:
                    player_cards = np.zeros(len(self.all_cards), int).tolist()
                player_state.append([hand_size, tichu_flag, player_cards])
            self.state[i] = player_state
        return 

    def _cards_to_vec(self, cards):
        vec = np.zeros(len(self.all_cards), int)
        for i in range(len(self.all_cards)):
            crd = Cards([self.all_cards[i]])
            if cards.contains(crd):
                vec[i] = 1
        return vec.tolist()

    def _vec_to_cards(self, vec):
        return Cards(list(compress(self.all_cards, vec)))
