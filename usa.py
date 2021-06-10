import random as r
from institutions import *

def main():
    # 4 bodies:
    #   1. People
    people = Body('People', r.randint(10000,100000))
    states = create_constituencies(people.members, 50)

    #   2. Congress: House, Senate
    #   3. President
    #   4. SCOTUS

    # President to be chosen by people from people
    # Senate to be chosen by states from states
    # House to be chosen by districts from districts
    # SCOTUS to be chosen by President


if __name__ == '__main__':
    main()
