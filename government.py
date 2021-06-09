import random as r
from institutions import Voter, Body, MultiHouse

def main():
    # 4 bodies:
    #   1. People
    people = Body('People', r.randint(1000,100000))
    #   2. Congress: House, Senate
    #   3. President
    #   4. SCOTUS
    # congresses threshholds to be set by People
    # president to be decided by people
    # scotus thresholds to be set by president


if __name__ == '__main__':
    main()
