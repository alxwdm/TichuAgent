# Env class for Python Implementation of Tichu
# A wrapper for Game class to enable reinforcement learning

from env.Cards import Cards
from env.Game import Game

class Env():

    def __init__(self):
        # TODO
        return

    def step(self, player_id, actions):
        # TODO
        return [next_state, reward, done]

    def reset(self):
        # TODO
        return [next_state, reward, done]

    def vector_action_space(self):
        # TODO
        return vector_action_space

    def vector_state_space(self):
        # TODO
        return vector_state_space

    def _game_to_env_state(self):
        # TODO
        return state

    def _env_to_game_state(self):
        # TODO
        return state

    def _game_to_env_action(self, cards):
        # TODO
        return action

    def _env_to_game_action(self, action):
        # TODO
        return cards

    def _get_rewards_from_game(self):
        # TODO
        return reward
