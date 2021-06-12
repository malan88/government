import math
from numpy.random import normal as norm, multinomial, pareto
import numpy as np
from more_itertools import split_into
import random as r

N = 7
STDDEV = 0.1
CENTER = 0

NORMPOOL = norm(loc=CENTER, scale=STDDEV, size=10000)
NORMPOOL.sort()

PARETOSHAPE = 1

PARETOPOOL = pareto(PARETOSHAPE, 10000)
PARETOPOOL.sort()


# helper function
def clamp(num): return max(min(num, 1.0), -1.0)


def get_random(distribution='normal'):
    """Normal distribution from 0 to 1 with STDDEV standard deviation from
    CENTER.
    """
    if distribution == 'normal':
        return norm(CENTER, STDDEV, 1)
    return None


def create_position():
    """A position is a tuple of N dimensions between 0 and 1"""
    return list(clamp(get_random()) for i in range(N))


def distance(p, q):
    """Finds the distance between two positions in N-dimensional space."""
    square = 0
    for pn, qn in zip(p,q):
        square += (pn-qn)**2
    return math.sqrt(square)


def create_compromise(position):
    """Compromise is the compliment of the distance between the voter and the
    origin. This signals polarization. The more radical the voter, the less
    compromising they are.
    """
    return clamp(1-distance([0]*N, position))


def create_constituencies(x, m):
    min_size = 2
    #distribution =  [clamp(r.choice(PARETOPOOL) )for _ in range(m)]
    distribution = [1/m] * m
    constituencies = multinomial(len(x) - m * min_size, distribution)
    constituencies = [int(const_size + min_size) for const_size in constituencies]
    return list(split_into(x, constituencies))


class Law:
    """A law is an arbitrary lambda with a position in N-dimensional political
    space.
    """
    def __init__(self, rule, position):
        self.rule = rule
        self.position = position


class Voter:
    """A voter is the atomic unit for decision in political space.

    In a dictatorship, there is only one voter.
    """
    def __init__(self, position=None):
        self.position = create_position() if not position else position
        self.compromise = create_compromise(self.position)

    def __repr__(self):
        return '<Voter {}>'.format(self.position)

    def vote(self, law):
        """To vote yea a voter must be no farther from the position of the law
        than their compromise allows.
        """
        return abs(distance(self.position, law.position)) < self.compromise

    def choose(self, choices):
        """To choose a voter finds the closest choice to themselves."""
        return min(distance(self.position, choice.position) for choice in choices)


class Office:
    def __init__(self, constituency):
        self.constituency = constituency

    def elect(self, candidates):
        votes = {choice:0 for choice in candidates}
        for member in self.constituency:
            votes[member.choose(candidates)] += 1
        self.occupant = max(votes, key=votes.get)

    def election(self, candidates=2):
        candidates = [choice(self.constituency) for _ in range(candidates)]
        return self.elect(candidates)

    def vote(self, law):
        return self.occupant.vote(law)

    def choose(self, choices):
        return self.occupant.choose(choices)


class Body:
    """A body is a distinct governing body that contains members.

    name: the name of the body (e.g., Senate)
    members: multi-type
        - integer: the number of members to be randomly generated
        - list of tuples: positions in N-dimensional space from which to
          generate members
        - list of Voters
    threshold: integer, the number of bodies above which positive votes must
               reach to pass
    """
    # bodies need the Positions and Positions need constituencies.
    def __init__(self, name, constituencies, threshold=None, cycles=1):
        self.name = name
        self.offices = [Office(constituency) for constituency in constituencies]
        self.threshold = (int(len(self.offices)/2) if threshold is None
                          else threshold)
        self.cycles = cycles
        self.current_cycle = 0

    def __repr__(self):
        return '<Body {} of {} members>'.format(self.name, len(self.members))

    def vote(self, law):
        """To vote, a body simply finds if the yeas are greater than their
        threshold.
        """
        return sum(m.vote(law) for m in self.offices) > self.threshold

    def choose(self, choices):
        """Choice is simply a plurality for a body."""
        votes = {choice:0 for choice in choices}
        for member in self.offices:
            votes[member.choose(choices)] += 1
        return max(votes, key=votes.get)

    def election(self):
        self.cycles
        self.current_cycle
        start = round(self.current_cycle/self.cycles * len(self.offices))
        end = start + round(self.current_cycle/self.cycles)
        for o in self.offices[start:end]:
            o.election()
        self.current_cycle += 1
        self.current_cycle %= self.cycles


class MultiBody:
    """A multi-body governmental structure, meant to simulate Congress.

    MultiBody's cannot choose, because that doesn't really make any sense.
    """
    def __init__(self, name, bodies, threshold=None):
        self.bodies = {b.name:b for b in bodies}
        self.name = name
        self.threshold = len(self.bodies) if threshold is None else threshold

    def vote(self):
        """To vote, a multi-body simply finds if the body-yeas are greater than
        it's threshold.
        """
        votes = [b.vote() for b in self.bodies.values()]
        return sum(votes) >= self.threshold
