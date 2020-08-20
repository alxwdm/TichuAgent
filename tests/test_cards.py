# pytest test cases for class Cards

import pytest
from env.cards import Cards

# test card set types

def test_type_h0(hand_0):
    assert hand_0.type == 'hand'

def test_type_h1(hand_1):
    assert hand_1.type == 'hand'

def test_type_h2(hand_2):
    assert hand_2.type == 'hand'

def test_type_h3(hand_3):
    assert hand_3.type == 'hand'

def test_type_h4(hand_4):
    assert hand_4.type == 'hand'

def test_type_h5(hand_5):
    assert hand_5.type == 'hand'

def test_type_e0(pass_0):
    assert pass_0.type == 'pass'

def test_type_s0(solo_0):
    assert solo_0.type == 'solo'

def test_type_s1(solo_1):
    assert solo_1.type == 'solo'

def test_type_s2(solo_2):
    assert solo_2.type == 'solo'

def test_type_s3(solo_3):
    assert solo_3.type == 'solo'

def test_type_p0(pair_0):
    assert pair_0.type == 'pair'

def test_type_p1(pair_1):
    assert pair_1.type == 'pair'

def test_type_p2(pair_2):
    assert pair_2.type != 'pair'

def test_type_t0(triple_0):
    assert triple_0.type == 'triple'

def test_type_t1(triple_1):
    assert triple_1.type == 'triple'

def test_type_fb0(four_0):
    assert four_0.type == 'four_bomb'

def test_type_fb1(four_1):
    assert four_1.type != 'four_bomb'

def test_type_fh0(full_0):
    assert full_0.type == 'full'

def test_type_fh1(full_1):
    assert full_1.type == 'full'

def test_type_fh2(full_2):
    assert full_2.type == 'full'

def test_type_strt0(strt_0):
    assert strt_0.type == 'straight'

def test_type_strt1(strt_1):
    assert strt_1.type == 'straight'

def test_type_strt2(strt_2):
    assert strt_2.type == 'straight'

def test_type_strt3(strt_3):
    assert strt_3.type == 'straight'

def test_type_strt4(strt_4):
    assert strt_4.type == 'straight_bomb'

def test_type_strt5(strt_5):
    assert strt_5.type != 'straight'

def test_type_strt6(strt_6):
    assert strt_6.type != 'straight'

def test_type_ps0(ps_0):
    assert ps_0.type == 'pair_seq'

def test_type_ps1(ps_1):
    assert ps_1.type == 'pair_seq'

def test_type_ps2(ps_2):
    assert ps_2.type == 'pair_seq'

def test_type_ps3(ps_3):
    assert ps_3.type == 'pair_seq'

def test_type_ps4(ps_4):
    assert ps_4.type == 'pair_seq'

def test_type_ps5(ps_5):
    assert ps_5.type != 'pair_seq'

# test logical operations

def test_logical_0(solo_0, solo_1):
    assert (solo_0 > solo_1) == True

def test_logical_1(solo_2, solo_1):
    assert (solo_2 < solo_1) == False

def test_logical_2(solo_0):
    assert (solo_0 == solo_0) == True

def test_logical_3(solo_0, hand_0):
    assert (solo_0 >= hand_0) == False

def test_logical_4(pair_0, pair_1):
    assert (pair_0 >= pair_1) == True

def test_logical_5(pair_1, triple_0):
    assert (pair_1 <= triple_0) == False

def test_logical_6(triple_1, triple_0):
    assert (triple_1 <= triple_0) == True

def test_logical_7(four_0, four_1):
    assert (four_0 < four_1) == False

def test_logical_8(strt_1, strt_2):
    assert (strt_1 > strt_2) == True

def test_logical_9(strt_0, strt_1):
    assert (strt_0 > strt_1) == False

def test_logical_10(strt_4, strt_3):
    assert (strt_4 > strt_3) == True

def test_logical_11(strt_4, four_1):
    assert (strt_4 < four_1) == False

def test_logical_12(full_0, full_1):
    assert (full_0 <= full_1) == True

def test_logical_13(ps_0, ps_1):
    assert (ps_0 == ps_1) == False

def test_logical_14(ps_2, ps_3):
    assert (ps_2 == ps_3) == True

def test_logical_15(ps_0, ps_4):
    assert (ps_0 <= ps_4) == False

# test game points of cards

def test_points_0(hand_0):
     assert hand_0.points == 30

def test_points_1(hand_1):
     assert hand_1.points == -25

def test_points_2(hand_4):
     assert hand_4.points == -15

def test_points_3(pass_0):
     assert pass_0.points == 0

def test_points_4(solo_0):
     assert solo_0.points == 0

def test_points_5(pair_0):
     assert pair_0.points == 0

def test_points_6(triple_0):
     assert triple_0.points == 30

def test_points_7(four_0):
     assert four_0.points == 40

def test_points_8(full_1):
     assert full_1.points == -5

def test_points_9(strt_0):
     assert strt_0.points == 5

def test_points_10(ps_3):
     assert ps_3.points == -15

# test removing cards from set

def test_remove_0(Spd_10, Hrt_10, Phoenix, Dragon):
    remove_0 = Cards([Spd_10, Hrt_10, Phoenix, Dragon])
    assert remove_0.type == 'hand'
    assert remove_0.size == 4
    assert remove_0.power == 0
    assert remove_0.remove(Dragon) == True
    assert remove_0.type == 'triple'
    assert remove_0.size == 3
    assert remove_0.power == 10
    assert remove_0.remove(Phoenix) == True
    assert remove_0.type == 'pair'
    assert remove_0.size == 2
    assert remove_0.power == 10
    assert remove_0.remove(Phoenix) == False

# test other cards functions

def test_contains_0(hand_0, Spd_10, Hrt_10):
    assert hand_0.contains(Cards([Spd_10, Hrt_10])) == True

def test_contains_1(hand_0, Spd_10, Hrt_2):
    assert hand_0.contains(Cards([Spd_10, Hrt_2])) == False

def test_avail_comb_0(hand_0):
    avail_combs = hand_0.get_available_combinations()
    assert len(avail_combs[0]) == 8
    assert len(avail_combs[1]) == 8
    assert len(avail_combs[2]) == 2
    assert len(avail_combs[3]) == 0
    assert len(avail_combs[4]) == 2
    assert len(avail_combs[5]) == 0
    assert len(avail_combs[6]) == 0
    assert len(avail_combs[7]) == 1
