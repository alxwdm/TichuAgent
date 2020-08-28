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
        # dispatch table for type checking function
        self.dispatch_type = {0: self._typecheck_pass,
                              1: self._typecheck_solo,
                              2: self._typecheck_pair,
                              3: self._typecheck_triple,
                              4: self._typecheck_four_bomb,
                              5: self._typecheck_full_straight,
                              6: self._typecheck_pair_seq}
        # set attributes
        self.phoenix_flag = False
        self.cards = list()
        for i in card_list:
            self.cards.append(i)
            if i.name == 'Phoenix':
                self.phoenix_flag = True
        self.cards.sort()
        self.size = len(self.cards)
        self.type = None
        self.power = 0
        # run init functions
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
        self.type = 'unk'
        # check for all but pair sequence depending on card length
        self.dispatch_type[min(len(self.cards),5)]()
        # if type is still unkown, check for pair sequence
        if self.type == 'unk':
            self.dispatch_type[6]()
        # if type is still unkown, it must be a hand
        if self.type == 'unk':
            self.type = 'hand'
            self.power = 0

    def get_available_combinations(self):
        """ Get all available combinations form this card set. """
        solo = self._get_available_solo()
        pair = self._get_available_pair()
        triple = self._get_available_triple()
        four_bomb = self._get_available_four_bomb()
        full = self._get_available_full()
        straight, straight_bomb = self._get_available_straight()
        pair_seq = self._get_available_pair_seq()
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
        except ValueError: # if card is not in cards, return False
            return False
        self.cards.sort()
        if card.name == 'Phoenix':
            self.phoenix_flag = False
        self.size = self.size - 1
        self._set_type_and_power()
        self._set_points()
        return True

    def _typecheck_pass(self):
        """ Checks whether Cards is of type pass. """
        if len(self.cards)==0:
            self.type = 'pass'
            self.power = 0

    def _typecheck_solo(self):
        """ Checks whether Cards is of type solo. """
        if len(self.cards)==1:
            self.type = 'solo'
            self.power = self.cards[0].power

    def _typecheck_pair(self):
        """ Checks whether Cards is of type pair. """
        if len(self.cards)==2:
            # regular pair
            if self.cards[0].power == self.cards[1].power:
                self.type = 'pair'
                self.power = self.cards[0].power
                return
            # phoenix pair
            elif (self.phoenix_flag and
                  not (self.cards[1].name == 'Dragon' or
                       self.cards[1].name == 'Dog')):
                self.type = 'pair'
                self.power = self.cards[1].power

    def _typecheck_triple(self):
        """ Checks whether Cards is of type triple. """
        if len(self.cards)==3:
            # regular triple
            if (self.cards[0].power == self.cards[1].power and
                  self.cards[1].power == self.cards[2].power):
                self.type = 'triple'
                self.power = self.cards[0].power
            # phoenix triple
            elif self.phoenix_flag and self.cards[1].power == self.cards[2].power:
                self.type = 'triple'
                self.power = self.cards[1].power

    def _typecheck_four_bomb(self):
        """ Checks whether Cards is of type four bomb. """
        if (len(self.cards)==4 and self.cards[0].power == self.cards[1].power and
              self.cards[1].power == self.cards[2].power and
              self.cards[2].power == self.cards[3].power):
            self.type = 'four_bomb'
            self.power = 50 + self.cards[0].power

    def _typecheck_full_straight(self):
        """ Checks whether Cards is of type full house or straight. """
        self._typecheck_full()
        self._typecheck_straight()

    def _typecheck_full(self):
        """ Checks whether Cards is of type full house. """
        if len(self.cards)==5:
            # regular full house with triple higher than pair
            if (self.cards[0].power == self.cards[1].power and
                  self.cards[1].power == self.cards[2].power and
                  self.cards[3].power == self.cards[4].power):
                self.type = 'full'
                self.power = self.cards[0].power
            # regular full house with pair higher than triple
            elif (self.cards[0].power == self.cards[1].power and
                  self.cards[2].power == self.cards[3].power and
                  self.cards[3].power == self.cards[4].power):
                self.type = 'full'
                self.power = self.cards[2].power
            # phoenix full house with phoenix triple
            elif (self.phoenix_flag and
                  self.cards[1].power == self.cards[2].power and
                  self.cards[3].power == self.cards[4].power):
                self.type = 'full'
                self.power = self.cards[3].power
            # phoenix full house with phoenix pair
            elif self.phoenix_flag:
                if (self.cards[1].power == self.cards[2].power and
                      self.cards[2].power == self.cards[3].power):
                    self.type = 'full'
                    self.power = self.cards[1].power
                elif (self.cards[2].power == self.cards[3].power and
                      self.cards[3].power == self.cards[4].power):
                    self.type = 'full'
                    self.power = self.cards[2].power

    def _typecheck_straight(self):
        """
        Checks whether Cards is of type straight.

        Can be a straight with regular cards, straight with Phoenix,
        or straight bomb.
        """
        self._typecheck_regular_straight()
        self._typecheck_phoenix_straight()

    def _typecheck_regular_straight(self):
        """ Checks whether Cards is of type straight (w/o Phoenix). """
        if len(self.cards)>=5:
            is_straight = True
            is_flush = True
            for i in range(len(self.cards)-1):
                if self.cards[i].power + 1 == self.cards[i+1].power:
                    if self.cards[i].suit == self.cards[i+1].suit:
                        pass
                    else:
                        is_flush = False
                else:
                    is_straight = False
                    break
            # if it is a straight and all suits are equal, it is a bomb
            if is_straight and is_flush:
                self.type = 'straight_bomb'
                self.power = 100 + self.cards[-1].power
                return
            if is_straight:
                self.type = 'straight'
                self.power = self.cards[-1].power

    def _typecheck_phoenix_straight(self):
        """ Checks whether Cards is of type straight (with Phoenix). """
        if len(self.cards)>=5 and self.phoenix_flag:
            phoenix_used = False
            phoenix_idx = -1
            is_straight = True
            for i in range(len(self.cards)-2):
                if self.cards[i+1].power+1 == self.cards[i+2].power:
                    pass
                elif (not(phoenix_used) and
                     (self.cards[i+1].power+2 == self.cards[i+2].power)):
                    phoenix_used = True
                    phoenix_idx = i+1
                else:
                    is_straight = False
            if is_straight:
                self.type = 'straight'
                # phoenix is last card of straight: power is last card + 1
                if not(phoenix_used) or (phoenix_idx == len(self.cards)):
                    self.power = self.cards[-1].power+1
                # phoenix is not last card of straight: power is last card
                else:
                    self.power = self.cards[-1].power

    def _typecheck_pair_seq(self):
        """ Checks whether Cards is of type pair sequence. """
        self._typecheck_regular_pair_seq()
        self._typecheck_phoenix_pair_seq()


    def _typecheck_regular_pair_seq(self):
        """ Checks whether Cards is of type pair_seq (w/o Phoenix). """
        if (len(self.cards)>=4 and len(self.cards)%2==0 and
              not(any((crd.name == 'Dog' or crd.name == 'Dragon')
              for crd in self.cards))):
            is_pair_regular = True
            for i in range(len(self.cards)-1):
                if i%2 == 0 and self.cards[i].power == self.cards[i+1].power:
                    pass
                elif i%2 == 1 and self.cards[i].power+1 == self.cards[i+1].power:
                    pass
                else:
                    is_pair_regular = False
                    break
            if is_pair_regular:
                self.type = 'pair_seq'
                self.power = self.cards[-1].power

    def _typecheck_phoenix_pair_seq(self):
        """
        Checks whether Cards is of type pair_seq (with Phoenix).

        For a phoenix pair sequence, the algorithm is quite complicated,
        because there are a lot of possible combinations.
        Phoenix can be used in the first pair, in any middle pair, or in
        the last pair.
        Depending on where the Phoenix is used, either all equal or all
        unequal indices are increments of 1 in a valid pair sequence.
        If the Phoenix is used as a replacement for an equal indexed card,
        then the logic turns around ("toggles") and all subsequent cards
        need to be increments of the previous card in unequal indices.
        """
        # return if pair sequence is not possible
        if not (len(self.cards)>=4 and len(self.cards)%2==0 and
              not(any((crd.name == 'Dog' or crd.name == 'Dragon')
              for crd in self.cards)) and
              self.phoenix_flag):
            return
        # return if card sequence (excluding Phoenix) does not increase by 1
        unique_power = sorted({crd.power for crd in self.cards})
        unique_power.pop(0) # remove phoenix from set
        if not (all(x+1==y for x, y in zip(unique_power, unique_power[1:])
              ) and len(unique_power)>1):
            return
        # continue and prepare local variables if preconditions are met
        phoenix_used = False
        is_pair_equal = True
        is_pair_unequal = True
        # check for phoenix use in equal card list index
        toggle = 1
        antitoggle = 0
        for i in range(1,len(self.cards)-1):
            if (i%2 == toggle and
                  self.cards[i].power == self.cards[i+1].power):
                pass
            elif (i%2 == antitoggle and
                  self.cards[i].power + 1 == self.cards[i+1].power):
                if i+1 >= len(self.cards)-1 and not phoenix_used:
                    # phoenix used as the highest pair of sequence
                    phoenix_used = True
            elif phoenix_used: # phoenix cannot be used twice
                is_pair_unequal = False
                break
            else:
                # if phoenix is used in the middle of the sequence,
                # change matching behavior of toggle/antitoggle
                # so that i%2 matches next element
                phoenix_used = True
                toggle = 0
                antitoggle = 1
        # check for phoenix use in equal card list index
        if not is_pair_unequal:
            phoenix_used = False
            for i in range(1,len(self.cards)-1):
                if (i%2 == 0 and
                      self.cards[i].power == self.cards[i+1].power):
                    pass
                elif (i%2 == 1 and
                      self.cards[i].power+1 == self.cards[i+1].power):
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
            self.power = self.cards[-1].power

    def _get_available_solo(self):
        """ Returns a list with all possible solo combinations. """
        solo = list()
        for i in range(len(self.cards)):
            solo_list = self.cards[i]
            solo_cards = Cards([solo_list])
            if solo_cards.type == 'solo':
                solo.append(solo_cards)
        return solo

    def _get_available_pair(self):
        """ Returns a list with all possible pair combinations. """
        pair = list()
        for i in range(len(self.cards)-1):
            # regular pairs
            if self.cards[i].power == self.cards[i+1].power:
                pair_list = [self.cards[i], self.cards[i+1]]
                pair_cards = Cards(pair_list)
                if pair_cards.type == 'pair':
                    pair.append(pair_cards)
            # phoenix pairs
            if self.phoenix_flag and self.cards[i+1].suit != 'Special':
                pair_list = [self.cards[0], self.cards[i+1]]
                pair_cards = Cards(pair_list)
                if pair_cards.type == 'pair':
                    pair.append(pair_cards)
            # multiple pairs
            try:
                if self.cards[i].power == self.cards[i+2].power:
                    pair_list = [self.cards[i], self.cards[i+2]]
                    pair_cards = Cards(pair_list)
                    if pair_cards.type == 'pair':
                        pair.append(pair_cards)
                if self.cards[i].power == self.cards[i+3].power:
                    pair_list = [self.cards[i], self.cards[i+3]]
                    pair_cards = Cards(pair_list)
                    if pair_cards.type == 'pair':
                        pair.append(pair_cards)
            except IndexError:
                pass
        return pair

    def _get_available_triple(self):
        """ Returns a list with all possible triple combinations. """
        def check_and_append_triple(cards_list, triple):
            triple_cards = Cards(cards_list)
            if triple_cards.type == 'triple':
                triple.append(triple_cards)
            return triple
        triple = list()
        for i in range(len(self.cards)-2):
            # regular triple
            if (self.cards[i].power == self.cards[i+1].power and
                self.cards[i+1].power == self.cards[i+2].power):
                triple_candidate = [self.cards[i], self.cards[i+1],
                                    self.cards[i+2]]
                triple = check_and_append_triple(triple_candidate, triple)
            # phoenix triple
            if (self.phoenix_flag and
                  self.cards[i+1].power == self.cards[i+2].power):
                triple_candidate = [self.cards[0], self.cards[i+1],
                                    self.cards[i+2]]
                triple = check_and_append_triple(triple_candidate, triple)
            # multiple triples
            try:
                if (self.cards[i].power == self.cards[i+1].power and
                      self.cards[i+1].power == self.cards[i+3].power):
                    triple_candidate = [self.cards[i], self.cards[i+1],
                                        self.cards[i+3]]
                    triple = check_and_append_triple(triple_candidate, triple)
                if (self.cards[i].power == self.cards[i+2].power and
                      self.cards[i+2].power == self.cards[i+3].power):
                    triple_candidate = [self.cards[i], self.cards[i+2],
                                        self.cards[i+3]]
                    triple = check_and_append_triple(triple_candidate, triple)
                if (self.phoenix_flag and
                      self.cards[i+1].power == self.cards[i+3].power):
                    triple_candidate = [self.cards[0], self.cards[i+1],
                                        self.cards[i+3]]
                    triple = check_and_append_triple(triple_candidate, triple)
                if (self.phoenix_flag and
                      self.cards[i+1].power == self.cards[i+4].power):
                    triple_candidate = [self.cards[0], self.cards[i+1],
                                        self.cards[i+4]]
                    triple = check_and_append_triple(triple_candidate, triple)
            except IndexError:
                pass
        return triple

    def _get_available_four_bomb(self):
        """ Returns a list with all possible four bomb combinations. """
        four_bomb = list()
        for i in range(len(self.cards)-3):
            if (self.cards[i].power == self.cards[i+1].power and
                  self.cards[i+1].power == self.cards[i+2].power and
                  self.cards[i+2].power == self.cards[i+3].power):
                four_list = [self.cards[i], self.cards[i+1],
                             self.cards[i+2], self.cards[i+3]]
                four_cards = Cards(four_list)
                if four_cards.type == 'four_bomb':
                    four_bomb.append(four_cards)
        return four_bomb

    def _get_available_full(self):
        """ Returns a list with all possible full house combinations. """
        full = list()
        pair = self._get_available_pair()
        triple = self._get_available_triple()
        for i in pair:
            for j in triple:
                if i.power != j.power:
                    full_list = list()
                    full_list.extend(i.cards)
                    full_list.extend(j.cards)
                    full_cards = Cards(full_list)
                    if full_cards.type == 'full':
                        full.append(full_cards)
        return full

    def _get_available_straight(self):
        """ Returns a list with all possible straight combinations. """
        def check_candidate(candidate_list, straight, straight_bomb):
            if len(candidate_list) > 4:
                straight_cards = Cards(candidate_list)
                if straight_cards.type == 'straight':
                    straight.append(straight_cards)
                elif straight_cards.type == 'straight_bomb':
                    straight_bomb.append(straight_cards)
                else:
                    pass
            return straight, straight_bomb
        straight = list()
        straight_bomb = list()
        for i in range(len(self.cards)-4):
            candidate_list = list()
            phoenix_available = self.phoenix_flag
            for j in range(i,len(self.cards)):
                # add first card of possible straight
                if len(candidate_list)==0:
                    candidate_list.append(self.cards[j])
                    if self.cards[j].name == 'Phoenix':
                        phoenix_available = False
                # no check if Phoenix is last entry
                elif candidate_list[-1].name == 'Phoenix':
                    candidate_list.append(self.cards[j])
                    straight, straight_bomb = check_candidate(candidate_list,
                        straight, straight_bomb)
                # add subsequent cards
                elif candidate_list[-1].power+1 == self.cards[j].power:
                    candidate_list.append(self.cards[j])
                    straight, straight_bomb = check_candidate(candidate_list,
                        straight, straight_bomb)
                # skip pairs
                elif candidate_list[-1].power == self.cards[j].power:
                    pass
                # use phoenix mid straight if available
                elif (phoenix_available and
                    candidate_list[-1].power+2 == self.cards[j].power):
                    candidate_list.append(self.cards[0])
                    candidate_list.append(self.cards[j])
                    straight, straight_bomb = check_candidate(candidate_list,
                        straight, straight_bomb)
                    phoenix_available = False
                # use phoenix as first/last card if available
                elif phoenix_available:
                    candidate_list.append(self.cards[0])
                    straight, straight_bomb = check_candidate(candidate_list,
                        straight, straight_bomb)
                    phoenix_available = False
                # no straight possible
                else:
                    break
        return straight, straight_bomb

    def _get_available_pair_seq(self):
        """ Returns a list with all possible pair sequence combinations. """
        pair_seq = list()
        pair = self._get_available_pair()
        for i in range(len(pair)-1):
            candidate_list = list()
            for j in range(i,len(pair)):
                # add first element to candidate list
                if len(candidate_list) == 0:
                    candidate_list.extend(pair[j].cards)
                # add subsequent pairs
                elif candidate_list[-1].power+1 == pair[j].power:
                    candidate_list.extend(pair[j].cards)
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
        return pair_seq

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
