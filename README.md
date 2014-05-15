#Reversi (Othello) Strategy Explorer

###The purpose of this program is to explore strategies for the game of reversi (more popularly known by the brand name Othello). Reversi is a game played between two players which has a very large game tree of all positions (somewhere around 10<sup>28</sup> positions). Since the game tree would be so large, it is infeasible to find a complete strategy, therefore the game tree may be expanded and searched according to heuristic utility functions.

The program is made up of the following files and their corresponding purposes:

+ enums.py

 + Contains an enumeration specifying the two possible colors that may be played

+ game.py
 
 + Contains the actual game logic that allows two players to progress through the game against one another.

+ graphics.py
 
 + This library http://mcsp.wartburg.edu/zelle/python/graphics.py is a simple wrapper on TKinter
        
    