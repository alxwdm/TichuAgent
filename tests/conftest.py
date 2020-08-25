# pytest test cases configuration file

import pytest

from env.card import Card
from env.cards import Cards
from env.player import Player

# define pytest fixtures

# class Card test fixtures

# 2
@pytest.fixture(scope='session', autouse='True')
def Spd_2():
    return Card(name='2', suit='Spade')

@pytest.fixture(scope='session', autouse='True')
def Hrt_2():
    return Card(name='2', suit='Heart')

@pytest.fixture(scope='session', autouse='True')
def Dia_2():
    return Card(name='2', suit='Dia')

@pytest.fixture(scope='session', autouse='True')
def Clb_2():
    return Card(name='2', suit='Club')

#3
@pytest.fixture(scope='session', autouse='True')
def Spd_3():
    return Card(name='3', suit='Spade')

@pytest.fixture(scope='session', autouse='True')
def Hrt_3():
    return Card(name='3', suit='Heart')

@pytest.fixture(scope='session', autouse='True')
def Dia_3():
    return Card(name='3', suit='Dia')

@pytest.fixture(scope='session', autouse='True')
def Clb_3():
    return Card(name='3', suit='Club')

# 4
@pytest.fixture(scope='session', autouse='True')
def Spd_4():
    return Card(name='4', suit='Spade')

@pytest.fixture(scope='session', autouse='True')
def Hrt_4():
    return Card(name='4', suit='Heart')

@pytest.fixture(scope='session', autouse='True')
def Dia_4():
    return Card(name='4', suit='Dia')

@pytest.fixture(scope='session', autouse='True')
def Clb_4():
    return Card(name='4', suit='Club')

# 5
@pytest.fixture(scope='session', autouse='True')
def Spd_5():
    return Card(name='5', suit='Spade')

@pytest.fixture(scope='session', autouse='True')
def Hrt_5():
    return Card(name='5', suit='Heart')

@pytest.fixture(scope='session', autouse='True')
def Dia_5():
    return Card(name='5', suit='Dia')

@pytest.fixture(scope='session', autouse='True')
def Clb_5():
    return Card(name='5', suit='Club')

# 6
@pytest.fixture(scope='session', autouse='True')
def Spd_6():
    return Card(name='6', suit='Spade')

@pytest.fixture(scope='session', autouse='True')
def Hrt_6():
    return Card(name='6', suit='Heart')

@pytest.fixture(scope='session', autouse='True')
def Dia_6():
    return Card(name='6', suit='Dia')

@pytest.fixture(scope='session', autouse='True')
def Clb_6():
    return Card(name='6', suit='Club')

# 7
@pytest.fixture(scope='session', autouse='True')
def Spd_7():
    return Card(name='7', suit='Spade')

@pytest.fixture(scope='session', autouse='True')
def Hrt_7():
    return Card(name='7', suit='Heart')

@pytest.fixture(scope='session', autouse='True')
def Dia_7():
    return Card(name='7', suit='Dia')

@pytest.fixture(scope='session', autouse='True')
def Clb_7():
    return Card(name='7', suit='Club')

# 8
@pytest.fixture(scope='session', autouse='True')
def Spd_8():
    return Card(name='8', suit='Spade')

@pytest.fixture(scope='session', autouse='True')
def Hrt_8():
    return Card(name='8', suit='Heart')

@pytest.fixture(scope='session', autouse='True')
def Dia_8():
    return Card(name='8', suit='Dia')

@pytest.fixture(scope='session', autouse='True')
def Clb_8():
    return Card(name='8', suit='Club')

# 9
@pytest.fixture(scope='session', autouse='True')
def Spd_9():
    return Card(name='9', suit='Spade')

@pytest.fixture(scope='session', autouse='True')
def Hrt_9():
    return Card(name='9', suit='Heart')

@pytest.fixture(scope='session', autouse='True')
def Dia_9():
    return Card(name='9', suit='Dia')

@pytest.fixture(scope='session', autouse='True')
def Clb_9():
    return Card(name='9', suit='Club')

# 10
@pytest.fixture(scope='session', autouse='True')
def Spd_10():
    return Card(name='10', suit='Spade')

@pytest.fixture(scope='session', autouse='True')
def Hrt_10():
    return Card(name='10', suit='Heart')

@pytest.fixture(scope='session', autouse='True')
def Dia_10():
    return Card(name='10', suit='Dia')

@pytest.fixture(scope='session', autouse='True')
def Clb_10():
    return Card(name='10', suit='Club')

# J
@pytest.fixture(scope='session', autouse='True')
def Spd_J():
    return Card(name='J', suit='Spade')

@pytest.fixture(scope='session', autouse='True')
def Hrt_J():
    return Card(name='J', suit='Heart')

@pytest.fixture(scope='session', autouse='True')
def Dia_J():
    return Card(name='J', suit='Dia')

@pytest.fixture(scope='session', autouse='True')
def Clb_J():
    return Card(name='J', suit='Club')

# Q
@pytest.fixture(scope='session', autouse='True')
def Spd_Q():
    return Card(name='Q', suit='Spade')

@pytest.fixture(scope='session', autouse='True')
def Hrt_Q():
    return Card(name='Q', suit='Heart')

@pytest.fixture(scope='session', autouse='True')
def Dia_Q():
    return Card(name='Q', suit='Dia')

@pytest.fixture(scope='session', autouse='True')
def Clb_Q():
    return Card(name='Q', suit='Club')

# K
@pytest.fixture(scope='session', autouse='True')
def Spd_K():
    return Card(name='K', suit='Spade')

@pytest.fixture(scope='session', autouse='True')
def Hrt_K():
    return Card(name='K', suit='Heart')

@pytest.fixture(scope='session', autouse='True')
def Dia_K():
    return Card(name='K', suit='Dia')

@pytest.fixture(scope='session', autouse='True')
def Clb_K():
    return Card(name='K', suit='Club')

# A
@pytest.fixture(scope='session', autouse='True')
def Spd_A():
    return Card(name='A', suit='Spade')

@pytest.fixture(scope='session', autouse='True')
def Hrt_A():
    return Card(name='A', suit='Heart')

@pytest.fixture(scope='session', autouse='True')
def Dia_A():
    return Card(name='A', suit='Dia')

@pytest.fixture(scope='session', autouse='True')
def Clb_A():
    return Card(name='A', suit='Club')

# Special
@pytest.fixture(scope='session', autouse='True')
def Majong():
    return Card(name='Majong', suit='Special')

@pytest.fixture(scope='session', autouse='True')
def Dog():
    return Card(name='Dog', suit='Special')

@pytest.fixture(scope='session', autouse='True')
def Phoenix():
    return Card(name='Phoenix', suit='Special')

@pytest.fixture(scope='session', autouse='True')
def Dragon():
    return Card(name='Dragon', suit='Special')

# class Cards test fixtures

@pytest.fixture(scope='session', autouse='True')
def hand_0(Spd_10, Hrt_10, Dia_2, Phoenix, Dragon, Clb_K, Dia_J, Clb_J):
    return Cards([Spd_10, Hrt_10, Dia_2, Phoenix, Dragon, Clb_K, Dia_J, Clb_J])

@pytest.fixture(scope='session', autouse='True')
def hand_1(Clb_J, Dia_J, Phoenix, Dog):
    return Cards([Clb_J, Dia_J, Phoenix, Dog])

@pytest.fixture(scope='session', autouse='True')
def hand_2(Clb_J, Dia_J, Phoenix, Dragon):
    return Cards([Clb_J, Dia_J, Phoenix, Dragon])

@pytest.fixture(scope='session', autouse='True')
def hand_3(Clb_J, Clb_10, Spd_K, Hrt_K, Clb_Q, Dia_Q):
    return Cards([Clb_J, Clb_10, Spd_K, Hrt_K, Clb_Q, Dia_Q])

@pytest.fixture(scope='session', autouse='True')
def hand_4(Clb_2, Hrt_2, Spd_3, Phoenix, Clb_5, Dia_5, Clb_6, Dia_6):
    return Cards([Clb_2, Hrt_2, Spd_3, Phoenix, Clb_5, Dia_5, Clb_6, Dia_6])

@pytest.fixture(scope='session', autouse='True')
def hand_5(Clb_2, Phoenix, Spd_4, Clb_4):
    return Cards([Clb_2, Phoenix, Spd_4, Clb_4])

@pytest.fixture(scope='session', autouse='True')
def hand_6(Majong, Dog, Clb_2, Clb_3, Hrt_4, Phoenix, Dragon, Spd_K, Dia_K, Hrt_K, Clb_A, Hrt_A):
    return Cards([Majong, Dog, Clb_2, Clb_3, Hrt_4, Phoenix, Dragon, Spd_K, Dia_K, Hrt_K, Clb_A, Hrt_A])

@pytest.fixture(scope='session', autouse='True')
def pass_0():
    return Cards([])

@pytest.fixture(scope='session', autouse='True')
def solo_0(Spd_A):
    return Cards([Spd_A])

@pytest.fixture(scope='session', autouse='True')
def solo_1(Hrt_5):
    return Cards([Hrt_5])

@pytest.fixture(scope='session', autouse='True')
def solo_2(Dragon):
    return Cards([Dragon])

@pytest.fixture(scope='session', autouse='True')
def solo_3(Phoenix):
    return Cards([Phoenix])

@pytest.fixture(scope='session', autouse='True')
def pair_0(Spd_J, Dia_J):
    return Cards([Spd_J, Dia_J])

@pytest.fixture(scope='session', autouse='True')
def pair_1(Spd_7, Phoenix):
    return Cards([Spd_7, Phoenix])

@pytest.fixture(scope='session', autouse='True')
def pair_2(Dragon, Phoenix):
    return Cards([Dragon, Phoenix]) # no pair

@pytest.fixture(scope='session', autouse='True')
def triple_0(Spd_K, Hrt_K, Dia_K):
    return Cards([Spd_K, Hrt_K, Dia_K])

@pytest.fixture(scope='session', autouse='True')
def triple_1(Spd_3, Hrt_3, Phoenix):
    return Cards([Spd_3, Hrt_3, Phoenix])

@pytest.fixture(scope='session', autouse='True')
def four_0(Spd_10, Hrt_10, Dia_10, Clb_10):
    return Cards([Spd_10, Hrt_10, Dia_10, Clb_10]) # bomb

@pytest.fixture(scope='session', autouse='True')
def four_1(Spd_10, Hrt_10, Dia_10, Phoenix):
    return Cards([Spd_10, Hrt_10, Dia_10, Phoenix]) # no bomb

@pytest.fixture(scope='session', autouse='True')
def full_0(Spd_3, Hrt_3, Clb_3, Spd_K, Hrt_K):
    return Cards([Spd_3, Hrt_3, Clb_3, Spd_K, Hrt_K])

@pytest.fixture(scope='session', autouse='True')
def full_1(Spd_K, Hrt_K, Phoenix, Spd_3, Hrt_3):
    return Cards([Spd_K, Hrt_K, Phoenix, Spd_3, Hrt_3])

@pytest.fixture(scope='session', autouse='True')
def full_2(Spd_4, Hrt_4, Clb_4, Phoenix, Hrt_K):
    return Cards([Spd_4, Hrt_4, Clb_4, Phoenix, Hrt_K])

@pytest.fixture(scope='session', autouse='True')
def strt_0(Spd_3, Hrt_4, Clb_5, Spd_6, Hrt_7, Clb_8):
    return Cards([Spd_3, Hrt_4, Clb_5, Spd_6, Hrt_7, Clb_8])

@pytest.fixture(scope='session', autouse='True')
def strt_1(Spd_3, Hrt_4, Clb_5, Phoenix, Hrt_7):
    return Cards([Spd_3, Hrt_4, Clb_5, Phoenix, Hrt_7])

@pytest.fixture(scope='session', autouse='True')
def strt_2(Majong, Hrt_2, Clb_3, Phoenix, Hrt_4):
    return Cards([Majong, Hrt_2, Clb_3, Phoenix, Hrt_4])

@pytest.fixture(scope='session', autouse='True')
def strt_3(Spd_5, Hrt_2, Clb_3, Phoenix, Hrt_4):
    return Cards([Spd_5, Hrt_2, Clb_3, Phoenix, Hrt_4])

@pytest.fixture(scope='session', autouse='True')
def strt_4(Spd_5, Spd_6, Spd_7, Spd_8, Spd_9):
    return Cards([Spd_5, Spd_6, Spd_7, Spd_8, Spd_9]) # straight bomb

@pytest.fixture(scope='session', autouse='True')
def strt_5(Spd_5, Hrt_2, Clb_6, Phoenix, Hrt_7):
    return Cards([Spd_5, Hrt_2, Clb_6, Phoenix, Hrt_7]) # hand (no straight)

@pytest.fixture(scope='session', autouse='True')
def strt_6(Spd_A, Clb_K, Dia_J, Clb_Q, Dragon):
    return Cards([Spd_A, Clb_K, Dia_J, Clb_Q, Dragon]) # hand (no straight)

@pytest.fixture(scope='session', autouse='True')
def strt_7(Majong, Hrt_2, Clb_3, Clb_5, Hrt_4):
    return Cards([Majong, Hrt_2, Clb_3, Clb_5, Hrt_4])

@pytest.fixture(scope='session', autouse='True')
def ps_0(Spd_J, Dia_J, Clb_Q, Dia_Q):
    return Cards([Spd_J, Dia_J, Clb_Q, Dia_Q])

@pytest.fixture(scope='session', autouse='True')
def ps_1(Spd_K, Phoenix, Clb_Q, Dia_Q):
    return Cards([Spd_K, Phoenix, Clb_Q, Dia_Q])

@pytest.fixture(scope='session', autouse='True')
def ps_2(Clb_J, Dia_J, Spd_K, Phoenix, Clb_K, Dia_Q):
    return Cards([Clb_J, Dia_J, Spd_K, Phoenix, Clb_K, Dia_Q])

@pytest.fixture(scope='session', autouse='True')
def ps_3(Clb_J, Dia_J, Spd_K, Phoenix, Clb_Q, Dia_Q):
    return Cards([Clb_J, Dia_J, Spd_K, Phoenix, Clb_Q, Dia_Q])

@pytest.fixture(scope='session', autouse='True')
def ps_4(Clb_J, Phoenix, Spd_K, Hrt_K, Clb_Q, Dia_Q):
    return Cards([Clb_J, Phoenix, Spd_K, Hrt_K, Clb_Q, Dia_Q])

@pytest.fixture(scope='session', autouse='True')
def ps_5(Clb_2, Phoenix, Spd_2, Hrt_4):
    return Cards([Clb_2, Phoenix, Spd_2, Hrt_4])

# class Player fixtures

@pytest.fixture(scope='session', autouse='True')
def player_0():
    return Player()

@pytest.fixture(scope='session', autouse='True')
def player_1():
    return Player()
