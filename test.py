import miniprojects.game2048 as game
import coursera.poc_ttt_provided as provided
import miniprojects.tictactoe as tictactoe

assert (game.merge([0,0,0,0]) == [0,0,0,0])
assert (game.merge([0,0,0,2]) == [2,0,0,0])
assert (game.merge([0,0,2,2]) == [4,0,0,0])
assert (game.merge([0,2,0,2]) == [4,0,0,0])
assert (game.merge([0,2,2,2]) == [4,2,0,0])
assert (game.merge([2,0,2,2]) == [4,2,0,0])
assert (game.merge([2,0,2,0]) == [4,0,0,0])
assert (game.merge([2,2,2,0]) == [4,2,0,0])
assert (game.merge([2,2,2,2]) == [4,4,0,0])
assert (game.merge([4,4,8,8]) == [8,16,0,0])
assert (game.merge([8,8,8,2]) == [16,8,2,0])

board = provided.TTTBoard(3, False, [[provided.PLAYERX, provided.PLAYERX, provided.PLAYERO], [provided.PLAYERO, provided.PLAYERX, provided.EMPTY], [provided.EMPTY, provided.PLAYERX, provided.PLAYERO]])
scores = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
tictactoe.mc_update_scores(scores, board, 2)
assert scores == [[1.0, 1.0, -1.0], [-1.0, 1.0, 0], [0, 1.0, -1.0]]