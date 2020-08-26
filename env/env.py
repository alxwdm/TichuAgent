from itertools import compress

import numpy as np

from env.cards import Cards
from env.deck import Deck
from env.game import Game

ILLEGAL_MOVE_PENALTY = -10
REWARD_STYLE  = 'rich'

class Env():
    """
    A wrapper for Tichu Game class to enable Reinforcement Learning.

    Brings a Tichu Game instance in a shape where an (RL-)Agent can:
      1. Observe a state.
      2. Take an action.
      3. Recieve a reward.

    The state consists of infos from a Players perspective:
    [Players' hand size, Tichu Flag, Players' hand cards]
    [Opponent 1 hand size, Tichu Flag, Opponent 1 last move]
    [Teammate hand size, Tichu Flag, Teammates last move]
    [Opponent 2 hand size, Tichu Flag, Opponent 2 last move]
    The Cards are one-hot-encoded (OHE), e.g.:
    [1, 0, 0, ... 0, 0] is a OHE representation of 2 of Spades.
    There are alternative possibilites for the state-design which
    may be included in the future.

    The action is also a OHE of Cards, e.g.:
    [1, 0, 0, 0, 1, 0, ... 0] means play a pair of 2s.

    The reward function is designed two ways:

    Rich rewards means that a reward can be recieved after each step.
    A step is considered a move by all 4 players.
    In a rich reward setting, the reward is equal to the points
    in a Stack if the Stack is won by either the Player or its teammate.
    The same reward, but negative, is given to the opposing team.
    For Example:
    Player 0 wins a Stack containing 20 points.
    The rewards will be [20, -20, 20, -20] until the next step.

    Sparse rewards means that the rewards are only different from 0
    when a game has finished. In this case, the rewards exactly match
    the outcome of a Game.
    For Example:
    Team 0 has achieved 60 points, Team 1 has achieved 40 points.
    Player 0 has successfully called Tichu (+100 points.
    The rewards will be [160, -60, 160, -60].

    For both reward styles, an invalid move by a Player leads to an
    immediate negative reward.

    Attributes
    ----------
    dispatch_reward: dictionary
      This is to set the reward function (rich/sparse.
    train_mode: bool
      Sets the verbosity of the Game.
    state_size: int
      The size of the state dimension.
    action_size: int
      The size of the action dimension.
    all_cards: list of Card
      A list containing instances of all Cards in a Tichu Deck.
    game: Game
      A Tichu Game instance.
    action_buffer: list of int
      A list containing the last actions of all Players.
    states: list of int
      A list of the states from all Players' perspectives.
    rewards: list of int
      The rewards that an Agent will recieved after a step.
    done: bool
      Whether the episode (i.e. Game) is finished.
    nstep: int
      An internal step conter used for rich rewards.

    Methods
    -------
    reset():
      Instantiates a new Game and resets state, action, rewards, done.

    step(player_id, action):
      Takes a step in the Game and updates state, action, rewards, done.
    """

    def __init__(self, train_mode=True):
        """
        Constructs a Tichu Environment for RL.

        Parameter
        ---------
        train_mode: If false, verbosity of Game will be set to 1.
        """
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
        self.game = None
        self.action_buffer = [[None], [None], [None], [None]]
        self.state = [[None], [None], [None], [None]]
        self.rewards = [None, None, None, None]
        self.done = False
        self.nstep = 0 # only relevant for rich rewards
        self.pass_counter = 0 # only relevant for debugging

    def reset(self):
        """ Resets the Environment. """
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
        """
        Takes a step in the Game.
        Updates state, action, rewards, done and returns them.

        Paramter
        --------
        player_id: The id (0...3) of the player that makes a move.
        action: The action of the player as OHE Cards representation.
        """
        # convert action vector and make game step
        cards = self._vec_to_cards(action)
        suc, points_this_step = self.game.step(player_id, cards)
        # illegal move
        if not suc:
            self.rewards[player_id] = ILLEGAL_MOVE_PENALTY
        # legal move
        else:
            self._update_action_buffer(player_id, action)
            self._update_all_states()
            # reset state and action buffer if stack has been emptied
            # and update rewards according to points in the stack
            if not self.game.stack.cards:
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
        Resets the state to the initial setting.

        Initial game state of player i:
        i:     [hand_size, tichu_flag, hand_cards (OHE)]
        i + 1: [hand_size, tichu_flag, played_cards (OHE)]
        i + 2: [hand_size, tichu_flag, played_cards (OHE)]
        i + 3: [hand_size, tichu_flag, played_cards (OHE)]
        """
        self.state = list()
        for i in range(4):
            this_player = i
            player_state = list()
            for j in range(4):
                pid = (this_player + j)%4
                hand_size = self.game.players[pid].hand_size
                tichu_flag = int(self.game.players[pid].tichu_flag)
                if pid == this_player:
                    player_cards = self._cards_to_vec(
                        self.game.players[pid].hand)
                else:
                    player_cards = np.zeros(len(self.all_cards), int).tolist()
                player_state.append([hand_size, tichu_flag, player_cards])
            self.state.append(player_state)

    def _update_all_states(self):
        """ Updates states with latest action taken by other players. """
        self.state = list()
        for i in range(4):
            this_player = i
            player_state = list()
            for j in range(4):
                pid = (this_player + j)%4
                hand_size = self.game.players[pid].hand_size
                tichu_flag = int(self.game.players[pid].tichu_flag)
                if pid == this_player:
                    player_cards = self._cards_to_vec(
                        self.game.players[pid].hand)
                else:
                    player_cards = self.action_buffer[pid]
                player_state.append([hand_size, tichu_flag, player_cards])
            self.state.append(player_state)

    def _reset_action_buffer(self):
        """ Resets the action buffer. """
        for i in range(4):
            self.action_buffer[i] = np.zeros(len(self.all_cards),int).tolist()

    def _update_action_buffer(self, player_id, action):
        """ Updates the action buffer. """
        self.action_buffer[player_id] = action

    def _reset_rewards(self):
        """ Resets the rewards to 0. """
        self.rewards = [0, 0, 0, 0]
        self.nstep = self.game.active_player

    def _update_rewards(self, points_this_step):
        """ Updates the rewards according to reward style. """
        self.dispatch_reward[REWARD_STYLE](points_this_step)

    def _update_rich_rewards(self, points_this_step):
        """
        Updates the rewards according to a rich reward function.

        This implemenation of a reward function promises rewards after
        each round (i.e. consecutive steps of all 4 players).
        If a player or its teammate (!) gets points during a round
        (e.g. by winning a stack), it gets a reward in the amount of
        the points in this round.
        The benefit of this reward function is that each step promises a
        reward (i.e. no sparse rewards that may impede learning).
        The danger is that the actual points are assigned at the end of a
        game, which means the last player looses all its points to the
        first finisher.
        This may lead to a non-ideal game strategy, where lots of
        rewards might be collected during the game, but actually the game is
        lost if the player does not finish early.
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

    def _update_sparse_rewards(self, points_this_step):
        """
        Updates the rewards according to a sparse reward function.

        Sparse rewards means that rewards are only achived when
        a Game is completed.
        The benefit is that the rewards exactly represent the outcome
        of the Game.
        The danger is that it is hard for an Agent to make sense
        of its actions when the rewards come only at the end
        of an episode.

        The sparse rewards are not yet implemented!
        """
        raise NotImplementedError("TODO")

    def _cards_to_vec(self, cards):
        """ Turns a Cards instance into a vector representation. """
        vec = np.zeros(len(self.all_cards), int)
        for i in range(len(self.all_cards)):
            crd = Cards([self.all_cards[i]])
            if cards.contains(crd):
                vec[i] = 1
        return vec.tolist()

    def _vec_to_cards(self, vec):
        """ Turns a vector representation into a Cards instance. """
        return Cards(list(compress(self.all_cards, vec)))
