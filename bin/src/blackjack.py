#!/usr/bin/python
import csv
from enum import Enum
from mpl_toolkits import mplot3d
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import random
import sys
from tqdm import trange
random.seed()

### Game Objects ###

class Card(Enum):
    ACE = 1
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

    # TODO: gotta pull from a deck of cards so it's more accurate.
    @classmethod
    def Random(cls):
        return cls(random.randrange(13)+1)

class Hand:
    def __init__(self, is_dealer):
        self.is_dealer = is_dealer
        self.hand = []
        self.sum = 0
        self.usable_aces = 0
        if is_dealer:
            self.addCardToHand()
        else:
            self.addCardToHand()
            self.addCardToHand()

    def addCardToHand(self):
        crd = Card.Random()
        self.hand.append(crd)
        if crd == Card.ACE:
            self.usable_aces += 1
            self.sum += 11
        elif crd in [Card.JAC, Card.QUE, Card.KIN]:
            self.sum += 10
        else:
            self.sum += crd.value
        while self.sum > 21 and self.usable_aces > 0:
            self.sum -= 10
            self.usable_aces -= 1
        
    def Hand(self):
        return self.hand

    def Sum(self):
        return self.sum

    def UsableAces(self):
        return self.usable_aces

    def Hit(self):
        if self.is_dealer:
            while self.sum <= 16:
                self.addCardToHand()
        else:
            self.addCardToHand()

class Game:
    class Action(Enum):
        HIT = 0
        STICK = 1

        @classmethod
        def Random(cls):
            return cls(random.randrange(2))

    def __init__(self):
        self.dealer = Hand(is_dealer=True)
        self.player = Hand(is_dealer=False)

    def State(self): # returns (usable_aces, player_sum, dealer_sum)
        return self.player.UsableAces(), self.player.Sum(), self.dealer.Sum()

    # If Game.Action.STICK is selected, a reward will be returned (-1 for loss,
    #     0 for tie, 1 for win)
    # If Game.Action.HIT is selected, a reward of -1 is returned on bust,
    #     otherwise None is returned.
    def Act(self, action):
        if self.player.Sum() > 21 or len(self.dealer.Hand()) > 1:
            raise Exception("Hand is over. No more actions allowed.")
        if action == Game.Action.STICK:
            self.dealer.Hit()
            if self.dealer.Sum() > 21:
                return 1
            elif self.dealer.Sum() > self.player.Sum():
                return -1
            elif self.dealer.Sum() == self.player.Sum():
                return 0
            return 1
        elif action == Game.Action.HIT:
            self.player.Hit()
            if self.player.Sum() > 21:
                return -1
            return None
        raise Exception(f"Invalid action: {action}")

class Policy:
    def __init__(self):
        self.actionValues = dict()  # state: [(sum, count)] indexed by Game.Action
    
    def bestActionValue(self, state):
        max_action = Game.Action.Random()
        max_value = -1
        if state in self.actionValues:
            for _, action in Game.Action.__members__.items():
                v = self.actionValues[state][action.value]
                if v[1] == 0:
                    val = 0
                else:
                    val = v[0]/v[1]
                if val > max_value:
                    max_value = val
                    max_action = action
        return max_action, max_value

    def GreedyAction(self, state):
        return self.bestActionValue(state)[0]

    def Value(self, state):
        return self.bestActionValue(state)[1]

    def StateActionReward(self, state, action, reward):
        if state in self.actionValues:
            curr = self.actionValues[state][action.value]
            self.actionValues[state][action.value] = (curr[0]+reward, curr[1]+1)
        else:
            self.actionValues[state] = [(0,0)] * len(Game.Action.__members__.items())
            self.actionValues[state][action.value] = (reward, 1)

    def Print(self):
        for state in sorted(self.actionValues):
            print(f'{state}: {self.actionValues[state]}')

    def GenerateGraph(self):  # returns fig & 2d array of ax objects created.
        fig = plt.figure()
        axes = [[None,None],[None,None]]

        for numaces in [0,1]:
            # REWARD 3d surface plot
            ax = fig.add_subplot(221+numaces, projection='3d')
            axes[0][numaces] = ax

            # Optimal Action 2d plot
            optimal_actions = np.zeros([10,10])
            ax = fig.add_subplot(223+numaces)
            axes[1][numaces] = ax

        self.UpdateGraph(fig, axes)
        return fig, axes

    def UpdateGraph(self, fig, axes):  # pass in what was returned from GenerateGraph()
        player_sums = np.arange(4, 22, 1)
        dealer_sums = np.arange(2, 12, 1)
        player_sums, dealer_sums = np.meshgrid(player_sums, dealer_sums)
        for numaces in [0,1]:
            # REWARD 3d surface plot
            ax = axes[0][numaces]
            ax.clear()
            ax.set_title('Value Function')
            ax.set_xlabel('player sum')
            ax.set_ylabel('dealer card')
            ax.set_zlabel(f'E[Reward] {numaces} aces')
            expected_rewards = np.zeros([10,18])
            for state in self.actionValues:
                # state: (usable_aces, player_sum, dealer_sum)
                if state[0] == numaces:
                    expected_rewards[state[2]-2][state[1]-4] = self.Value(state)
            ax.plot_surface(player_sums, dealer_sums, expected_rewards)

            # Optimal Action 2d plot
            ax = axes[1][numaces]
            ax.clear()
            ax.set_title('Hit (Green) or Stick (Red)')
            ax.set_xlabel('player sum')
            ax.set_ylabel('dealer card')
            optimal_actions = np.zeros([10,18])
            for state in self.actionValues:
                # state: (usable_aces, player_sum, dealer_sum)
                if state[0] == numaces:
                    optimal_actions[state[2]-2][state[1]-4] = self.GreedyAction(state).value
            cmap = mpl.colors.ListedColormap(['green','red'])
            ax.imshow(optimal_actions, cmap = cmap, extent=[4,21,11,2])


        # https://stackoverflow.com/questions/28269157/plotting-in-a-non-blocking-way-with-matplotlib
        plt.pause(0.001)


class Episode:
    def __init__(self, game):
        self.episode = []  # (state, action) tuples
        self.game = game

    def TakeAction(self, action):  # appends to episode & returns reward
        state = self.game.State()
        reward = self.game.Act(action)
        self.episode.append((state, action))
        return reward

    def TakeRandomAction(self):
        return self.TakeAction(Game.Action.Random())

    def StateActions(self):
        return self.episode

class LearningIteration:
    def __init__(self, policy, aplha=0.9):
        self.game = Game()
        self.episode = Episode(self.game)
        self.policy = policy

    def Run(self):
        reward = self.episode.TakeRandomAction()
        while reward is None:
            reward = self.episode.TakeAction(self.policy.GreedyAction(self.game.State()))
        # update policy
        for (state, action) in self.episode.StateActions():
            self.policy.StateActionReward(state, action, reward)

policy = Policy()
fig, axes = policy.GenerateGraph()
plt.ion()
plt.show()
iters = 1000000
if len(sys.argv) > 1:
    iters = int(sys.argv[1])
for i in trange(iters):
    iteration = LearningIteration(policy)
    iteration.Run()
    if i % 10000 == 9999:
        policy.UpdateGraph(fig, axes)
policy.Print()
plt.ioff()
plt.show()
