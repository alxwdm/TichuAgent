# pytest test cases for class Card

import pytest

# test logical operators

def test_logical_eq(Spd_2, Hrt_2):
    assert (Spd_2 == Hrt_2) == True

def test_logical_ge(Dia_2, Clb_2):
    assert (Dia_2 >= Clb_2) == True

def test_logical_gt(Spd_A, Hrt_10):
    assert (Spd_A > Hrt_10) == True 

def test_logical_le(Clb_K, Hrt_K):
    assert (Clb_K <= Hrt_K) == True 

def test_logical_lt(Dia_Q, Hrt_Q):
    assert (Dia_Q < Hrt_Q) == False

def test_logical_ne(Clb_2, Spd_3):
    assert (Clb_2 != Spd_3) == True

def test_logical_s0(Phoenix, Dragon):
    assert (Phoenix < Dragon) == True

def test_logical_s1(Hrt_A, Dragon):
    assert (Hrt_A > Dragon) == False

# test game points

def test_points_0(Spd_2, Hrt_3, Clb_4, Dia_5, Spd_J, Dia_Q, Clb_A):
    assert Spd_2.points == 0
    assert Hrt_3.points == 0
    assert Clb_4.points == 0
    assert Spd_J.points == 0
    assert Dia_Q.points == 0
    assert Clb_A.points == 0

def test_points_K(Spd_K, Clb_K, Hrt_K, Dia_K):
    assert Spd_K.points == 10
    assert Clb_K.points == 10
    assert Hrt_K.points == 10
    assert Dia_K.points == 10

def test_points_5(Spd_5, Clb_5, Hrt_5, Dia_5):
    assert Spd_5.points == 5
    assert Clb_5.points == 5
    assert Hrt_5.points == 5
    assert Dia_5.points == 5

def test_points_10(Spd_10, Clb_10, Hrt_10, Dia_10):
    assert Spd_10.points == 10
    assert Clb_10.points == 10
    assert Hrt_10.points == 10
    assert Dia_10.points == 10

def test_points_Special(Phoenix, Dragon, Majong, Dog):
    assert Phoenix.points == -25
    assert Dragon.points == 25
    assert Majong.points == 0
    assert Dog.points == 0
