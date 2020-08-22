# Env class for Python Implementation of Tichu
# A wrapper for Game class to enable reinforcement learning

import numpy as np
from itertools import compress

from env.cards import Cards
from env.deck import Deck
from env.game import Game

ILLEGAL_MOVE_PENALTY = -10
REWARD_STYLE  = 'rich'

class Env():

    def __init__(self, train_mode=True):
        # dispatch table for reward function
        self.dispatch_reward = {'rich': self._update_rich_rewards,
                                'sparse': self._update_sparse_rewards}
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
        self.action_buffer = [[None], [None], [None], [None]]
        self.state = [[None], [None], [None], [None]]
        self.rewards = [None, None, None, None]
        self.done = False
        self.pass_counter = 0 # only for debugging
        return

    def reset(self):
        self.game = Game(verbose=self.verbose)
        self._reset_all_states()
        self._reset_rewards()
        self.done = False
        state = self.state
        rewards = self.rewards
        done = self.done
        active_player = self.game.active_player
        return state, rewards, done, active_player

    def step(self, player_id, action):
        # convert action vector and make game step
        cards = self._vec_to_cards(action)
        suc, points_this_step = self.game.step(player_id, cards)
        # illegal move
        if not(suc):
            self.rewards[player_id] = ILLEGAL_MOVE_PENALTY
        # legal move
        else:
            self._update_action_buffer(player_id, action)
            self._update_all_states()
            # reset state and action buffer if stack has been emptied 
            # and update rewards according to points in the stack
            if not(self.game.stack.cards):
                self._reset_all_states()
                self._reset_action_buffer() 
                self._update_rewards(points_this_step)
            # update rewards for pass move
            elif cards.type == 'pass':
                self._update_rewards(points_this_step)
            # reset state, action_buffer and rewards if Dog has been played
            # (required because Dog skips players)
            elif cards.cards[0].name == 'Dog':
                self._reset_all_states()
                self._reset_action_buffer()
                self._reset_rewards()
           # update rewards for regular game move
            else:
                self._update_rewards(points_this_step)
        # check if game is finished
        if self.game.game_finished:
            self.done = True
        # return step variables
        state = self.state
        rewards = self.rewards
        done = self.done
        active_player = self.game.active_player
        # only for debugging
        if cards.type == 'pass':
            self.pass_counter += 1
            if self.pass_counter >= 10:
                done = True
                print('Loop detected, aborting...')
        else:
            self.pass_counter = 0
        return state, rewards, done, active_player

    def _reset_all_states(self):
        """
        # initial game state of player i:
        # i:     [hand_size, tichu_flag, hand_cards (1/0 of all_cards)]
        # i + 1: [hand_size, tichu_flag, played_cards (0 initially)]
        # i + 2: [hand_size, tichu_flag, played_cards (0 initially)]
        # i + 3: [hand_size, tichu_flag, played_cards (0 initially)]
        """
        self.state = list()
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
            self.state.append(player_state)
        return 

    def _update_all_states(self):
        # updates states with latest action taken by other players
        self.state = list()
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
                    player_cards = self.action_buffer[pid]
                player_state.append([hand_size, tichu_flag, player_cards])
            self.state.append(player_state) 
        return

    def _reset_action_buffer(self):
        for i in range(4):
            self.action_buffer[i] = np.zeros(len(self.all_cards), int).tolist()
        return

    def _update_action_buffer(self, player_id, action):
        self.action_buffer[player_id] = action
        return

    def _reset_rewards(self):
        self.rewards = [0, 0, 0, 0]
        self.nstep = self.game.active_player
        return

    def _update_rewards(self, points_this_step):
        self.dispatch_reward[REWARD_STYLE](points_this_step)
        return

    def _update_rich_rewards(self, points_this_step):
        """
        This implemenation of a reward function promises rewards after
        each round (i.e. consecutive steps of all 4 players).
        If a player or its teammate (!) gets points during a round 
        (e.g. by winning a stack), it gets a reward in the amount of 
        the points in this round.
        The benefit of this reward function is that each step promises a reward
        (i.e. no sparse rewards that may impede learning).
        The danger is that the actual points are assigned at the end of a game, 
        which means the last player looses all its points to the first finisher.
        This may lead to a non-ideal game strategy, where lots of rewards might 
        be collected during the game, but actually the game is lost if the player 
        does not finish early.
        Also, cummulative reward is higher for players that finish later.
        However, if the winning team gets more cumulative reward, then this
        reward design will still lead to a good policy.
        """
        # reset rewards every new player round
        self.rewards[self.nstep] = 0
        # accumulate rewards (teammate rewards are also taken into account)
        # opponent rewards are considered negative
        rewards_team_0 = (points_this_step[0] + points_this_step[2])
        rewards_team_1 = (points_this_step[1] + points_this_step[3])
        self.rewards[0] += (rewards_team_0 - rewards_team_1)
        self.rewards[1] += (rewards_team_1 - rewards_team_0)
        self.rewards[2] += (rewards_team_0 - rewards_team_1)
        self.rewards[3] += (rewards_team_1 - rewards_team_0)
        # update nstep counter
        self.nstep = (self.nstep+1)%4
        return

    def _update_sparse_rewards(self, points_this_step):
        raise NotImplementedError("TODO")

    def _cards_to_vec(self, cards):
        vec = np.zeros(len(self.all_cards), int)
        for i in range(len(self.all_cards)):
            crd = Cards([self.all_cards[i]])
            if cards.contains(crd):
                vec[i] = 1
        return vec.tolist()

    def _vec_to_cards(self, vec):
        return Cards(list(compress(self.all_cards, vec)))
