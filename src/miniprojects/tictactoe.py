"""
Tic Tac Toe game

@author: Dmitry Marcautsan
"""

import random
import coursera.poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 1         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
def mc_trial(board, player):
    """ Play game until finished by switching players and performing random moves """
    while board.check_win() is None:
        empty_cells = board.get_empty_squares()
        next_move = random.choice(empty_cells)
        board.move(next_move[0], next_move[1], player)
        player = provided.switch_player(player)
        
def mc_update_scores(scores, board, player):
    """Update scores for a finished game"""
    winner = board.check_win()
    if winner == provided.DRAW:
        return
    
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            square = board.square(row, col)
            if square == player:
                scores[row][col] = scores[row][col] + (SCORE_CURRENT if winner == player else -SCORE_CURRENT)
            elif square == provided.switch_player(player):
                scores[row][col] = scores[row][col] + (SCORE_OTHER if winner != player else -SCORE_OTHER)

def get_best_move(board, scores):
    """Choose the next move randomly from empty cells with maximum score"""
    empty_squares = board.get_empty_squares()
    if len(empty_squares) == 0:
        return
    
    max_score = max([scores[empty[0]][empty[1]] for empty in empty_squares])
    possible_moves = [empty for empty in empty_squares if scores[empty[0]][empty[1]] == max_score]
    return random.choice(possible_moves)

def mc_move(board, player, trials):
    """Returns the next move by first performing simulation, updating scores and finally choosing the next move according to scores"""
    scores = [[0.0 for dummycol in range(board.get_dim())] 
                           for dummyrow in range(board.get_dim())]
    
    for dummytrial in range(NTRIALS):
        trial_board = board.clone()
        mc_trial(trial_board, player)
        mc_update_scores(scores, trial_board, player)
        
    return get_best_move(board, scores)
    
