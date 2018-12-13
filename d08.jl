day = "08"
lines = open("inputs/$(day).txt") do f
    readlines(f); #
end

lines = [parse(Int, x) for x in split(lines[1], " ")]

function parseTree(T)
    nc, nm = T[1:2]
    T = T[3:end]

    totals = 0
    values = []
    for i in 1:nc
        total, value, T = parseTree(T)
        totals += total
        push!(values, value)
    end

    totals += sum(T[1:nm])
    if nc == 0
        return totals, totals, T[nm+1:end]
    else
        value = sum([values[j] for j in T[1:nm]
                     if ((j > 0) & (j <= length(values)))])
        return totals, value, T[nm+1:end]
    end
end

t, v, r = parseTree(lines)
println("Day ", day)
println("-------------")
println("Part 1: ", t)
println("Part 2: ", v)
println("remaining:", r)
