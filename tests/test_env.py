# pytest test cases for class Env

import pytest
import numpy as np

from env.env import Env
from utils import play_greedy_game

TEST_N_ENV = 1000

def test_env_state():
    env = Env()
    state, _, _, _ = env.reset()
    assert np.shape(state) == (4, 4, 3)
    for i in range(4):
        assert sum(state[i][0][2]) == 14

@pytest.mark.timeout(TEST_N_ENV)  
def test_env():
    """
    Testing all possible combinations of Cards is unfeasable.
    instead, test the environment by running TEST_N_ENV games
    using a certain policy (here: greedyAgent).
    Timeout marker is used to detect infinity loops.
    More than 1s per game is unusual.
    """
    game_cnt = 0
    while game_cnt < TEST_N_ENV:
        play_greedy_game(verbose=False)
        game_cnt += 1
