# pytest test cases for class Game

import pytest

from utils import play_dumb_game

TEST_N_GAME = 1000

@pytest.mark.timeout(TEST_N_GAME) # more than 2s per game is unusual
def test_game():
    """
    Testing all possible combinations of Cards is unfeasable.
    instead, test the Game by running TEST_N_GAME games
    using a certain policy (here: "dumb / random").
    Timeout marker is used to detect infinity loops.
    More than 1s per game is unusual.
    """
    game_cnt = 0
    while game_cnt < TEST_N_GAME:
        play_dumb_game(verbose=0)
        game_cnt += 1
