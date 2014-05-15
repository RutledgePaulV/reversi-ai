#Reversi (Othello) Strategy Explorer
##

##Purpose
####The purpose of this program is to explore strategies for the game of [reversi](http://en.wikipedia.org/wiki/Reversi) (more popularly known by the brand name Othello). Reversi is a game played between two players which has a very large game tree of all positions (somewhere around 10<sup>28</sup> positions). Since the game tree would be so large, it is infeasible to find a complete strategy, therefore the game tree may be expanded and searched according to heuristic utility functions.


##Application Structure

+ **enums.py**

 + Contains an enumeration specifying the two possible colors that may be played

+ **game.py**
 
 + Contains the actual game logic that allows two players to progress through the game against one another.

+ **graphics.py**
 
 + This library [graphics.py](http://mcsp.wartburg.edu/zelle/python/graphics.py) is a simple wrapper on TKinter
        
+ **renderer.py**
 
 + Sets up the window object and managed drawing a board / refreshing the current board in the window.
 
+ **strategy.py**
 
 + Contains the heuristic definitions to be used in navigating and expanding the game tree.
 
+ **structures.py**
 
 + This is the main content of this program as it handles the game board and pieces as well as the logic for determining a positions validity and making a move.
 
+ **weightings.py**
 
 + This is a helper class for generating particular weightings to be used with the weighted sum heuristic.