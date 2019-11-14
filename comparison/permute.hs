import Data.List (delete)

permutations [] = [[]]
permutations xs = [ x:ys | x <- xs, ys <- permutations (delete x xs)]
main = do print $ permutations [ 1 .. 3 ]
