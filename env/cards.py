""" This module contains a class to represent multiple Tichu Cards. """

BOMBS = ['four_bomb', 'straight_bomb']

class Cards():
    """
    A class to represent multiple Tichu Cards.

    Can either be a hand (i.e. no specific combination)
    or a combination (e.g. pair, straight, ...).
    The type is determined automatically when adding or removing cards.

    Inspired by the following sources:
    - https://github.com/hundredblocks/ticher
    - https://github.com/sylee421/TichuRL

    Attributes
    ----------
    cards: list of Card
      A list containing all Card objects in this Cards instance.
    phoenix_flag: bool
      Whether this Cards instance contains a Phoenix.
    size: int
      The number of Cards in this instance.
    points: int
      The points of the card.
      In Tichu, only 5, 10, K, Phoenix and Dragon give points.
    type: str
      The type of this Cards instance (e.g. hand, pair, straight)
    power: float
      The power of this Cards instance. It depends on the type
      and the highest Card.
      For example: A hand has 0 power, a pair of 10s has power 10.
    points: int
      The aggregated Card points in this instance.

    Methods
    -------
    show:
      Prints all the Cards using the Card.image attribute.
    get_available_combinations:
      Outputs a list of all possible combinations.
    contains(other):
      Checks whether other (list of Card objects) are contained
      in this Cards instance.
    remove(card):
      Removes a Card from this Cards instance.
    """

    size = None
    cards = None
    phoenix_flag = None

    def __init__(self, card_list):
        """
        Constructs a Cards instance.

        Paramter
        --------
        card_list: A list of Card objects.
        """
        self.phoenix_flag = False
        self.cards = list()
        for i in card_list:
            self.cards.append(i)
            if i.name == 'Phoenix':
                self.phoenix_flag = True
        self.cards.sort()
        self.size = len(self.cards)
        self._set_type_and_power()
        self._set_points()

    def show(self):
        """ A nice visualization of all cards in the set. """
        if self.size == 0:
            print('  PASS')
        else:
            for i in range(5):
                for crd in range(self.size):
                    print(self.cards[crd].image[i], end='')
                print()

    def _set_points(self):
        """ Set number of game points of this card set. """
        if self.type != 'pass':
            self.points = sum([crd.points for crd in self.cards])
        else:
            self.points = 0

    def _set_type_and_power(self):
        """ Determines which combination (if any) is this card set. """
        card_set = self.cards
        card_set.sort()
        phoenix_flag = self.phoenix_flag
        self.type = 'unk'
        # pass
        if len(card_set)==0:
            self.type = 'pass'
            self.power = 0
            return
        # solo
        if len(card_set)==1:
            self.type = 'solo'
            self.power = card_set[0].power
            return
        # pair
        if len(card_set)==2:
            if card_set[0].power == card_set[1].power:
                self.type = 'pair'
                self.power = card_set[0].power
                return
            # phoenix pair
            elif (phoenix_flag and 
                  not (card_set[1].name == 'Dragon' or 
                       card_set[1].name == 'Dog')):
                self.type = 'pair'
                self.power = card_set[1].power
                return
        # triple
        if len(card_set)==3:
            if (card_set[0].power == card_set[1].power and
                card_set[1].power == card_set[2].power):
                self.type = 'triple'
                self.power = card_set[0].power
                return
            # phoenix triple
            elif phoenix_flag and card_set[1].power == card_set[2].power:
                self.type = 'triple'
                self.power = card_set[1].power
                return
        # four (BOMB)
        if (len(card_set)==4 and card_set[0].power == card_set[1].power and
            card_set[1].power == card_set[2].power and
            card_set[2].power == card_set[3].power):
            self.type = 'four_bomb'
            self.power = 50 + card_set[0].power
            return
        # full house
        if len(card_set)==5:
            if (card_set[0].power == card_set[1].power and
                  card_set[1].power == card_set[2].power and
                  card_set[3].power == card_set[4].power):
                self.type = 'full'
                self.power = card_set[0].power
                return
            elif (card_set[0].power == card_set[1].power and
                    card_set[2].power == card_set[3].power and
                    card_set[3].power == card_set[4].power):
                self.type = 'full'
                self.power = card_set[2].power
                return
            # phoenix full house with phoenix triple
            elif (phoenix_flag and
                    card_set[1].power == card_set[2].power and
                    card_set[3].power == card_set[4].power):
                self.type = 'full'
                self.power = card_set[3].power
                return
            # phoenix full house with phoenix pair
            elif phoenix_flag:
                if (card_set[1].power == card_set[2].power and
                      card_set[2].power == card_set[3].power):
                    self.type = 'full'
                    self.power = card_set[1].power
                    return
                elif (card_set[2].power == card_set[3].power and
                      card_set[3].power == card_set[4].power):
                    self.type = 'full'
                    self.power = card_set[2].power
                    return
        # straight and straight bomb
        if len(card_set)>=5:
            is_straight = True
            is_flush = True
            for i in range(len(card_set)-1):
                if card_set[i].power + 1 == card_set[i+1].power:
                    if card_set[i].suit == card_set[i+1].suit:
                        pass
                    else:
                        is_flush = False
                else:
                    is_straight = False
                    break
            if is_straight and is_flush:
                self.type = 'straight_bomb'
                self.power = 100 + card_set[-1].power
                return
            if is_straight:
                self.type = 'straight'
                self.power = card_set[-1].power
                return
            # phoenix straight
            if phoenix_flag:
                phoenix_used = False
                phoenix_idx = -1
                is_straight = True
                for i in range(len(card_set)-2):
                    if card_set[i+1].power+1 == card_set[i+2].power:
                        pass
                    elif (not(phoenix_used) and
                         (card_set[i+1].power+2 == card_set[i+2].power)):
                        phoenix_used = True
                        phoenix_idx = i+1
                    else:
                        is_straight = False
                if is_straight:
                    self.type = 'straight'
                    # phoenix is last card of straight
                    if not(phoenix_used) or (phoenix_idx == len(card_set)):
                        self.power = card_set[-1].power+1
                    else:
                        self.power = card_set[-1].power
                    return
        # pair sequence
        if (len(card_set)>=4 and len(card_set)%2==0 and
            not(any((crd.name == 'Dog' or crd.name == 'Dragon')
                for crd in card_set))):
            is_pair_regular = True
            for i in range(len(card_set)-1):
                if i%2 == 0 and card_set[i].power == card_set[i+1].power:
                    pass
                elif i%2 == 1 and card_set[i].power+1 == card_set[i+1].power:
                    pass
                else:
                    is_pair_regular = False
                    break
            if is_pair_regular:
                self.type = 'pair_seq'
                self.power = card_set[-1].power
                return
            # phoenix pair sequence (quite complicated to get all valid cases)
            if phoenix_flag:
                # first, check if it is an increasing by +1 sequence
                unique_power = sorted(set([crd.power for crd in card_set]))
                unique_power.pop(0) # remove phoenix
                if (all(x+1==y for x, y in zip(unique_power, unique_power[1:])
                      ) and len(unique_power)>1):
                    phoenix_used = False
                    is_pair_equal = True
                    is_pair_unequal = True
                    # check for phoenix use in 'unequal' index
                    toggle = 1
                    antitoggle = 0
                    for i in range(1,len(card_set)-1):
                        if (i%2 == toggle and
                              card_set[i].power == card_set[i+1].power):
                            pass
                        elif (i%2 == antitoggle and
                              card_set[i].power + 1 == card_set[i+1].power):
                            if i+1 >= len(card_set)-1 and not phoenix_used:
                                # phoenix used as the highest pair of sequence
                                phoenix_used = True
                        elif phoenix_used: # phoenix cannot be used twice
                            is_pair_unequal = False
                            break
                        else:
                            # phoenix is used in the middle of the sequence
                            # toggle 1 and 0 so that i%2 matches next element
                            phoenix_used = True
                            toggle = 0
                            antitoggle = 1
                    # check for phoenix use in 'equal' index
                    if not is_pair_unequal:
                        phoenix_used = False
                        for i in range(1,len(card_set)-1):
                            if (i%2 == 0 and
                                  card_set[i].power == card_set[i+1].power):
                                pass
                            elif (i%2 == 1 and
                                  card_set[i].power+1 == card_set[i+1].power):
                                # check if phoenix is first card in sequence
                                if i == 1:
                                    phoenix_used = True
                            elif phoenix_used: # phoenix cannot be used twice
                                is_pair_equal = False
                                break
                            else:
                                phoenix_used = True
                    if is_pair_unequal or is_pair_equal:
                        self.type = 'pair_seq'
                        self.power = card_set[-1].power
                        return
        # no combination must be a hand
        if self.type == 'unk':
            self.type = 'hand'
            self.power = 0

    def get_available_combinations(self):
        """ Get all available combinations form this card set. """
        all_cards = self.cards
        all_cards.sort()
        phoenix_flag = self.phoenix_flag

        solo = list()
        pair = list()
        triple = list()
        four_bomb = list()
        full = list()
        straight = list()
        straight_bomb = list()
        pair_seq = list()

        # solo
        for i in range(len(self.cards)):
            solo_list = all_cards[i]
            solo_cards = Cards([solo_list])
            if solo_cards.type == 'solo':
                solo.append(solo_cards)
        # pair
        for i in range(len(all_cards)-1):
            # regular pairs
            if all_cards[i].power == all_cards[i+1].power:
                pair_list = [all_cards[i], all_cards[i+1]]
                pair_cards = Cards(pair_list)
                if pair_cards.type == 'pair':
                    pair.append(pair_cards)
            # phoenix pairs
            if phoenix_flag and all_cards[i+1].suit != 'Special':
                pair_list = [all_cards[0], all_cards[i+1]]
                pair_cards = Cards(pair_list)
                if pair_cards.type == 'pair':
                    pair.append(pair_cards)
            # multiple pairs
            try:
                if all_cards[i].power == all_cards[i+2].power:
                    pair_list = [all_cards[i], all_cards[i+2]]
                    pair_cards = Cards(pair_list)
                    if pair_cards.type == 'pair':
                        pair.append(pair_cards)
                if all_cards[i].power == all_cards[i+3].power:
                    pair_list = [all_cards[i], all_cards[i+3]]
                    pair_cards = Cards(pair_list)
                    if pair_cards.type == 'pair':
                        pair.append(pair_cards)
            except:
                pass
        # triple
        for i in range(len(self.cards)-2):
            # regular triple
            if (all_cards[i].power == all_cards[i+1].power and
                all_cards[i+1].power == all_cards[i+2].power):
                triple_list = [all_cards[i], all_cards[i+1], all_cards[i+2]]
                triple_cards = Cards(triple_list)
                if triple_cards.type == 'triple':
                    triple.append(triple_cards)
            # phoenix triple
            if phoenix_flag and all_cards[i+1].power == all_cards[i+2].power:
                triple_list = [all_cards[0], all_cards[i+1], all_cards[i+2]]
                triple_cards = Cards(triple_list)
                if triple_cards.type == 'triple':
                    triple.append(triple_cards)
            # multiple triples
            try:
                if (all_cards[i].power == all_cards[i+1].power and
                      all_cards[i+1].power == all_cards[i+3].power):
                    triple_list = [all_cards[i], all_cards[i+1],
                                   all_cards[i+3]]
                    triple_cards = Cards(triple_list)
                    if triple_cards.type == 'triple':
                        triple.append(triple_cards)
                if (all_cards[i].power == all_cards[i+2].power and
                      all_cards[i+2].power == all_cards[i+3].power):
                    triple_list = [all_cards[i], all_cards[i+2],
                                   all_cards[i+3]]
                    triple_cards = Cards(triple_list)
                    if triple_cards.type == 'triple':
                        triple.append(triple_cards)
                if (phoenix_flag and
                      all_cards[i+1].power == all_cards[i+3].power):
                    triple_list = [all_cards[0], all_cards[i+1],
                                   all_cards[i+3]]
                    triple_cards = Cards(triple_list)
                    if triple_cards.type == 'triple':
                        triple.append(triple_cards)
                if (phoenix_flag and
                      all_cards[i+1].power == all_cards[i+4].power):
                    triple_list = [all_cards[0], all_cards[i+1],
                                   all_cards[i+4]]
                    triple_cards = Cards(triple_list)
                    if triple_cards.type == 'triple':
                        triple.append(triple_cards)
            except:
                pass
        # four
        for i in range(len(self.cards)-3):
            if (all_cards[i].power == all_cards[i+1].power and
                  all_cards[i+1].power == all_cards[i+2].power and
                  all_cards[i+2].power == all_cards[i+3].power):
                four_list = [all_cards[i], all_cards[i+1],
                             all_cards[i+2], all_cards[i+3]]
                four_cards = Cards(four_list)
                if four_cards.type == 'four_bomb':
                    four_bomb.append(four_cards)
        # full house
        for i in pair:
            for j in triple:
                if i.power != j.power:
                    full_list = list()
                    full_list.extend(i.cards)
                    full_list.extend(j.cards)
                    full_cards = Cards(full_list)
                    if full_cards.type == 'full':
                        full.append(full_cards)
        # straight and straight_bomb
        for i in range(len(self.cards)-4):
            candidate_list = list()
            phoenix_available = self.phoenix_flag
            for j in range(i,len(self.cards)):
                # add first card of possible straight
                if len(candidate_list)==0:
                    candidate_list.append(all_cards[j])
                    if all_cards[j].name == 'Phoenix':
                        phoenix_available = False
                # no check if Phoenix is last entry
                elif candidate_list[-1].name == 'Phoenix':
                    candidate_list.append(all_cards[j])
                    if len(candidate_list) > 4:
                        straight_cards = Cards(candidate_list)
                        if straight_cards.type == 'straight':
                            straight.append(straight_cards)
                        else:
                            pass
                # add subsequent cards
                elif candidate_list[-1].power+1 == all_cards[j].power:
                    candidate_list.append(all_cards[j])
                    if len(candidate_list) > 4:
                        straight_cards = Cards(candidate_list)
                        if straight_cards.type == 'straight':
                            straight.append(straight_cards)
                        elif straight_cards.type == 'straight_bomb':
                            straight_bomb.append(straight_cards)
                        else:
                            pass
                # skip pairs
                elif candidate_list[-1].power == all_cards[j].power:
                    pass
                # use phoenix mid straight if available
                elif (phoenix_available and 
                    candidate_list[-1].power+2 == all_cards[j].power):
                    candidate_list.append(all_cards[0])
                    candidate_list.append(all_cards[j])
                    if len(candidate_list) > 4:
                        straight_cards = Cards(candidate_list)
                        if straight_cards.type == 'straight':
                            straight.append(straight_cards)
                    phoenix_available = False
                # use phoenix as first/last card if available
                elif phoenix_available:
                    candidate_list.append(all_cards[0])
                    if len(candidate_list) > 4:
                        straight_cards = Cards(candidate_list)
                        if straight_cards.type == 'straight':
                            straight.append(straight_cards)
                    phoenix_available = False
                # no straight possible
                else:
                    break
        # pair_seq
        for i in range(len(pair)-1):
            candidate_list = list()
            for j in range(i,len(pair)):
                # add first element to candidate list
                if len(candidate_list) == 0:
                    candidate_list.extend([elem for elem in pair[j].cards])
                # add subsequent pairs
                elif candidate_list[-1].power+1 == pair[j].power:
                    candidate_list.extend([elem for elem in pair[j].cards])
                    if len(candidate_list) > 1:
                        pair_seq_cards = Cards(candidate_list)
                        if pair_seq_cards.type == 'pair_seq':
                            pair_seq.append(pair_seq_cards)
                # skip double pairs
                elif candidate_list[-1].power == pair[j].power:
                    pass
                # break if no pair_seq possible
                else:
                    break
        return [solo, pair, triple, four_bomb,
                full, straight, straight_bomb, pair_seq]

    def contains(self, other):
        """ Checks if this instance contains all cards from other. """
        this_cards = [(crd.name, crd.suit) for crd in self.cards]
        other_cards = [(crd.name, crd.suit) for crd in other.cards]
        return all([elem in this_cards for elem in other_cards])

    def remove(self, card):
        """ Remove a single Card and update this Cards instance. """
        try:
            self.cards.remove(card)
        except: # if card is not in cards, return False
            return False
        self.cards.sort()
        if card.name == 'Phoenix':
            self.phoenix_flag = False
        self.size = self.size - 1
        self._set_type_and_power()
        self._set_points()
        return True

    def __add__(self, card_list_to_add):
        this_card_list = self.cards
        this_card_list.append(card_list_to_add)
        new_cards = Cards(card_list=this_card_list)
        return new_cards

    def __sub__(self, cards):
        this_card_list = self.cards
        for crd in cards:
            this_card_list.remove(crd)
        new_cards = Cards(card_list=this_card_list)
        return new_cards

    def __ge__(self, other):
        # equal types or bombs, compare power
        if ((self.type == other.type and
            self.size == other.size) or
            self.type in BOMBS or
            other.type in BOMBS):
            return self.power >= other.power
        # unequal types, return False (opt: raise error)
        else:
            return False

    def __le__(self, other):
        # equal types or bombs, compare power
        if ((self.type == other.type and
            self.size == other.size) or
            self.type in BOMBS or
            other.type in BOMBS):
            return self.power <= other.power
        # unequal types, return False (opt: raise error)
        else:
            return False

    def __gt__(self, other):
        # equal types or bombs, compare power
        if ((self.type == other.type and
            self.size == other.size) or
            self.type in BOMBS or
            other.type in BOMBS):
            return self.power > other.power
        # unequal types, return False (opt: raise error)
        else:
            return False

    def __lt__(self, other):
        # equal types or bombs, compare power
        if ((self.type == other.type and
            self.size == other.size) or
            self.type in BOMBS or
            other.type in BOMBS):
            return self.power < other.power
        # unequal types, return False (opt: raise error)
        else:
            return False

    def __eq__(self, other):
        return (self.type == other.type and
                self.size == other.size and
                self.power == other.power)

    def __ne__(self, other):
        return (self.type != other.type and
                self.size != other.size and
                self.power != other.power)

    def __repr__(self):
        card_str = ''
        for crd in self.cards:
            card_str = card_str + str(crd.name) + ' ' + str(crd.suit) + ', '
        return str({'type': self.type,
                    'size': self.size,
                    'cards': card_str})
