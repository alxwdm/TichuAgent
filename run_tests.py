# Test cases for Python Implementation of Tichu

# import all
from env.Card import Card
from env.Cards import Cards
from env.Deck import Deck
from env.Stack import Stack
from env.Player import Player
from env.Game import Game
from env.Env import Env

COMB_TYPES = {'solo': 0,
              'pair': 1,
              'triple': 2,
              'four_bomb': 3,
              'full': 4,
              'straight': 5,
              'straight_bomb': 6,
              'pair_seq': 7}

def play_dumb_game(max_steps=200):
    """
    This function plays a game with dumb heuristic players
    """
    game = Game(verbose=1)
    step_cnt = 0
    game_active = True
    while game_active:
        active_player = game.active_player
        leading_player = game.leading_player
        # make a random move if stack is empty
        if not(game.stack.cards) and not(game.players[active_player].has_finished()):
            comb = game.players[active_player].random_move()
            suc = game.step(active_player, comb)
        # try to make a matching move if opponent is leading
        elif ((active_player+leading_player)%2) !=0:
            leading_type = game.stack.type
            leading_idx = COMB_TYPES[leading_type]
            avail_comb = game.players[active_player].hand.get_available_combinations()
            # try to play, starting with lowest combination
            suc = False
            if avail_comb[leading_idx]:
                for i in range(len(avail_comb[leading_idx])):
                    suc = game.step(active_player, avail_comb[leading_idx][i])  
                if suc:
                    break
            # Try to bomb if no combination exists
            if not(suc) and avail_comb[COMB_TYPES['four_bomb']]:
                suc = game.step(active_player, avail_comb[COMB_TYPES['four_bomb']][0])
            elif not(suc) and avail_comb[COMB_TYPES['straight_bomb']]:
                suc = game.step(active_player, avail_comb[COMB_TYPES['straight_bomb']][0])
              # pass if nothing works
            elif not(suc):
                game.step(active_player, Cards([]))
        # pass if teammate is leading player
        else:
            game.step(active_player, Cards([]))
        # stop if game is finished (or counter overflow)
        step_cnt += 1
        if game.game_finished or step_cnt >= max_steps:
            game_active=False
            if step_cnt >= max_steps:
                print('max_steps exceeded, aborting game.')
            break


def run_tests():
    """
    This function runs tests for all classes.
    """

    # Test config
    TEST_CARD = True
    TEST_CARDS = True
    TEST_DECK = True
    TEST_STACK = True
    TEST_PLAYER = True
    TEST_GAME = True
    TEST_N_GAME = 1000
    TEST_ENV = False

    # instantiate all cards
    Spd_2 = Card(name='2', suit='Spade')
    Hrt_2 = Card(name='2', suit='Heart')
    Dia_2 = Card(name='2', suit='Dia')
    Clb_2 = Card(name='2', suit='Club')

    Spd_3 = Card(name='3', suit='Spade')
    Hrt_3 = Card(name='3', suit='Heart')
    Dia_3 = Card(name='3', suit='Dia')
    Clb_3 = Card(name='3', suit='Club')

    Spd_4 = Card(name='4', suit='Spade')
    Hrt_4 = Card(name='4', suit='Heart')
    Dia_4 = Card(name='4', suit='Dia')
    Clb_4 = Card(name='4', suit='Club')

    Spd_5 = Card(name='5', suit='Spade')
    Hrt_5 = Card(name='5', suit='Heart')
    Dia_5 = Card(name='5', suit='Dia')
    Clb_5 = Card(name='5', suit='Club')

    Spd_6 = Card(name='6', suit='Spade')
    Hrt_6 = Card(name='6', suit='Heart')
    Dia_6 = Card(name='6', suit='Dia')
    Clb_6 = Card(name='6', suit='Club')

    Spd_7 = Card(name='7', suit='Spade')
    Hrt_7 = Card(name='7', suit='Heart')
    Dia_7 = Card(name='7', suit='Dia')
    Clb_7 = Card(name='7', suit='Club')

    Spd_8 = Card(name='8', suit='Spade')
    Hrt_8 = Card(name='8', suit='Heart')
    Dia_8 = Card(name='8', suit='Dia')
    Clb_8 = Card(name='8', suit='Club')

    Spd_9 = Card(name='9', suit='Spade')
    Hrt_9 = Card(name='9', suit='Heart')
    Dia_9 = Card(name='9', suit='Dia')
    Clb_9 = Card(name='9', suit='Club')

    Spd_10 = Card(name='10', suit='Spade')
    Hrt_10 = Card(name='10', suit='Heart')
    Dia_10 = Card(name='10', suit='Dia')
    Clb_10 = Card(name='10', suit='Club')

    Spd_J = Card(name='J', suit='Spade')
    Hrt_J = Card(name='J', suit='Heart')
    Dia_J = Card(name='J', suit='Dia')
    Clb_J = Card(name='J', suit='Club')

    Spd_Q = Card(name='Q', suit='Spade')
    Hrt_Q = Card(name='Q', suit='Heart')
    Dia_Q = Card(name='Q', suit='Dia')
    Clb_Q = Card(name='Q', suit='Club')

    Spd_K = Card(name='K', suit='Spade')
    Hrt_K = Card(name='K', suit='Heart')
    Dia_K = Card(name='K', suit='Dia')
    Clb_K = Card(name='K', suit='Club')

    Spd_A = Card(name='A', suit='Spade')
    Hrt_A = Card(name='A', suit='Heart')
    Dia_A = Card(name='A', suit='Dia')
    Clb_A = Card(name='A', suit='Club')

    Majong = Card(name='Majong', suit='Special')
    Dragon = Card(name='Dragon', suit='Special')
    Phoenix = Card(name='Phoenix', suit='Special')
    Dog = Card(name='Dog', suit='Special')

    # instantiate some card sets
    hand_0 = Cards([Spd_10, Hrt_10, Dia_2, Phoenix, Dragon, Clb_K, Dia_J, Clb_J])
    hand_1 = Cards([Clb_J, Dia_J, Phoenix, Dog])
    hand_2 = Cards([Clb_J, Dia_J, Phoenix, Dragon])
    hand_3 = Cards([Clb_J, Clb_10, Spd_K, Hrt_K, Clb_Q, Dia_Q])
    hand_4 = Cards([Clb_2, Hrt_2, Spd_3, Phoenix, Clb_5, Dia_5, Clb_6, Dia_6])
    hand_5 = Cards([Clb_2, Phoenix, Spd_4, Clb_4])
    empty = Cards([])

    solo_0 = Cards([Spd_A])
    solo_1 = Cards([Hrt_5])
    solo_2 = Cards([Dragon])
    solo_3 = Cards([Phoenix])

    pair_0 = Cards([Spd_J, Dia_J])
    pair_1 = Cards([Spd_7, Phoenix])

    triple_0 = Cards([Spd_K, Hrt_K, Dia_K])
    triple_1 = Cards([Spd_3, Hrt_3, Phoenix])

    four_0 = Cards([Spd_10, Hrt_10, Dia_10, Clb_10]) # bomb
    four_1 = Cards([Spd_10, Hrt_10, Dia_10, Phoenix]) # no bomb

    fh_0 = Cards([Spd_3, Hrt_3, Clb_3, Spd_K, Hrt_K])
    fh_1 = Cards([Spd_K, Hrt_K, Phoenix, Spd_3, Hrt_3])
    fh_2 = Cards([Spd_4, Hrt_4, Clb_4, Phoenix, Hrt_K])

    strt_0 = Cards([Spd_3, Hrt_4, Clb_5, Spd_6, Hrt_7, Clb_8])
    strt_1 = Cards([Spd_3, Hrt_4, Clb_5, Phoenix, Hrt_7])
    strt_2 = Cards([Majong, Hrt_2, Clb_3, Phoenix, Hrt_4])
    strt_3 = Cards([Spd_5, Hrt_2, Clb_3, Phoenix, Hrt_4])
    strt_4 = Cards([Spd_5, Spd_6, Spd_7, Spd_8, Spd_9]) # straight bomb

    pair_seq_0 = Cards([Spd_J, Dia_J, Clb_Q, Dia_Q])
    pair_seq_1 = Cards([Spd_K, Phoenix, Clb_Q, Dia_Q])
    pair_seq_2 = Cards([Clb_J, Dia_J, Spd_K, Phoenix, Clb_K, Dia_Q])
    pair_seq_3 = Cards([Clb_J, Dia_J, Spd_K, Phoenix, Clb_Q, Dia_Q])
    pair_seq_4 = Cards([Clb_J, Phoenix, Spd_K, Hrt_K, Clb_Q, Dia_Q])


    # Class Card
    if TEST_CARD:
        print('Running tests for class Card ...')

        # Test logical operations
        assert (Spd_A > Hrt_10) == True 
        assert (Clb_J > Dia_K) == False
        assert (Clb_K >= Hrt_K) == True 
        assert (Dia_Q < Hrt_Q) == False
        assert (Hrt_2 <= Spd_2) == True 
        assert (Clb_2 == Spd_3) == False
        assert (Phoenix < Dragon) == True

        # Test game points of individual cards
        assert Spd_10.points == 10
        assert Dia_K.points == 10
        assert Hrt_5.points == 5
        assert Dragon.points == 25
        assert Phoenix.points == -25
        assert Clb_A.points == 0

        print('done!')

    if TEST_CARDS:
        print('Running tests for class Cards ...')

        # test card set types
        assert hand_0.type == 'hand'
        assert hand_1.type == 'hand'
        assert hand_2.type == 'hand'
        assert hand_3.type == 'hand'
        assert hand_4.type == 'hand'
        assert hand_5.type == 'hand'
        assert empty.type == 'pass'
        assert solo_0.type == 'solo'
        assert solo_1.type == 'solo'
        assert solo_2.type == 'solo'
        assert pair_0.type == 'pair'
        assert pair_1.type == 'pair'
        assert triple_0.type == 'triple'
        assert triple_1.type == 'triple'
        assert four_0.type == 'four_bomb'
        assert four_1.type == 'hand'
        assert fh_0.type == 'full'
        assert fh_1.type == 'full'
        assert fh_2.type == 'full'
        assert strt_0.type == 'straight'
        assert strt_1.type == 'straight'
        assert strt_2.type == 'straight'
        assert strt_3.type == 'straight'
        assert strt_4.type == 'straight_bomb'
        assert pair_seq_0.type == 'pair_seq'
        assert pair_seq_1.type == 'pair_seq'
        assert pair_seq_2.type == 'pair_seq'
        assert pair_seq_3.type == 'pair_seq'
        assert pair_seq_4.type == 'pair_seq'
        assert Cards([Dragon, Phoenix]).type != 'pair'
        assert Cards([Spd_A, Clb_K, Dia_J, Clb_Q, Dragon]).type != 'straight'

        # Test logical operations
        assert (solo_0 > solo_1) == True
        assert (solo_2 < solo_1) == False
        assert (solo_0 == solo_0) == True
        assert (solo_0 >= hand_0) == False
        assert (pair_0 >= pair_1) == True
        assert (pair_1 <= triple_0) == False
        assert (triple_1 <= triple_0) == True
        assert (four_0 < four_1) == False
        assert (strt_1 > strt_2) == True
        assert (strt_0 > strt_1) == False
        assert (strt_4 > strt_3) == True
        assert (strt_4 < four_1) == False
        assert (fh_0 <= fh_1) == True
        assert (pair_seq_0 == pair_seq_1) == False
        assert (pair_seq_2 == pair_seq_3) == True
        assert (pair_seq_0 <= pair_seq_4) == False

        # Test game points of cards
        assert hand_0.points == 30
        assert hand_1.points == -25
        assert hand_4.points == -15
        assert empty.points == 0
        assert solo_0.points == 0
        assert pair_0.points == 0
        assert triple_0.points == 30
        assert four_0.points == 40
        assert fh_1.points == -5
        assert strt_0.points == 5
        assert pair_seq_3.points == -15

        # Test removing cards from card set
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

        # Test other cards functions
        assert hand_0.contains(Cards([Spd_10, Hrt_10])) == True
        assert hand_0.contains(Cards([Spd_10, Hrt_2])) == False
        avail_combs = hand_0.get_available_combinations()
        assert len(avail_combs[0]) == 8
        assert len(avail_combs[1]) == 8
        assert len(avail_combs[2]) == 2
        assert len(avail_combs[3]) == 0
        assert len(avail_combs[4]) == 2
        assert len(avail_combs[5]) == 0
        assert len(avail_combs[6]) == 0
        assert len(avail_combs[7]) == 1

        print('done!')

    if TEST_DECK:
        print('Running tests for class Deck ...')

        # test instantiating and dealing the deck
        deck = Deck()
        sets = deck.shuffle_and_deal()
        assert len(sets[0]) == 14
        assert len(sets[1]) == 14
        assert len(sets[2]) == 14
        assert len(sets[3]) == 14

        print('done!')

    if TEST_STACK:
        print('Running tests for class Stack ...')

        # test adding cards to stack according to game rules
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

        # tests on class Stack with more complex card sets
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

        # test static check_valid_move fn
        assert Stack.check_valid_move(fh_0, bomb_0) == True
        assert Stack.check_valid_move(fh_1, fh_0) == False
        assert Stack.check_valid_move(fh_0, bomb_0) == True
        assert Stack.check_valid_move(solo_0, pair_1) == False
        assert Stack.check_valid_move(strt_2, strt_1) == True
        assert Stack.check_valid_move(strt_1, strt_0) == False

        print('done!')

    if TEST_PLAYER:
        print('Running tests for class Player ...')

        # try to play some hands with class Player
        hand_0 = Cards([Spd_10, Hrt_10, Dia_2, Phoenix, Dragon, Clb_K, Dia_J, Dia_J])
        hand_1 = Cards([Clb_J, Dia_J, Phoenix, Dog])

        player = Player(id=0)
        assert player.id == 0
        assert player.assign_hand(hand_0) == True
        assert player.hand_power == 0
        comb = player.random_move()
        assert player.move(comb) == True
        assert player.remove_cards(comb) == True
        player.add_points(comb.points)
        player.set_points(100)
        assert player.points == 100
        assert player.call_tichu() == False

        player = Player(id=1)
        player.assign_hand(hand_1) == True
        comb = Cards([Clb_J, Dia_J, Phoenix])
        assert player.move(comb) == True
        assert player.remove_cards(comb) == True
        comb = Cards([Dog])
        assert player.move(comb) == True
        assert player.remove_cards(comb) == True
        assert player.has_finished() == True

        print('done!')

    if TEST_GAME:
        print('Running tests for class Game with {0} random games ...'.format(
            TEST_N_GAME))

        # run x random games
        game_cnt = 0
        while game_cnt < TEST_N_GAME:
            play_dumb_game()
            game_cnt += 1

        print('done!')

# run as script
run_tests()