from random import randint
from institutions import *

def main():
    # 4 bodies:
    #   1. People
    people = [Voter() for _ in range(randint(10000,100000))]

    #   2. Congress: House, Senate
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
    senate.election()
    senate.election()
    senate.election()
    house = Body('House', districts)
    house.election()

    congress = MultiBody('Congress', [senate, house])

    #   3. President
    ec = [size+2 for size in size_of_districts]
    candidates = [choice(people) for _ in range(2)]

    #   4. SCOTUS

    # President to be chosen by people from people
    # Senate to be chosen by states from states
    # House to be chosen by districts from districts
    # SCOTUS to be chosen by President


if __name__ == '__main__':
    main()
