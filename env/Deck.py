# Deck class for Python Implementation of Tichu

import random

from env.Card import Card
from env.Cards import Cards

class Deck():

    def __init__(self):
        # instatiate all cards
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

        self.all_cards = [Spd_2 , Hrt_2 , Dia_2 , Clb_2 ,    
                          Spd_3 , Hrt_3 , Dia_3 , Clb_3 ,
                          Spd_4 , Hrt_4 , Dia_4 , Clb_4 ,
                          Spd_5 , Hrt_5 , Dia_5 , Clb_5 , 
                          Spd_6 , Hrt_6 , Dia_6 , Clb_6 , 
                          Spd_7 , Hrt_7 , Dia_7 , Clb_7 , 
                          Spd_8 , Hrt_8 , Dia_8 , Clb_8 ,
                          Spd_9 , Hrt_9 , Dia_9 , Clb_9 ,
                          Spd_10 , Hrt_10 , Dia_10 , Clb_10 ,
                          Spd_J , Hrt_J , Dia_J , Clb_J ,
                          Spd_Q , Hrt_Q , Dia_Q , Clb_Q ,
                          Spd_K , Hrt_K , Dia_K , Clb_K ,
                          Spd_A , Hrt_A , Dia_A , Clb_A,
                          Phoenix, Dragon, Majong, Dog]
        self.size = len(self.all_cards)

    def shuffle_and_deal(self):
        all_cards = self.all_cards
        random.shuffle(all_cards)
        chunk_size = int(self.size/4)
        set_0 = Cards(card_list=all_cards[0:chunk_size])
        set_1 = Cards(card_list=all_cards[chunk_size:2*chunk_size])
        set_2 = Cards(card_list=all_cards[2*chunk_size:3*chunk_size])
        set_3 = Cards(card_list=all_cards[3*chunk_size:])
        return set_0, set_1, set_2, set_3
       