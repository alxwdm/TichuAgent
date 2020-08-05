# Game class for Python Implementation of Tichu

import random

from env.Cards import Cards
from env.Deck import Deck
from env.Player import Player
from env.Stack import Stack

class Game():

    def __init__(self, verbose=0):

        # Create deck and distribute
        deck = Deck()
        sets = deck.shuffle_and_deal()

        # Create players and assign hands
        self.players = list()
        for i in range(4):
            self.players.append(Player(id=i))
            self.players[i].assign_hand(sets[i])
            if self.verbose > 0:
                print('Player {0} hand is:'.format(i))
                self.players[i].hand.show()

        # Create empty stack
        self.stack = Stack()

        # Game managing parameter
        self.active_player = random.randint(0,3)
        self.leading_player = None
        self.players_finished = list()
        self.pass_counter = 0
        self.game_finished = False
        self.verbose = verbose

    def step(self, player_id, cards):
        if not(player_id == self.active_player):
            if verbose > 0:
                print('Player {0} tried to make a move, but active player is {1}.'.format(
                    player_id, self.active_player))
            return
        # active player passes 
        if isempty(cards):
            if verbose > 0:
                print('Player {0} passes'.format(player_id))
            self.pass_counter += 1
            # stack is finished when 3 players have passed
            if self.pass_counter >= 3:
                # if stack contains Dragon, it must be given to opponent player
                if self.stack.dragon_flag:
                    self._dragon_stack() 
                else:
                    self.player[self.leading_player].add_points(self.stack.points)
                # initialize new round 
                self.stack = Stack()
                self.active_player = self.leading_player
                self.pass_counter = 0
            # stack not finished, next players turn
            else:
                self.active_player += 1 # TODO modulo
            return True
        # active player plays cards
        else:
            # check if cards to play is in hands of player 
            suc1 = self.player[player_id].move(cards)
            # try to add cards to current stack
            suc2 = self.stack.add(cards)
            if suc1 and suc2:
                self.leading_player = player_id
                self.active_player += 1 # TODO modulo
                suc = self.player[player_id].remove_cards(cards)
                if not(suc): # This should never happen
                    print('Could not remove players cards.')
                    return
                self.pass_counter = max(0, self.pass_counter-1)
                if self.verbose > 0:
                    print('Player {0} plays {1}.'.format(player_id, cards.type))
                    cards.show()
                # check if player has finished
                if self.player[player_id].finished:
                    if self.verbose > 0:
                        print('Player {0} has finished on position {1}!'.format(
                            player_id, len(self.players_finished)+1))
                    self.players_finished.append(player_id)
                    # check if game has finished
                    # double-team victory, game is finished and points by cards are discarded
                    if len(self.players_finished) == 2 and sum(self.players_finished)%2 == 0:
                        if self.verbose > 0:
                            print('Double team victory by players {0} and {1}!'.format(
                                player_id,self._get_teammate()))
                        opponents = self._get_opponents()
                        teammate = self._get_teammate()
                        self.player[player_id].set_points(100)
                        self.player[teammate].set_points(100)
                        self.player[opponents[0]].set_points(0)
                        self.player[opponents[1]].set_points(0)
                        self.game_finished = True
                    # if player called tichu and finished, check if tichu is successfull
                    if self.player[player_id].tichu_flag:
                        if len(self.players_finished == 1):
                            self.player[player_id].add_points(100)
                            if self.verbose > 0:
                                print('Successfull Tichu by player {0}!'.format(player_id))
                        else:
                            self.player[player_id].add_points(-100)
                            if self.verbose > 0:
                                print('Tichu by player {0} was not successfull!'.format(player_id))
                    # regular game end
                    elif len(self.players_finished) == 3:
                        # get first and last finisher
                        first = self.players_finished[0]
                        for i in range(4):
                            if not(self.players[i].finished):
                                last = i
                        # opponent team gets hand of last finisher
                        hand_points_last = self.players[last].hand.points
                        opponents = self._get_opponents(pid=last)
                        self.players[opponents[0]].add_points(hand_points_last)
                        # first finisher gets stack of last finisher
                        stack_points_last = self.players[last].points
                        self.players[first].add_points(stack_points_last)
                        self.players[last].set_points(0)
                        if self.verbose > 0:
                            print('Game is finished!')
                            print('Score of player 0 and player 2: {0}'.format(
                                (self.players[0].points + self.players[2].points)))
                            print('Score of player 1 and player 3: {0}'.format(
                                (self.players[1].points + self.players[3].points)))
                return True
            # invalid move
            else:
                if self.verbose > 0:
                    print('Invalid move by player {0}'.format(player_id))
                return False

    def show_hands(self, pid=None):
        if pid:
            print('Player {0} hand is:'.format(pid))
            self.players[pid].hand.show()              
        else: # show all hands if pid not specified
            for i in range(4):
                print('Player {0} hand is:'.format(i))
                self.players[i].hand.show()            

    def _get_opponents(self, pid=self.leading_player):
        if pid%2 == 0:
            opps = [1, 3]
        else:
            opps = [0, 2]
        return opps

    def _get_teammate(self, pid=self.leading_player):
        if pid == 0:
            return 2
        elif pid == 1:
            return 3
        elif pid == 2:
            return 0
        else:
            return 1

    def _dragon_stack(self):
        # give dragon stack to opponent player according to a simple heuristic
        # determine opponents
        opponents = self._get_opponents
        # if either opponent has called tichu, give cards to other opponent
        if self.player[opponents[0]].tichu_flag:
            self.player[opponents[1]].add_points(self.stack.points)
        elif self.player[opponents[1]].tichu_flag:
            self.player[opponents[0]].add_points(self.stack.points)
        # if no tichu called by opposite team, give dragon to player with more hand cards
        elif self.player[opponents[0]].hand_size < self.player[opponents[1]].hand_size:
            self.player[opponents[1]].add_points(self.stack.points)
        else:
            self.player[opponents[0]].add_points(self.stack.points)
