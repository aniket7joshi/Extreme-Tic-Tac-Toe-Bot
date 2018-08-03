# Extreme TicTacToe Bot

A multi-agent bot for the Extreme TicTacToe Tournament. A 4 * 4 board is further subdivided into 4 * 4 blocks. The bot plays against the opponent using Artificial Intelligence.

## Methodology

It searches with iteratively increasing the depth of the search. It uses minimax algorithm with alpha-beta pruning to decide its move and on reaching the depth limit it uses a heuristic function as a quantitative analysis of the board state. It also uses Zobrist Hashing to compute the next move quickly if the same state of the board is acquired again.
