import miniprojects.game2048 as game

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