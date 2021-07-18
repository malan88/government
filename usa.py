from random import randint, choice
from institutions import (Constituency, Law, Body, MultiBody)


def get_president(size_of_districts, states, people, incumbent=None):
    ec = [size+2 for size in size_of_districts]
    if incumbent:
        candidates = {incumbent: 0, choice(people): 0}
    else:
        candidates = {choice(people): 0 for _ in range(2)}
    for votes, state in zip(ec, states):
        constituency = Constituency(state)
        candidates[constituency.choose(candidates)] += votes
    president = max(candidates, key=candidates.get)
    if not hasattr(president, 'term'):
        president.term = 1
    else:
        president.term += 1
    return president


def main():
    passed, rejected = [], []

    people = [Voter() for _ in range(randint(10000, 100000))]

    states = create_constituencies(people, 50)
    size_of_districts = [round(len(state)/len(people)*435) for state in states]
    difference = 435 - sum(size_of_districts)

    while difference != 0:
        direction = -1 if difference > 0 else 1
        size_of_districts[difference] += direction
        difference += direction

    districts = []
    for district, state in zip(size_of_districts, states):
        districts.extend(create_constituencies(state, district))

    senate = Body('Senate', states*2, threshold=60, cycles=3)
    house = Body('House', districts)

    congress = MultiBody('Congress', [senate, house])

    president = get_president(size_of_districts, states, people)

    session = 10  # session laws
    sessions = 10  # of sessions

    for i in range(session * sessions):
        law = Law(randint(0, 10000), create_position())
        cvote = congress.vote(law)
        if cvote:
            pvote = president.vote(law)
            if not pvote:
                override = congress.veto_override(law)
                if override:
                    passed.append(law)
                else:
                    rejected.append(law)
            else:
                passed.append(law)

        if not i % session:
            print("Midterm", i / session)
            congress.election()

        if not i % (session * 2):
            print("Presidential election")
            if president.term < 2:
                president = get_president(
                    size_of_districts, states, people, president)
            else:
                president = get_president(size_of_districts, states, people)

    print(len(passed), len(rejected))
    print('Conservatism:', len(rejected)/(session * sessions))


if __name__ == '__main__':
    main()
