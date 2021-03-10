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

    def __repr__(self):
        return self.name
    def __str__(self):
        return __repr__(self)

    def All():
        for card in Card.__members__.items():
            yield card[1]

class Deck:
    # build a deck. By default, cards=None tells the constructor to build
    # a default 52 deck of cards. If cards is passed in, the deck is set to
    # these cards.
    def __init__(self, cards=None):
        if cards is not None:
            self.cards = cards
            return

        self.cards = []
        for card in Card.All():
            self.cards.extend([card] * 4)

    # Take n cards from the top of this deck.
    # If there are fewer than n cards in the deck, it takes all of them.
    def Take(self, n):
        ret, self.cards = Deck(self.cards[:n]), self.cards[n:]
        return ret

    # Returns itself to be used in a fluent style.
    def Shuffle(self):
        np.random.shuffle(self.cards)
        return self

    # Returns number of cards in the deck
    def Len(self):
        return len(self.cards)

    def Print(self):
        cardDict = {}
        for card in Card.All():
            cardDict[card] = 0
        for card in self.cards:
            cardDict[card] += 1
        print(cardDict)


d1 = Deck().Shuffle()
d2 = d1.Take(26)

