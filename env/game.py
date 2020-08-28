""" This module contains a class to represent a Tichu Game. """

from env.deck import Deck
from env.player import Player
from env.stack import Stack

# Tichu is called when the hand rating of a Player exceeds the threshold.
TICHU_THRESHOLD = 90 # 90 = roughly 30% Tichu frequency in all games

class Game():
    """
    A class to represent a Tichu game.

    Attributes
    ----------
    verbose: int
      The Players' moves and Game info is printed if verbose > 0.
    players: list of Player
      A list containing all 4 Players of a Tichu Game.
    Stack: Stack
      Players play Cards on top of the Stack in order to win it.
    leading_player: int
      The Player who currently wins the Stack.
    active_player: int
      The Player who is currently in turn to make a move.
    pass_counter: int
      A counter to determine whether a Player won the Stack.
    players_finished: list of int
      A list containing all Players that have finished in order.
    game_finished: bool
      Whether the Game is finished or not.
    tichu_points: list of int
      The points the Players have achieved when Tichu is called.

    Methods
    -------
    step(player_id, cards):
      Continues the Game by making a move of player_id.
    show_hands(player_id):
      Prints the hand Cards of all Players.
    """

    def __init__(self, verbose=0):
        """
        Constructs a Tichu Game, distributes cards and checks Tichu calls.

        Paramter
        --------
        verbose: Whether to print Game states and Players actions.
        """
        # Create deck and distribute cards
        deck = Deck()
        sets = deck.shuffle_and_deal()
        # Set verbosity
        self.verbose = verbose
        # Create players and assign hands
        self.players = list()
        for i in range(4):
            self.players.append(Player())
            self.players[i].assign_hand(sets[i])
            rating = self.players[i].hand_rating
            if self.verbose > 0:
                print('Player {0} hand (rating: {1}) is:'.format(i, rating))
                self.players[i].hand.show()
        # Create empty stack
        self.stack = Stack()
        # Determine active player and set game managing parameter
        for i in range(4):
            for crd in self.players[i].hand.cards:
                # Player with Majong starts
                if crd.name == 'Majong':
                    self.active_player = i
        self.leading_player = None
        self.players_finished = list()
        self.pass_counter = 0
        self.game_finished = False
        # Start Tichu routine, starting from active player
        # Tichu is called if:
        # - hand rating is high enough (i.e. above TICHU_THRESHOLD)
        # - teammate has not called Tichu yet
        self.tichu_points = [0, 0, 0, 0]
        tichu_threshold = TICHU_THRESHOLD
        for i in range(4):
            player_idx = (self.active_player+i)%4
            teammate_idx = self._get_teammate(player_idx)
            if self.players[teammate_idx].tichu_flag:
                pass
            elif self.players[player_idx].hand_rating > tichu_threshold:
                self.players[player_idx].call_tichu()
                if verbose > 0:
                    print('Player {} called Tichu!'.format(player_idx))
            else:
                pass

    def step(self, player_id, cards):
        """
        This function manages a game step:
        - adds cards to stack (if move is valid)
        - assigns stack points to players who won it
        - iterates active player token
        - checks if game is finished
        """
        dispatch_move = {True: self._pass_routine,
                         False: self._play_routine}
        points_this_step = [0, 0, 0, 0]
        # check if action is by active player
        if not player_id == self.active_player:
            if self.verbose > 0:
                print(
                  'Player {0} tried to make a move, but active player is {1}.'
                  .format(player_id, self.active_player))
            return False, points_this_step
        # call either pass or play routine
        suc, points_this_step = dispatch_move[cards.type == 'pass'](
            player_id, cards)
        return suc, points_this_step

    def show_hands(self, pid=None):
        """ Prints current hand cards of pid. """
        if pid:
            print('Player {0} hand is:'.format(pid))
            self.players[pid].hand.show()
        else: # show all hands if pid not specified
            for i in range(4):
                print('Player {0} hand is:'.format(i))
                self.players[i].hand.show()

    def _get_opponents(self, pid=None):
        """ Returns the opponents of pid as list. """
        if not pid:
            pid = self.leading_player
        if pid%2 == 0:
            opps = [1, 3]
        else:
            opps = [0, 2]
        return opps

    def _get_teammate(self, pid=None):
        """ Returns the teammate of pid. """
        if not pid:
            pid = self.leading_player
        if pid == 0:
            return 2
        elif pid == 1:
            return 3
        elif pid == 2:
            return 0
        else:
            return 1

    def _pass_routine(self, player_id, *unused_args):
        """ Changes game state when active player passes. """
        dispatch_pass = {True: self._stack_finished_routine,
                         False: self._stack_continues_routine}
        if self.verbose > 0:
            print('Player {0} passes'.format(player_id))
        # increment pass counter
        self.pass_counter += 1
        # if 3 players have passed, stack is finished
        points_this_step = dispatch_pass[self.pass_counter>=3](player_id)
        return True, points_this_step

    def _stack_finished_routine(self, *unused_args):
        """ Changes game state when stack is won by a player. """
        points_this_step = [0, 0, 0, 0]
        # if stack contains Dragon it must be given to opponent player
        if self.stack.dragon_flag:
            points_this_step = self._dragon_stack()
        else:
        # else, stack points belong to leading player
            self.players[self.leading_player].add_points(
                self.stack.points)
            points_this_step[self.leading_player] = self.stack.points
        # initialize new round
        self.stack = Stack()
        # determine next active and leading player:
        #   if stack winner has not finished, he is next active player
        #   else pass the leading token around, but
        #   do not skip finished players from being active,
        #   they auto-pass to keep the game logic consistent
        if not self.leading_player in self.players_finished:
            self.active_player = self.leading_player
        elif not (self.leading_player+1)%4 in self.players_finished:
            self.leading_player = (self.leading_player+1)%4
            self.active_player = self.leading_player
        elif not (self.leading_player+2)%4 in self.players_finished:
            self.leading_player = (self.leading_player+2)%4
            self.active_player = self.leading_player
        else:
            self.leading_player = (self.leading_player+3)%4
            self.active_player = self.leading_player
        self.pass_counter = 0
        return points_this_step

    def _stack_continues_routine(self, player_id):
        """ ‚Changes game state when stack is still playable. """
        points_this_step = [0, 0, 0, 0]
        self.active_player = (player_id+1)%4
        return points_this_step

    def _play_routine(self, player_id, cards):
        """ Changes game state when active player plays cards. """
        points_this_step = [0, 0, 0, 0]
        dispatch_valid_move = {True: self._valid_move_routine,
                               False: self._invalid_move_routine}
        # plausibility check: cards in hand of player and matches stack type
        suc1 = self.players[player_id].move(cards)
        suc2 = self.stack.add(cards)
        suc, points_this_step = dispatch_valid_move[(suc1 and suc2)](
            player_id, cards)
        return suc, points_this_step

    def _valid_move_routine(self, player_id, cards):
        """ Changes game state when player move is valid. """
        points_this_step = [0, 0, 0, 0]
        # determine next active player
        if cards.cards[0].name == 'Dog':
            teammate = self._get_teammate(player_id)
            if not teammate in self.players_finished:
                self.active_player = teammate
                self.leading_player = teammate
            elif not (teammate+1)%4 in self.players_finished:
                self.active_player = (teammate+1)%4
                self.leading_player = (teammate+1)%4
            elif not ((self.leading_player+2)%4
                      in self.players_finished):
                self.active_player = (teammate+2)%4
                self.leading_player = (teammate+2)%4
            else:
                self.active_player = (teammate+3)%4
                self.leading_player = (teammate+3)%4
            self.stack = Stack()
        else:
            self.leading_player = player_id
            self.active_player = (player_id+1)%4
        # remove cards from player hand
        _ = self.players[player_id].remove_cards(cards)
        self.pass_counter = 0
        if self.verbose > 0:
            print('Player {0} plays {1}.'.format(
                    player_id, cards.type))
            cards.show()
        # check if player and game is finished
        if self.players[player_id].finished:
            points_this_step = self._player_finished_routine(player_id)
        return True, points_this_step

    def _player_finished_routine(self, player_id):
        """ Changes game state when player made finishing move. """
        dispatch_finish = {1: lambda *args: [0, 0, 0, 0],
                           2: self._check_double_victory,
                           3: self._regular_game_end}
        if self.verbose > 0:
            print(
              'Player {0} has finished on position {1}!'
              .format(player_id, len(self.players_finished)+1))
        self.players_finished.append(player_id)
        # check if any Tichu call was successfull or not
        tichu_points_this_step = self._check_tichu_success()
        # check if game is finished
        points_this_step = dispatch_finish[len(self.players_finished)](
                                                                    player_id)
        # aggregate points from game end and tichu
        total_points_this_step = [sum(x) for x in zip(points_this_step,
                                                      tichu_points_this_step)]
        if self.game_finished and self.verbose > 0:
            print('-----')
            print('Game is finished!')
            print('Score of player 0 and player 2: {0}'.format(
                (self.players[0].points+self.players[2].points)))
            print('Score of player 1 and player 3: {0}'.format(
                (self.players[1].points+self.players[3].points)))
        return total_points_this_step

    def _check_double_victory(self, player_id):
        """ Checks if it is a double victory if 2 players have finished. """
        points_this_step = [0, 0, 0, 0]
        if (len(self.players_finished) == 2 and
              sum(self.players_finished)%2 == 0):
            if self.verbose > 0:
                print(
                  'Double team victory by players {0} and {1}!'
                  .format(self.players_finished[0],
                          self.players_finished[1]))
            opponents = self._get_opponents()
            teammate = self._get_teammate()
            self.players[player_id].set_points(100)
            self.players[teammate].set_points(100)
            self.players[opponents[0]].set_points(0)
            self.players[opponents[1]].set_points(0)
            # Add individual Tichu points to player score
            self.players[player_id].add_points(self.tichu_points[player_id])
            self.players[teammate].add_points(self.tichu_points[teammate])
            # Set points this step to double victory points + tichu points
            tichu_points = (self.tichu_points[player_id]
                            + self.tichu_points[teammate])
            points_this_step[player_id] = 200 + tichu_points
            points_this_step[teammate] = 200 + tichu_points
            points_this_step[opponents[0]] = 0
            points_this_step[opponents[1]] = 0
            self.game_finished = True
        return points_this_step

    def _regular_game_end(self, *unused_args):
        """ Changes game state for a regular game end. """
        points_this_step = [0, 0, 0, 0]
        self.game_finished = True
        # if last stack is dragon stack
        if self.stack.dragon_flag:
            points_this_step = self._dragon_stack()
        # get first and last finisher
        first = self.players_finished[0]
        for i in range(4):
            if not self.players[i].finished:
                last = i
        # opponent team gets hand of last finisher
        hand_points_last = self.players[last].hand.points
        opponents = self._get_opponents(pid=last)
        self.players[opponents[0]].add_points(
                                     hand_points_last)
        points_this_step[opponents[0]] = hand_points_last
        # first finisher gets stack of last finisher
        stack_points_last = self.players[last].points
        self.players[first].add_points(stack_points_last)
        points_this_step[first] += stack_points_last
        self.players[last].set_points(0)
        points_this_step[last] = 0
        return points_this_step

    def _check_tichu_success(self):
        """ Checks whether a Tichu call was succesfull. """
        tichu_points_this_step = [0, 0, 0, 0]
        for i in range(4):
            if self.players[i].tichu_flag:
                # Tichu is successfull when Tichu caller finishes first
                if ((len(self.players_finished) == 1) and
                      self.players[i].finished):
                    self.players[i].add_points(100)
                    self.tichu_points[i] = 100
                    tichu_points_this_step[i] += 100
                    if self.verbose > 0:
                        print('Successfull Tichu by player {0}!'
                          .format(i))
                else:
                    self.players[i].add_points(-100)
                    self.tichu_points[i] = -100
                    tichu_points_this_step[i] -= 100
                    if self.verbose > 0:
                        print(
                          'Tichu by player {0} was not successfull!'
                          .format(i))
                # undo Tichu flag to avoids points are added more than once
                self.players[i].tichu_flag = False
        return tichu_points_this_step

    def _invalid_move_routine(self, player_id, *unused_args):
        points_this_step = [0, 0, 0, 0]
        if self.verbose > 1:
            print('Invalid move by player {0}'.format(player_id))
        return False, points_this_step

    def _dragon_stack(self):
        """
        Manages a Stack containing a Dragon Card by a simple heuristic.

        According to game rules, a stack with a Dragon must be given
        to a player of the opposing team.
        Here, this is determined automatically by a simple heuristic:
        - If any opponent player has called Tichu,
          give the Dragon stack to the other player
        - Else, give Dragon stack to the opponent with the most hand cards.
        This is reasonable, because the Dragon stack can be reobtained
        if opponent finishes last.
        """
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
        # no tichu called, stack goes to opponent with more hand cards
        elif (self.players[opponents[0]].hand_size <
              self.players[opponents[1]].hand_size):
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
