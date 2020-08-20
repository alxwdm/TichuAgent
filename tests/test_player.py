# pytest test cases for class Player

import pytest

from env.cards import Cards

def test_id(player_0):
    assert player_0.id == 0

def test_assign(player_0, hand_0):
    assert player_0.assign_hand(hand_0) == True
    assert player_0.hand_power == 0

def test_move(player_0, hand_0):
    player_0.assign_hand(hand_0)
    comb = player_0.random_move()
    assert player_0.move(comb) == True
    assert player_0.remove_cards(comb) == True
    player_0.add_points(comb.points)
    assert player_0.points == comb.points

def test_points(player_0):
    player_0.set_points(100)
    assert player_0.points == 100

def test_tichu(player_0):
    assert player_0.call_tichu() == False

def test_finish(player_1, hand_1, Clb_J, Dia_J, Phoenix, Dog):
    player_1.assign_hand(hand_1) == True
    comb = Cards([Clb_J, Dia_J, Phoenix])
    assert player_1.move(comb) == True
    assert player_1.remove_cards(comb) == True
    comb = Cards([Dog])
    assert player_1.move(comb) == True
    assert player_1.remove_cards(comb) == True
    assert player_1.has_finished() == True
