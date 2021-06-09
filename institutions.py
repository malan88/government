import math
from numpy.random import normal as norm
import random as r

N = 2
STDDEV = 0.1
CENTER = 0.5

RPOOL = norm(loc=CENTER, scale=STDDEV, size=10000)
RPOOL.sort()


# helper function
def clamp(num): return max(min(num, 1.0), 0.0)


def get_random():
    """Normal distribution from 0 to 1 with STDEV standard deviation from
    CENTER.
    """
    return r.choice(RPOOL)


def create_position():
    """A position is a tuple of N dimensions between 0 and 1"""
    return (clamp(get_random()) for i in range(N))


def create_compromise(position):
    """Compromise is the compliment of the distance between the voter and the
    origin. This signals polarization. The more radical the voter, the less
    compromising they are.
    """
    return clamp(1-distance((0)*N, position))


def distance(p, q):
    """Finds the distance between two positions in N-dimensional space."""
    square = 0
    for pn, qn in zip(p,q):
        square += (pn-qn)**2
    return math.sqrt(square)


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
        return min(distance(self.position, choice.position for choice in choices))


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
    def __init__(self, name, members, threshold=None):
        """Takes """
        if isinstance(members, int):
            self.members = [Voter() for _ in range(members)]
        elif isinstance(members[0], int):
            self.members = [Voter(m) for m in members]
        elif isinstance(members[0], Voter):
            self.members = members
        else:
            raise TypeError("Required: members (int, [(int*N)], or [Voter])")
        self.name = name
        self.threshold = (int(len(self.members)/2) if threshold is not None
                          else threshold)

    def __repr__(self):
        return '<Body {} of {} members>'.format(self.name, len(self.members))

    def vote(self, law):
        """To vote, a body simply finds if the yeas are greater than their
        threshold.
        """
        return sum(m.vote(law) for m in self.members) > self.threshold

    def choose(self, choices):
        """Choice is simply a plurality for a body."""
        votes = {choice:0 for choice in choices}
        for member in self.members:
            votes[member.choose(choices)] += 1
        return max(votes, key=votes.get)


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
