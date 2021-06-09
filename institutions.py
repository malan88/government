import math
from numpy.random import normal as norm
import random as r


DIMENSIONS = 2
STDDEV = 0.1
CENTER = 0.5

def get_random():
    return r.choice(norm(loc=CENTER, scale=STDDEV, size=100))

def create_position():
    return (get_random() for i in range(DIMENSIONS))

def compare(p, q):
    square = 0
    for pn, qn in zip(p,q):
        square += (pn-qn)**2
    return math.sqrt(square)


class Law:
    def __init__(self, rule, position):
        self.rule = rule
        self.position = position


class Voter:
    def __init__(self, position=position):
        self.position = get_random() if not position else position

    def __repr__(self):
        return '<Voter {}>'.format(self.position)

    def vote(self, law):
        # need to figure this one out, probably my side of the distribution with
        # some wiggle
        pass

    def choose(self, choices):
        smallest = 1000000000
        closest = None
        for choice in choices:
            val = compare(self.position, choice.position)
            if val < smallest:
                closest = choice
                smallest = val
            return closest


class Body:
    def __init__(self, name, members, threshold=None):
        if isinstance(members, int):
            self.members = [Voter() for _ in range(members)]
        elif isinstance(members[0], int):
            self.members = [Voter(m) for m in members]
        else:
            self.members = members
        self.name = name
        self.threshold = int(len(members)/2) if not threshold else threshold

    def __repr__(self):
        return '<Body {} of {} members>'.format(self.name, len(self.name))

    def vote(self):
        return sum(m.vote() for m in self.members) > self.threshold

    def choice(self, choices):
        # need a multi-option vote
        pass


class MultiHouse:
    def __init__(self, name, bodies, unanimous=True):
        self.bodies = bodies
        self.name = name
        self.unanimous = unanimous

    def vote(self):
        votes = [b.vote() for b in self.bodies]
        if self.unanimous:
            return all(votes)
        return sum(votes) > int(len(self.bodies)/2)
