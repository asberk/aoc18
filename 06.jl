day = "06"
lines = open("inputs/$(day).txt") do f
    readlines(f); #
end

function parseTuple(s)
    x, y = parse.(Int, split(s, ", "))
    [x,y]
end

locs = [parseTuple(s) for s in lines]
r_locs = [loc[1] for loc in locs]
c_locs = [loc[2] for loc in locs]
max_r = maximum(r_locs)
min_r = minimum(r_locs)
max_c = maximum(c_locs)
min_c = minimum(c_locs)

println(min_r, ", ", max_r)
println(min_c, ", ", max_c)

using LinearAlgebra

function cdist(U, V)
    return [norm(u-v, 1) for u in U, v in V]
end

grid = [[i,j] for i in (min_r-1):(max_r+1) for j in (min_c-1):(max_c+1)]
distances = cdist(locs, grid)
