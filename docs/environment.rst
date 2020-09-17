Tichu Environment
=================

An RL Agent needs an environment to interact with in order to learn an optimal policy. State-of-the-art RL algorithms work as follows. The agent:
* observes the environment by looking at the **state**,
* chooses an **action** according to a policy,
* takes a **step** in the environment using the action,
* recieves a **reward** and
* learns from a (state, action, reward, next_state) **experience**.

The Tichu Environment is implemented in a way that satisfies these RL requirements. On a lower level, the Tichu game is designed independently of the RL setting in a straight forward, object orientated manner. The wrapper class ``env`` then converts the game instance into a format that enables RL (as described above). The design of the state, action and reward function needs to be considered throurougly, because the learning success massively depends on it.

Usage
-----

Use the environment to train and test an agent: ::

    env = Env()
    state, rewards, done, active_player = env.reset()
    (...) # let the agent choose an action according to its policy
    next_state, rewards, done, active_player = env.step(active_player, action)

You will recieve a nicely printed history of the game by setting the train_mode attribute to False. Please note that depending on the device, it may be necessary to change the image attribute of class ``Card`` to display the cards correctly (as you can see, the rst Code block does not look as nice as the Python console output). ::

    env = Env(train_mode=False)
    (...) # play a game
    Example output:
    Player 1 plays pair_seq.
    ┍┄┄┄┄┑  ┍┄┄┄┄┑  ┍┄┄┄┄┑ ┍┄┄┄┄┑
    ┆10   ┆ ┆10   ┆ ┆ J   ┆ ┆ J   ┆
    ┆  ♥  ┆ ┆  ⬧  ┆ ┆  ⬧  ┆ ┆  ♣  ┆
    ┆   10┆ ┆   10┆ ┆   J ┆ ┆   J ┆
    ┖┄┄┄┄┚  ┖┄┄┄┄┚ ┖┄┄┄┄┚  ┖┄┄┄┄┚
    Player 2 plays pair_seq.
    ┍┄┄┄┄┑  ┍┄┄┄┄┑  ┍┄┄┄┄┑ ┍┄┄┄┄┑
    ┆ Q   ┆ ┆ Q   ┆ ┆ K   ┆ ┆ K   ┆
    ┆  ♣  ┆ ┆  ♠  ┆ ┆  ⬧  ┆ ┆  ♣  ┆
    ┆   Q ┆ ┆   Q ┆ ┆   K ┆ ┆   K ┆
    ┖┄┄┄┄┚  ┖┄┄┄┄┚  ┖┄┄┄┚  ┖┄┄┄┄┚
    Player 3 passes.
    Player 0 passes.
    Player 1 passes,
    Player 2 has won the stack (20 points).
    Player 2 plays solo.
     ┍┄┄┄┄┑
    ┆ 2    ┆
    ┆  ♣   ┆
    ┆   2  ┆
     ┖┄┄┄┄┚
    (...)

State Design and Augmentation
-----------------------------

At the beginning and at each consecutive step, the environment outputs a state. The state needs to be designed in a way that:
* It covers all information about the game that is required to make an optimal decision about the next move.
* Does not include "illegal" information, e.g. the hand cards of the other players are not known to the agent.
* Has a limited but reasonable number of dimensions, because the larger the state size, the harder it is for an agent to learn.

In this particular case, the state depends on the point of view of the respective player. This means the environment outputs a list of four states from each players' perspective. Each (sub-)state must contain the hand cards of the player, obviously. Furthermore, the hand size of all four players is an important information in order to play successfully, and also which players (if any) have called Tichu. Finally, the last move of all players in the current stack is important to determine who is leading and which combination type and power needs to be beaten.

Considering all of the above, the state of ``player[i]`` looks as follows: ::

    [hand size, Tichu flag, hand cards*] of player i
    [hand size, Tichu flag, played cards*] of player i+1 (= left opponent)
    [hand size, Tichu flag, played cards*] of player i+2 (= vis-a-vis teammate)
    [hand size, Tichu flag, played cards*] of player i+3 (= right opponent)

    * Both the hand cards and played cards are represented as binary encodings of all 56 cards in a Tichu deck.

The way the state is designed allows the agent, in theory, to make a good decision on the next move, depending on questions such as:
* Who is leading the stack (teammate or opponent)?
* What is the leading combination and is my hand able to beat it?
* Is any player close to finishing the hand cards?
* Has anyone called Tichu (this strongly influences which decisions to take)

Two remarks are important regarding this state design:
1. A pro player would also count the cards that have already been played and consider this additional information in their move. For example, an Ace is the highest regular card but it can be beaten by the special card "Dragon". However, if the Dragon has already been played, it is safe to play a solo Ace to win a stack.
2. The suit of the card is, apart from the exceptional occurance of a straight-flush-bomb, not important.

The first remark implies that using the state as-is, it is not possible to determine the optimal decision. The second remark denotes that the suit of the card is only important in rare cases, thus the state may be simplified in order to enable a faster learning progress. Both assumptions are valid and by augmenting the state as a preprocessing step for the agent, they can be tackled. Preprocessing the state is completely okay if no illegal information are included. For example, you can preprocess the state before feeding it into the agent by summarizing all cards of the same suit but with different value. Then the cards will no longer be binary encoded, but the dimension size is reduced from 56 to 17 for each encoded card set.

Action Design and Augmentation
------------------------------

As the available cards of the raw state are binary encodings of all 56 cards in a Tichu deck, the action is likewise. For example: ::

    # Tichu deck representation:
    [2_Spades, 2_Heart, 2_Diamond, 2_Clubs, 3_Spades, 3_Heart, 3_Diamond, 3_Clubs, ..., Phoenix, Dragon, Majong, Dog]
    # Encoding of a pair of 2s:
    action = [1, 1, 0, 0, ..., 0]
    # Encoding of a Phoenix played as solo card:
    action = [0, 0, ..., 1, 0, 0, 0]
    # Encoding of an invalid combination (2, 2, 3):
    action = [1, 1, 0, 0, 1, 0, 0, 0, ..., 0]

Therefore, the action size is 56. This way however, a lot of learning is required for an agent to take actions with valid combinations. In order to enable faster learning, it is okay to simplify or augment the action, e.g. by ignoring the suit of the card.

Reward Design and Options
-------------------------

Probably the most critical part for the success of reinforcement learning is the reward design. RL agents are surprisingly good at hacking the reward function, i.e. learning a policy that yields great rewards but does not behave in an "optimal" oder "desired" way. There are endless examples of this on the internet, for example robots comitting "suicide" instead of walking through a parkour, because determining the episode as soon as poassible leads to a low negative reward, while failing to walk through the parkour without colliding would lead to an even higher negative reward.

Also, the way the actions and rewards are linked influences the performance. Consider two actions for a certain state. One action is like picking low hangig fruits, the reward is small but instantly recieved. The other action is a genius and bold move that leads to winning the game ten steps after. Hopefully, this example makes it clear how difficult learning to play a game can be and how essential the design of the reward function is.

In the particular case of Tichu, the reward setting can either be ``rich`` or ``sparse``. With ``rich`` rewards, it is possible to gain a reward after each step (of all four consecutive players). If the current stack is still active, the reward will be zero. If the stack is won by either player, the team that has made the trick recieves a reward in the amount of points included in this stack. The opposing team gets the exact same reward, but negative. Please note that in Tichu, only few cards give points and the Phoenix gives negative points. This way, it is possible to win a stack without recieving any points (and thus reward) or even with negative points. It is still beneficial to win stacks in order to finish as soon as possible.

With a ``sparse`` reward setting, a reward is only achieved at the end of the game. The winning team (by points or double-victor) will recieve the respective positive reward, the loosing team the negative reward. Successfull or failed Tichu calls are also included. 

While sparse rewards exactly match the points recieved by playing an episode of Tichu, rich rewards are recieved more frequently and thus lead to faster learning. However, both reward styles will penalize illegal moves so that the agent learns which card combinations are valid and which are not. The illegal move penalty may be set during the instantiation of an environment by setting the respective attribute, e.g. ``Env(illegal_move_penalty=-100)``. If the illegal move penalty is set to low, than the agent will not learn the game rules efficiently. On the other hand, if it is set to high, then the agent will learn that passing (i.e. playing no cards at all) is the best strategy because passing is almost always a valid move (remember the robot example).
