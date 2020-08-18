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

        # Set verbosity
        self.verbose = verbose

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
        for i in range(4):
            for crd in self.players[i].hand.cards:
                if crd.name == 'Majong':
                    self.active_player = i # Player with Majong starts
        self.leading_player = None
        self.players_finished = list()
        self.pass_counter = 0
        self.game_finished = False

    def step(self, player_id, cards):
        points_this_step = [0, 0, 0, 0]
        if not(player_id == self.active_player):
            if self.verbose > 0:
                print('Player {0} tried to make a move, but active player is {1}.'.format(
                    player_id, self.active_player))
            return False, points_this_step
        # active player passes 
        if cards.type == 'pass':
            if self.verbose > 0:
                print('Player {0} passes'.format(player_id))
            self.pass_counter += 1
            # stack is finished when 3 players have passed
            if self.pass_counter >= 3:
                # if stack contains Dragon, it must be given to opponent player
                if self.stack.dragon_flag:
                    points_this_step = self._dragon_stack() 
                else:
                    self.players[self.leading_player].add_points(self.stack.points)
                    points_this_step[self.leading_player] = self.stack.points
                # initialize new round 
                self.stack = Stack()
                # transmit leading player if player has finished
                # (but do not skip finished players from being active)
                if not(self.leading_player in self.players_finished):
                    self.active_player = self.leading_player
                elif not((self.leading_player+1)%4 in self.players_finished):
                    self.leading_player = (self.leading_player+1)%4
                elif not((self.leading_player+2)%4 in self.players_finished):
                    self.leading_player = (self.leading_player+2)%4
                else:
                    self.leading_player = (self.leading_player+3)%4
                self.pass_counter = 0
            # stack not finished, next players turn
            else:
                self.active_player = (player_id+1)%4
            return True, points_this_step
        # active player plays cards
        else:
            # check if cards to play is in hands of player 
            suc1 = self.players[player_id].move(cards)
            # try to add cards to current stack
            suc2 = self.stack.add(cards)
            if suc1 and suc2:
                if cards.cards[0].name == 'Dog':
                    teammate = self._get_teammate(player_id)
                    if not(teammate in self.players_finished):
                        self.active_player = teammate
                        self.leading_player = teammate
                    elif not((teammate+1)%4 in self.players_finished):
                        self.active_player = (teammate+1)%4
                        self.leading_player = (teammate+1)%4
                    elif not((self.leading_player+2)%4 in self.players_finished):
                        self.active_player = (teammate+2)%4
                        self.leading_player = (teammate+2)%4
                    else:
                        self.active_player = (teammate+3)%4
                        self.leading_player = (teammate+3)%4
                    self.stack = Stack()
                else:
                    self.leading_player = player_id
                    self.active_player = (player_id+1)%4 
                suc = self.players[player_id].remove_cards(cards)
                if not(suc): # This should never happen
                    print('Could not remove players cards.')
                    return
                self.pass_counter = 0
                if self.verbose > 0:
                    print('Player {0} plays {1}.'.format(player_id, cards.type))
                    cards.show()
                # check if player has finished
                if self.players[player_id].finished:
                    if self.verbose > 0:
                        print('Player {0} has finished on position {1}!'.format(
                            player_id, len(self.players_finished)+1))
                    self.players_finished.append(player_id)
                    if not(cards.cards[0].name == 'Dog'):
                        self.active_player = (player_id+1)%4
                    # check if game has finished
                    # double-team victory, game is finished and points by cards are discarded
                    if len(self.players_finished) == 2 and sum(self.players_finished)%2 == 0:
                        if self.verbose > 0:
                            print('Double team victory by players {0} and {1}!'.format(
                                self.players_finished[0],self.players_finished[1]))
                        opponents = self._get_opponents()
                        teammate = self._get_teammate()
                        self.players[player_id].set_points(100)
                        self.players[teammate].set_points(100)
                        self.players[opponents[0]].set_points(0)
                        self.players[opponents[1]].set_points(0)
                        points_this_step[player_id] = 100
                        points_this_step[teammate] = 100
                        points_this_step[opponents[0]] = 0
                        points_this_step[opponents[1]] = 0
                        self.game_finished = True
                    # if player called tichu and finished, check if tichu is successfull
                    if self.players[player_id].tichu_flag:
                        if len(self.players_finished == 1):
                            self.players[player_id].add_points(100)
                            points_this_step[player_id] += 100
                            if self.verbose > 0:
                                print('Successfull Tichu by player {0}!'.format(player_id))
                        else:
                            self.players[player_id].add_points(-100)
                            points_this_step[player_id] -= 100
                            if self.verbose > 0:
                                print('Tichu by player {0} was not successfull!'.format(player_id))
                    # regular game end
                    elif len(self.players_finished) == 3:
                        self.game_finished = True
                        # get first and last finisher
                        first = self.players_finished[0]
                        for i in range(4):
                            if not(self.players[i].finished):
                                last = i
                        # opponent team gets hand of last finisher
                        hand_points_last = self.players[last].hand.points
                        opponents = self._get_opponents(pid=last)
                        self.players[opponents[0]].add_points(hand_points_last)
                        points_this_step[opponents[0]] = hand_points_last
                        # first finisher gets stack of last finisher
                        stack_points_last = self.players[last].points
                        self.players[first].add_points(stack_points_last)
                        points_this_step[first] += stack_points_last
                        self.players[last].set_points(0)
                        points_this_step[last] = 0
                        # if remaining player called tichu -> tichu failed
                        if self.players[last].tichu_flag:
                            self.players[last].add_points(-100)
                            points_this_step[last] -= 100
                        if self.verbose > 0:
                            print('Game is finished!')
                            print('Score of player 0 and player 2: {0}'.format(
                                (self.players[0].points + self.players[2].points)))
                            print('Score of player 1 and player 3: {0}'.format(
                                (self.players[1].points + self.players[3].points)))
                return True, points_this_step
            # invalid move
            else:
                if self.verbose > 1:
                    print('Invalid move by player {0}'.format(player_id))
                return False, points_this_step

    def show_hands(self, pid=None):
        if pid:
            print('Player {0} hand is:'.format(pid))
            self.players[pid].hand.show()              
        else: # show all hands if pid not specified
            for i in range(4):
                print('Player {0} hand is:'.format(i))
                self.players[i].hand.show()            

    def _get_opponents(self, pid=None):
        if not(pid):
            pid = self.leading_player
        if pid%2 == 0:
            opps = [1, 3]
        else:
            opps = [0, 2]
        return opps

    def _get_teammate(self, pid=None):
        if not(pid):
            pid = self.leading_player
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
        opponents = self._get_opponents()
        points_this_step = [0, 0, 0, 0]
        # if either opponent has called tichu, give cards to other opponent
        if self.players[opponents[0]].tichu_flag:
            self.players[opponents[1]].add_points(self.stack.points)
            points_this_step[opponents[1]] = self.stack.points
            if self.verbose > 0:
                print('Player {0} gave dragon stack to player {1}'.format(
                    self.leading_player, opponents[1]))            
        elif self.players[opponents[1]].tichu_flag:
            self.players[opponents[0]].add_points(self.stack.points)
            points_this_step[opponents[0]] = self.stack.points
            if self.verbose > 0:
                print('Player {0} gave dragon stack to player {1}'.format(
                    self.leading_player, opponents[0]))
        # if no tichu called by opposite team, give dragon to player with more hand cards
        elif self.players[opponents[0]].hand_size < self.players[opponents[1]].hand_size:
            self.players[opponents[1]].add_points(self.stack.points)
            points_this_step[opponents[1]] = self.stack.points
            if self.verbose > 0:
                print('Player {0} gave dragon stack to player {1}'.format(
                    self.leading_player, opponents[1]))
        else:
            self.players[opponents[0]].add_points(self.stack.points)
            points_this_step[opponents[0]] = self.stack.points
            if self.verbose > 0:
                print('Player {0} gave dragon stack to player {1}'.format(
                    self.leading_player, opponents[0]))
        return points_this_step
