Welcome to the Tichu Agent Project
==================================

Tichu is a card game where four players in two opposing teams try to win by accumulating as much points as possible.
The combination of collaborative and competitive aspects of the game makes it a challenging task for reinforcement learning (RL).

The goals of this project are:

* Implement an environment of Tichu that enables RL-methods,
* Make agents learn (and possibly master) the game using different RL-approaches,
* Let the agents compete against rule-based, non-AI agents and humans.

Usage
-----

It is recommended to clone the whole repository including the environment and all pre-trained agents.::

     !git clone https://github.com/alxwdm/tichuagent
    
If you want to train your own agents, you can create and interact with the environment this way::

     env = Env()
     state, rewards, done, active_player = env.reset()
     (...)
     state, rewards, done, active_player = env.step(active_player, action)

For a detailed description of the environment, see contents below.

Contents
========

.. toctree::
    :maxdepth: 2
    
    environment
    agents
