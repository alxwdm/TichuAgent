# pytest test cases for class Stack

import pytest

from env.stack import Stack
from env.cards import Cards

def test_game_rules(solo_0, solo_1, solo_2, solo_3, pair_0, four_0):
    stack = Stack()
    assert stack.add(solo_1) == True
    assert stack.add(pair_0) == False
    assert stack.add(solo_0) == True
    assert stack.add(solo_1) == False
    assert stack.add(solo_3) == True
    assert stack.add(solo_0) == False
    assert stack.add(solo_2) == True
    assert stack.add(solo_3) == False
    assert stack.add(four_0) == True    

def test_complex_series(Phoenix, Spd_3, Hrt_3, Clb_3, 
                        Spd_4, Hrt_4, Clb_4, 
                        Clb_5, Hrt_5, Dia_5, Spd_5,
                        Spd_K, Hrt_K, Clb_K):
    stack = Stack()
    fh_0 = Cards([Spd_3, Hrt_3, Clb_3, Spd_K, Hrt_K])
    fh_1 = Cards([Spd_K, Hrt_K, Clb_K, Spd_3, Hrt_3])
    fh_2 = Cards([Spd_4, Hrt_4, Clb_4, Phoenix, Hrt_K])
    bomb_0 = Cards([Spd_5, Clb_5, Hrt_5, Dia_5])
    assert stack.add(fh_0) == True
    assert stack.power == 3
    assert stack.points == 20
    assert stack.type == 'full'
    assert stack.add(fh_2) == True
    assert stack.power == 4
    assert stack.points == 5
    assert stack.add(fh_1) == True
    assert stack.power == 13
    assert stack.points == 35
    assert stack.add(bomb_0) == True
    assert stack.power == 55
    assert stack.points == 55
    assert stack.type == 'four_bomb'
    assert stack.add(fh_0) == False    

def test_check_valid_move_0(full_0, four_0):
    assert Stack.check_valid_move(full_0, four_0) == True

def test_check_valid_move_1(full_1, full_0):
    assert Stack.check_valid_move(full_1, full_0) == False

def test_check_valid_move_2(full_0, four_0):
    assert Stack.check_valid_move(full_0, four_0) == True

def test_check_valid_move_3(solo_0, pair_1):
    assert Stack.check_valid_move(solo_0, pair_1) == False

def test_check_valid_move_4(strt_2, strt_1):
    assert Stack.check_valid_move(strt_2, strt_1) == True

def test_check_valid_move_5(strt_1, strt_0):
    assert Stack.check_valid_move(strt_1, strt_0) == False
