day = "02"
lines = open("inputs/$(day).txt") do f
    readlines(f); #
end

# lines (Array)
# <str>
# umdryebvlapkozostecnihjexg
# amdryebalapkozfstwcnrhjqxg
# umdcyebvlapaozfstwcnihjqgg
# ymdryrbvlapkozfstwcuihjqxg
# umdrsebvlapkozxstwcnihjqig

println("Day $day")
# println.(lines[1:5])


function hasNumReps(s, n)
    u = unique(s)
    d = Dict([(uu, 0) for uu in u])
    for ss in s
        d[ss] += 1
    end
    d = [k for (k,v) in d if v == n]
    Int(length(d) > 0)
end

function countNumReps(lines, tups)
    prod([sum([hasNumReps(s, tup) for s in lines]) for tup in tups])
end

p1 = countNumReps(lines, (2,3))
print("Part 1: ")
println(p1)


function numDiffs(s1, s2)
    sum([1 for (a,b) in zip(s1, s2) if a != b])
end

for (i, s1) in enumerate(lines)
    for s2 in lines[i+1:end]
        if numDiffs(s1, s2) == 1
            print("Part 2: ")
            [print(a) for (a,b) in zip(s1, s2) if a == b]
            print("\n")
        end
    end
end
