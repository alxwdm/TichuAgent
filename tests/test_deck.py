# pytest test cases for class Deck

import pytest

from env.deck import Deck

def test_deck():
    # test instantiating and dealing the deck
    deck = Deck()
    sets = deck.shuffle_and_deal()
    assert sets[0].size == 14
    assert sets[1].size == 14
    assert sets[2].size == 14
    assert sets[3].size == 14
