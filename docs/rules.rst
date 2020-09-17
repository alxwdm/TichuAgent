Game Rules
===========

This section contains a short description of the rules of the game of Tichu. It is a a card game where four players in two opposing teams try to win by accumulating as much points as possible. 

(Note: "They" is used as a gender-neutral pronoun troughout this text.)

Players, Cards and Points
-------------------------

From one players' perspective, the vis-à-vis player is the teammate, the left and right players are opponents.

At the beginning, each player recieves 14 hand cards from a Tichu deck with 56 cards in total. There are 52 regular cards in a range from 2 to Ace with the suits Spade ``♠``, Heart ``♥``, Diamond ``⬧`` and Club ``♣`` (originally called differently) and 4 special cards ``Phoenix``, ``Dragon``, ``Majong (= 1)`` and ``Dog``. The points of the cards are as follows: Cards with value 5 give 5 points, values 10 and K give 10 points, Dragon gives +25 points and Phoenix -25 points. All other cards give 0 points.

The player who owns the Majong starts. Afterwards, each player is in turn in counter-clockwise direction.

Stacks and Combinations
-----------------------

The cards are played as combinations upon a stack. Valid combinations are: solo, pair, triple, four, full house, straight, straigh flush and pair sequence. Initially, any valid combination may be played on an empty stack.

The rule in order to play a combination upon a stack is simple. It must be the same type but higher power. For example, a pair of 4 can be played on top of a pair of 2, but not on top of a pair of 10 or on top of a straight. A straight consists of five cards at least, with no maximum. Only straights of equal lengths can be played upon each other. Pair sequences are pairs in an increasing order, such as pair of 2 and pair of 3. Again, only equal length but higher power pair sequences can be played upon a stack. Four and straight flus are so called ``bombs``, they can be played anytime and on any combination. A straight flush is a higher powered bomb than a four type bomb.

At any step, a player is allowed to pass if they can not or do not want to play a valid combination upon a stack. If three consecutive players pass, then the stack is finished, i.e. the trick (and its points) goes to the player that has played the highest combination on the stack (i.e. the stack leading player). The leading player is also allowed to start the next stack, therefore determining the type of combination for the next round.

Special Cards and Tichu Call
----------------------------

The special card ``Dragon`` is the highest available card, but can only be played as a solo type combination. A stack containing the Dragon (and therefore all of its points) must be given away by the stack winner to an opponent.

The ``Phoeonix`` serves as a joker in any combination except solo and bomb types. Played as a solo card, the power of the Phoenix is always half a point above the power of the current stack card (except for the Dragon). For example, Phoenix on top of a 10 has power 10.5. A Phoenix on top of an Ace can only be beaten by the ``Dragon``.

The ``Majong`` has card value 1. It is used to determine the starting player. The card can either be played as solo, or in a straight.

The ``Dog`` can only be played at the begining of a stack. When played, the next opponent is skipped and the teammate is the next active player.

At any time during the game, a player is allowed to call ``Tichu`` if they has not played any cards yet. Calling Tichu is like betting to finish first. If the Tichu caller does so, 100 additional points are rewarded at the end of the game. Likewise, -100 points are added to the total score if the Tichu call was not successful. If a player has called Tichu, then the goal of the opposing team is to destroy the Tichu at any cost while the teammate will support the Tichu caller by any means. Thus, the strategy shifts from being "total points orientated" to "supporting or destroying Tichu".

End of Game
-----------

There are two possible ways to end the game. A regular game ends when only one player remains with hand cards. Then, the first finisher recieves all the points from the stacks that the last player has won. The remaining hand cards of the last player go to the opposite team. Then, the points of the two teammates are added and the winning team is determined. In the case that two players of one team finish first and second, it is called a "double victory". Then, the points achieved during the game are ignored. Instead, the double victory team recieves 200 points. Points from Tichu calls are considered in both cases. Usually, the points of single games are added up to a total score of 1000.

Deviations for this project
---------------------------

Some of the rules have been slightly modified for this project. In a regular game, each player must give away one hand card to all other players after the cards have been dealed. Plus, the player who has the Majong may make a card wish after the Majong has been played. For example, the player may wish for an "Ace of Spades". If the player that owns this card is able to make a valid move containing this card, they must play it. These rules has been left out.

Additionally, calling Tichu is not an action a player can take actively. Instead, it is determined by the game itself using a hand rating for each player. The hand rating is based on a simple scoring heuristic. If the rating exceeds a threshold, the player calls Tichu if the teammate has not already done so. Similarily, the Dragon stack will be given away based on a simple heuristic. It is given to the opponent player with the highest hand card count, except they has called Tichu. This is because the last finisher will give its poinst to the first finisher and the opponent with a higher amount of cards is less likely to finish, except the hand is very powerfull. This way, the point of the Dragon can be recovered. Both rules are modified to decrease the complexity of actions an agent needs to take. It only needs to concentrate on playing cards upon a stack, not giving them away or calling Tichu.
