"""
A Tichu Environment for Reinforcement Learning

Tichu is a card game where four players in two opposing teams try to win
by accumulating as much points as possible.

The rules of the game can be briefly described as follows: *
At the beginning, each player gets 14 hand cards from the deck.
The cards are played as combinations (such as high card, pair, triple,
full house, straight, etc.) upon a stack. Any valid combination may be
played upon an empty stack, but the following players must either play
the same type of combination with higher power upon the stack, or pass.
If all other players can not or do not want to play a higher combination
upon a stack, the stack (and all including points) goes to the player 
that has played the highest combination so far and the stack is emptied.
The game ends when only one player is remaining or the two teammates
have finished first and second, respectively (i.e. a "double victory").
The last player looses all points by giving their stacks to the first
finisher (who may be their teammate) and the remaining hand cards to the
opposing team.
Only few cards give points, namely: 5's give 5 points, 10's and Kings 
give 10 points. There are four special cards, two of which are the 
Dragon (who gives +25 points, but the stack must be given to a player of
the opposing team) and the Phoenx (-25 points, but serves as a joker).
In case of a double victory, the winning team gets 200 points. In case
of a regular game end, the stack points of either team are added in
order to determine the winner. 
Usually, the points are accumulated until 1000 total points are reached.
A player can call "Tichu" if they has not played any hand cards yet. In
doing so, they announces to finish first. A succesfull Tichu is worth
100 additional points, but yields the danger of loosing 100 points if 
the player who made the Tichu call does not finish first.

This Python implementation of Tichu is wrapped into an environment that
brings the game into a format that enables Reinforcement Learning, i.e.
a game move (= an action) yields a new state in a vectorized form from
the perspective of the player that made the action and also a reward.

The package contains the following modules:
- Card: A single card having a value, suit and power.
- Cards: Multiple cards, that can be a hand or combination of any type.
- Stack: Adds combinations according to the game rules.
- Deck: Contains all cards in a Tichu deck and serves as a dealer.
- Player: Has hand cards, points, can call Tichu and make a move.
- Game: A class for managing a Tichu game.
- Env: A wrapper for Tichu Game class to enable Reinforcement Learning.

* "they" is used throughout as gender-neutral singular pronoun.
"""