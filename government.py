import random as r

class Voter:
    def __init__(self, threshold=None):
        self.threshold = r.random() if not threshold else threshold

    def __repr__(self):
        return '<Voter {}>'.format(self.threshold)

    def vote(self):
        return r.random() > self.threshold


class Body:
    def __init__(self, name, members, threshold=None):
        self.members = [Voter() for _ in range(members)]
        self.name = name
        self.threshold = int(len(members)/2) if not threshold else threshold

    def __repr__(self):
        return '<Body {} of {} members>'.format(self.name, len(self.name))

    def vote(self):
        votes = [m.vote() for m in self.members]
        tally = sum(votes)
        return tally > self.threshold


class MultiHouse:
    def __init__(self, name, bodies, unanimous=True):
        self.bodies = []
        for body in bodies:
            self.bodies.append(Body(*body))
        self.name = name
        self.unanimous = unanimous

    def vote(self):
        votes = [b.vote() for b in self.bodies]
        if self.unanimous:
            return all(votes)
        return sum(votes) > int(len(self.bodies)/2)


if __name__ == '__main__':
    # 4 bodies:
    #   1. Congress # needs recursion? No, because House and Senate
    #       - House
    #       - Senate
    #   2. President
    #   3. SCOTUS
    #   4. People

    # congresses threshholds to be set by People
    # president to be decided by people
    # scotus thresholds to be set by president
