# Government Simulator

I'm interested in the idea of a monte carlo simulator for government systems.
I'd like to abstract the concept of government into classes. The base unit is a
Voter, and the library is/will be designed to be as flexible as possible.

What the users vote on is much more difficult to think about. I think a Law
requires a separate class with a randomly generated threshold (just like a vote)
and a to test against it.

Still not sure how that will work or be self-referential.

The base unit is a Voter, who either has a randomly set threshold, or a specific
threshold (in the case of a president).

The Electoral College can be represented by slices of a populace (the population
could be arbitrary, but I'm interested in asyncio gather to deal with 160
million voters).

Districts can also be slices.

Need to deal with choices. Weighted choices.

AH, THAT'S SIMPLE: I'm not dealing with multiple parties, always two choices.

Whichever choice's threshold is closer to theirs, that's who they choose.

That's perfect.

Correction: I am dealing with multiple parties if I have a parliamentary system,
etc. I should really get more familiar with how voting systems result in how
many parties. It would be cool to simulate the proliferation of parties. Problem
is I'm doing a linear gradient instead of a two dimensional (or
multi-dimensional) political compass. I should eventually implement that.
