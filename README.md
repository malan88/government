# Government Simulator

I'm interested in the idea of a monte carlo simulator for government systems. I'd like to abstract the concept of government into classes. The base unit is a Voter, and the library is/will be designed to be as flexible as possible.

What the users vote on is much more difficult to think about. I think a Law requires a separate class with a randomly generated threshold (just like a vote) and a to test against it.

Still not sure how that will work or be self-referential.

The base unit is a Voter, who either has a randomly set threshold, or a specific threshold (in the case of a president).

The Electoral College can be represented by slices of a populace (the population could be arbitrary, but I'm interested in asyncio gather to deal with 160 million voters).

Districts can also be slices.
