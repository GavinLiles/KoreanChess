# Korean chess

An implementation of chess made out of spite.

## TODO

- NEED TO FIX/ADD diagonal moves to pieces in palace
    - pieces can **only** move diagonally across the printed lines
- ~~Add a swap phase~~
- add win conditions
    - bikjang
        - A player may choose to place their king in direct sight of the opposing player's king.
        if this happens, the opposing player must move their king since they are now in check.
        However, if the player decides to do this, the game ends in a draw. Even if the player
        that initiated bikjang checkmates the opposing player. This can happen more than once
        by the same player 
- add point tracker
    - player class need captured_peices list
    - player class needs point variable
- multiplayer
- pieces moves with cursor when selected
- pieces design selection in settings
- timer
- move log
- sound effects
- music
- AI
- pass turn


Board and pieces taken from [this Github repo](https://github.com/Kadagaden/chess-pieces)