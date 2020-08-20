# Utility functions for Python Implementation of Tichu

# import all
from env.card import Card
from env.cards import Cards
from env.deck import Deck
from env.stack import Stack
from env.player import Player
from env.game import Game
from env.env import Env

COMB_TYPES = {'solo': 0,
              'pair': 1,
              'triple': 2,
              'four_bomb': 3,
              'full': 4,
              'straight': 5,
              'straight_bomb': 6,
              'pair_seq': 7}

def play_dumb_game(max_steps=1000, verbose=1):
    """
    This function plays a Tichu game with four "dumb" players.
    Each player iterates over available combinations and tries to beat opponents.
    """
    game = Game(verbose=verbose)
    step_cnt = 0
    game_active = True
    while game_active:
        active_player = game.active_player
        leading_player = game.leading_player
        # make a random move if stack is empty
        if not(game.stack.cards) and not(game.players[active_player].has_finished()):
            comb = game.players[active_player].random_move()
            suc, _ = game.step(active_player, comb)
        # try to make a matching move if opponent is leading
        elif ((active_player+leading_player)%2) !=0:
            leading_type = game.stack.type
            leading_idx = COMB_TYPES[leading_type]
            avail_comb = game.players[active_player].hand.get_available_combinations()
            # try to play, starting with lowest combination
            suc = False
            if avail_comb[leading_idx]:
                for i in range(len(avail_comb[leading_idx])):
                    suc, _ = game.step(active_player, avail_comb[leading_idx][i])  
                    if suc:
                        break
            # Try to bomb if no combination exists
            if not(suc) and avail_comb[COMB_TYPES['four_bomb']]:
                suc, _ = game.step(active_player, avail_comb[COMB_TYPES['four_bomb']][0])
            elif not(suc) and avail_comb[COMB_TYPES['straight_bomb']]:
                suc, _ = game.step(active_player, avail_comb[COMB_TYPES['straight_bomb']][0])
            # pass if nothing works
            elif not(suc):
                suc, _ = game.step(active_player, Cards([]))
        # pass if teammate is leading player
        else:
            suc, _ = game.step(active_player, Cards([]))
        # stop if game is finished (or counter overflow)
        step_cnt += 1
        if game.game_finished or step_cnt >= max_steps:
            game_active=False
            if step_cnt >= max_steps and verbose > 1:
                print('max_steps exceeded, aborting game.')
            break
