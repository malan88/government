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
