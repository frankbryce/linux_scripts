#!/usr/bin/python

# When my son wanted to learn a card game, War was the first one that came to
# mind. I started playing and realized I couldn't remember how a "war" actually
# worked so I needed to look up the rules on wikipedia (I was getting confused
# with Egyption Ratscrew). Anyways, on the article it said
#
# > Game designer Greg Costikyan has observed that since there are no choices
# > in the game, and all outcomes are random, it cannot be considered a game by
# > some definitions.
#
# I nodded and moved on, but then as I was playing, my 4yo son said "I want to
# put the Ace on top so that it comes up faster". And I realized there _IS_
# a choice... you can always choose to put your higher cards sooner when you
# win a "battle". Even more impactful, I think, would be to sort your cards
# from a war to get the high ones first out of those 10 cards you just picked
# up. Each time would be a small effect, but since the game takes so effing
# long, I intuit that it would make a difference in your winning odds should
# you not do this.
#
# I'm making this monte carlo simulation for a few policies one might have when
# deciding to put cards in their deck (random, high first, low first, only sort
# after a war, only put highest card one top after war, etc). I don't know how
# much it would affect a winning percentage, or game length. Looking forward to
# what a computer simulator says.
#
# https://en.wikipedia.org/wiki/War_(card_game)

from enum import Enum
import numpy as np
import random
random.seed()
import sys
from tqdm import trange

class Card(Enum):
    TWO = 2
    THR = 3
    FOU = 4
    FIV = 5
    SIX = 6
    SEV = 7
    EIG = 8
    NIN = 9
    TEN = 10
    JAC = 11
    QUE = 12
    KIN = 13
    ACE = 14

    def __eq__(self, other):
        return self.value == other.value
    def __gt__(self, other):
        return self.value > other.value
    def __lt__(self, other):
        return self.value < other.value
    def __repr__(self):
        return self.name
    def __str__(self):
        return self.__repr__()

    def All():
        for card in Card.__members__.items():
            yield card[1]

class Deck:
    # build a deck. By default, cards=None tells the constructor to build
    # a default 52 deck of cards. If cards is passed in, the deck is set to
    # these cards.
    def __init__(self, cards=None):
        if cards is not None:
            self.cards = np.array(cards)
            return

        self.cards = []
        for card in Card.All():
            self.cards = np.append(self.cards, [card] * 4)

    # Take n cards from the top of this deck.
    # If there are fewer than n cards in the deck, it takes all of them.
    def Take(self, n):
        ret, self.cards = Deck(self.cards[:n]), self.cards[n:]
        return ret

    # Returns itself to be used in a fluent style.
    def Shuffle(self):
        np.random.shuffle(self.cards)
        return self

    # Take top n cards from the deck and return them
    def TakeCards(self, n=1):
        ret, self.cards = self.cards[:n], self.cards[n:]
        return ret

    # Take top card from the deck and return it
    def TakeCard(self):
        cards = self.TakeCards(1)
        if len(cards) == 0:
            return None
        return cards[0]

    # Put cards on the bottom of the deck.
    # Earlier in the array will be towards the top of the deck.
    def PutCardsOnBottom(self, cards):
        self.cards = np.append(self.cards, cards)

    # Put a card on the bottom of the deck.
    def PutCardOnBottom(self, card):
        return self.PutCardsOnBottom([card])

    # Returns number of cards in the deck
    def Len(self):
        return len(self.cards)

    def Print(self):
        cardDict = {}
        for card in Card.All():
            cardDict[card.name] = 0
        for card in self.cards:
            cardDict[card.name] += 1
        print(f"{len(self.cards)} Cards: {cardDict}")

class Policy(Enum):
    RANDOM = 0
    SORT_HIGH_LOW = 1
    SORT_LOW_HIGH = 2

class Player:

    def __init__(self, deck, policy=Policy.RANDOM, epsilon=0.01):
        self.deck = deck
        self.policy = policy
        self.epsilon = epsilon

    def PutCardsOnBottom(self, cards, verbose=False):
        if self.policy == Policy.RANDOM or random.random() < self.epsilon:
            np.random.shuffle(cards)
            self.deck.PutCardsOnBottom(cards)
        elif self.policy == Policy.SORT_HIGH_LOW:
            cards.sort()
            self.deck.PutCardOnBottom(cards[::-1])
        elif self.policy == Policy.SORT_LOW_HIGH:
            cards.sort()
            self.deck.PutCardsOnBottom(cards)
        else:
            raise Exception(f"Invalid Policy {self.policy}")
        if verbose:
            print(f"Winner put {cards} On Bottom")

    def Deck(self):
        return self.deck

class Game:

    def __init__(self, policy1=Policy.RANDOM, policy2=Policy.RANDOM,
            epsilon1=0.01, epsilon2=0.01):
        d1 = Deck().Shuffle()
        d2 = d1.Take(26)
        self.p1 = Player(d1, policy1, epsilon1)
        self.p2 = Player(d2, policy2, epsilon2)
        self.rounds = 0

    # Battle! Returns a player IFF that player wins. Returns None otherwise
    def Battle(self, verbose=False):
        self.rounds += 1
        c1, c2 = self.p1.Deck().TakeCard(), self.p2.Deck().TakeCard()
        def _verbose(prefix):
            if verbose:
                print(f"{prefix} Player 1: {c1} Player 2: {c2}")
        if c1 is None:
            return self.p2
        if c2 is None:
            return self.p1
        if c1 > c2:
            _verbose("player 1 wins!")
            self.p1.PutCardsOnBottom([c1,c2], verbose)
        elif c1 < c2:
            _verbose("player 2 wins!")
            self.p2.PutCardsOnBottom([c1,c2], verbose)
        elif c1 == c2:  # WAR!
            c1 = [c1]
            c2 = [c2]
            while c1[-1].value == c2[-1].value:
                new1 = self.p1.Deck().TakeCards(4)
                if len(new1) == 0:
                    _verbose("player 2 wins!")
                    self.p2.PutCardsOnBottom(np.append(c1,c2), verbose)
                    return
                new2 = self.p2.Deck().TakeCards(4)
                if len(new2) == 0:
                    _verbose("player 1 wins!")
                    self.p1.PutCardsOnBottom(np.append(c1,c2), verbose)
                    return
                c1 = np.append(c1, new1)
                c2 = np.append(c2, new2)
            if c1[-1].value > c2[-1].value:
                _verbose("player 1 wins!")
                self.p1.PutCardsOnBottom(np.append(c1,c2), verbose)
            elif c1[-1].value < c2[-1].value:
                _verbose("player 2 wins!")
                self.p2.PutCardsOnBottom(np.append(c1,c2), verbose)
            else:
                raise Exception("This should never happen")
        else:
            raise Exception("This should never happen")
        if self.p1.Deck().Len() == 0:
            return self.p2
        elif self.p2.Deck().Len() == 0:
            return self.p1
        if verbose:
            self.p1.Deck().Print()
            self.p2.Deck().Print()
        return None

    def Player1(self):
        return self.p1

    def Player2(self):
        return self.p2

    def Rounds(self):
        return self.rounds

totalRounds = 0
totalRuns = 0
p1Wins = 0
p2Wins = 0
policy1 = Policy.RANDOM
policy2 = Policy.RANDOM
if len(sys.argv) > 1:
    policy1 = Policy(int(sys.argv[1]))
if len(sys.argv) > 2:
    policy2 = Policy(int(sys.argv[2]))
nruns = 10000
if len(sys.argv) > 3:
    nruns = int(sys.argv[3])
verbose = False
if len(sys.argv) > 4:
    verbose = True
for i in trange(nruns):
    game = Game(policy1,policy2)
    winner = None
    while winner is None:
        winner = game.Battle(verbose)
    if winner == game.Player1():
        p1Wins += 1
    elif winner == game.Player2():
        p2Wins += 1
    else:
        raise Exception("This should never happen")
    totalRuns += 1
    totalRounds += game.Rounds()
print(f"Rounds per game: {totalRounds/totalRuns}, p1Wins: {p1Wins}, p2Wins: {p2Wins}")
