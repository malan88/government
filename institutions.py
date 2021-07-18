from abc import ABC, abstractmethod
from typing import Union, Tuple, Callable
import math
import random as r

from more_itertools import split_into
import numpy as np
from numpy.random import multinomial, normal as norm, pareto

N = 7
STDDEV = 0.1
CENTER = 0

NORMPOOL = norm(loc=CENTER, scale=STDDEV, size=10000)
NORMPOOL.sort()

PARETOSHAPE = 1

PARETOPOOL = pareto(PARETOSHAPE, 10000)
PARETOPOOL.sort()

Position = tuple[float, ...]
ORIGIN: Position = tuple([0.] * N)


# helper function
def clamp(num: float) -> float:
    return max(min(num, 1.0), -1.0)


def get_random() -> float:
    """Normal distribution from 0 to 1 with STDDEV standard deviation from
    CENTER.
    """
    return r.choice(NORMPOOL)


def create_position() -> Position:
    """A position is a tuple of N dimensions between 0 and 1"""
    return tuple(clamp(get_random()) for i in range(N))


def distance(p: Position, q: Position) -> float:
    """Finds the distance between two positions in N-dimensional space."""
    square: float = 0.
    for pn, qn in zip(p, q):
        square += (pn-qn)**2
    return math.sqrt(square)


def create_compromise(position: Position):
    """Compromise is the compliment of the distance between the voter and the
    origin. This signals polarization. The more radical the voter, the less
    compromising they are.
    """
    return clamp(1-distance(ORIGIN, position))


def create_constituencies(x: list[Position], m: int) -> list[list[Position]]:
    min_size: int = 2
    distribution: float = [1/m] * m
    constituency_sizes: np.ndarray = multinomial(
        len(x) - m * min_size, distribution)
    constituencies: list[int] = [int(const_size + min_size)
                                 for const_size in constituency_sizes]
    return list(split_into(x, constituencies))


class Politic(ABC):
    position: Position

    @abstractmethod
    def choose(self, options):
        raise NotImplementedError


class Law(Politic):
    """A law is an arbitrary lambda with a position in N-dimensional political
    space.
    """
    position: Position

    def __init__(self, rule: Callable, position: Position):
        self.rule: Callable = rule
        self.position: Position = position

    def choose(self, choices: list[Politic]) -> Politic:
        """To choose a law finds the closest choice to itself."""
        votes = {choice: distance(self.position, choice.position)
                 for choice in choices}
        return min(votes, key=votes.get)


class Voter(Politic):
    """A voter is the atomic unit for decision in political space.

    In a dictatorship, there is only one voter.
    """

    def __init__(self, position: Union[Position, None] = None):
        self.position: Position = create_position() if not position else position
        self.compromise: float = create_compromise(self.position)

    def __repr__(self) -> str:
        return '<Voter {}>'.format(self.position)

    def vote(self, law: Law) -> bool:
        """To vote yea a voter must be no farther from the position of the law
        than their compromise allows.
        """
        return abs(distance(self.position, law.position)) < self.compromise

    def choose(self, choices: list[Politic]) -> Politic:
        """To choose a voter finds the closest choice to themselves."""
        votes = {choice: distance(self.position, choice.position)
                 for choice in choices}
        return min(votes, key=votes.get)


class Constituency:
    def __init__(self, bodypolitic: list[Politic]):
        self.constituency:  list[Politic] = bodypolitic

    def choose(self, choices: list[Politic]) -> Politic:
        """Choice is simply a plurality for a body."""
        votes = {choice: 0 for choice in choices}
        for member in self.constituency:
            votes[member.choose(choices)] += 1
        return max(votes, key=votes.get)


class Office:
    def __init__(self, constituency: list[Voter]):
        self.constituency: list[Voter] = constituency

    def elect(self, candidates: list[Voter]) -> Voter:
        votes: dict[Voter, int] = {choice: 0 for choice in candidates}
        for member in self.constituency:
            votes[member.choose(candidates)] += 1
        self.occupant = max(votes, key=votes.get)
        return self.occupant

    def election(self, num: int = 2) -> Voter:
        candidates: list[Voter] = [
            r.choice(self.constituency) for _ in range(num)]
        return self.elect(candidates)

    def vote(self, law: Law) -> Law:
        return self.occupant.vote(law)

    def choose(self, choices: list[Politic]) -> Politic:
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
    @property
    def population(self) -> int:
        return len(self.offices)

    # bodies need the Positions and Positions need constituencies.
    def __init__(self, name: str, constituencies: list[list[Voter]], threshold: Union[int, None] = None, cycles: int = 1):
        self.name: str = name
        self.offices: list[Office] = [
            Office(constituency) for constituency in constituencies]
        self.threshold: int = (int(len(self.offices)/2)
                               if threshold is None else threshold)
        self.current_cycle = 0

        self.cycles = 1
        self.election()
        self.cycles = cycles

    def __repr__(self):
        return '<Body {} of {} members>'.format(self.name, len(self.offices))

    def vote(self, law):
        """To vote, a body simply finds if the yeas are greater than their
        threshold.
        """
        return sum(m.vote(law) for m in self.offices) > self.threshold

    def vote_tally(self, law):
        """To vote, a body simply finds if the yeas are greater than their
        threshold.
        """
        return sum(m.vote(law) for m in self.offices)

    def choose(self, choices):
        """Choice is simply a plurality for a body."""
        votes = {choice: 0 for choice in choices}
        for member in self.offices:
            votes[member.choose(choices)] += 1
        return max(votes, key=votes.get)

    def election(self):
        start = round(self.current_cycle/self.cycles * len(self.offices))
        end = start + round(1/self.cycles * len(self.offices))
        for o in self.offices[start:end]:
            o.election()
        self.current_cycle += 1
        self.current_cycle %= self.cycles


class MultiBody:
    """A multi-body governmental structure, meant to simulate Congress.

    MultiBody's cannot choose, because that doesn't really make any sense.
    """

    def __init__(self, name, bodies, threshold=None):
        self.bodies = {b.name: b for b in bodies}
        self.name = name
        self.threshold = len(self.bodies) if threshold is None else threshold

    def __repr__(self):
        return f'<{self.name} {self.bodies.keys()}>'

    def vote(self, law):
        """To vote, a multi-body simply finds if the body-yeas are greater than
        it's threshold.
        """
        votes = [b.vote(law) for b in self.bodies.values()]
        return sum(votes) >= self.threshold

    def veto_override(self, law, threshold=2/3):
        for house in self.bodies:
            if house.vote_tally(law)/house.population < threshold:
                return False
        return True

    def election(self):
        for b in self.bodies.values():
            b.election()
