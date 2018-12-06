day = "04"
lines = open("inputs/$(day).txt") do f
    readlines(f); #
end

lines = sort(lines)

function parseLog(s)
    (s1, s2) = split(s, ":")
    (min, log) = split(s2, "] ")
    gid = split(log, "#")
    if length(gid) > 1
        gid = gid[2]
        gid = split(gid, " ")[1]
        gid = parse(Int, gid)
        event = nothing
    else
        gid = nothing
        event = log
    end
    return (gid, event, parse(Int, min))
end

function fillGuardIDs(gids)
    for (i, g) in enumerate(gids)
        if g == nothing
            gids[i] = gids[i-1]
        end
    end
    gids
end

logs = [parseLog(s) for s in lines]
gids = getindex.(logs, 1)
gids = fillGuardIDs(gids);
events = getindex.(logs, 2)
mins = getindex.(logs, 3);

ugids = unique(gids)
d = Dict([(u, 0) for u in ugids])
dd = Dict([(u, zeros(60)) for u in ugids])

for (i, (g1, e1, m1)) in enumerate(zip(gids, events, mins))
    if e1 == "falls asleep"
        (g2, e2, m2) = (gids[i+1], events[i+1], mins[i+1])
        if (e2 == "wakes up") && (g2 == g1)
            d[g1] += (m2 - m1)
            dd[g1][(1+m1):(m2)] .+= 1
        else
            d[g1] += (60 - m1)
            dd[g1][(1+m1):end] .+= 1
        end
    end
end

sleepy_gid = [k for (k,v) in d if v == maximum(values(d))][1]
sleepy_minute = [i-1 for (i,x) in enumerate(dd[sleepy_gid])
                 if x == maximum(dd[sleepy_gid])][1]
p1 = sleepy_gid * sleepy_minute
print("Part 1: ", sleepy_gid, " * ", sleepy_minute, " = ", )
println(p1)


most_sleeps = maximum([maximum(dd[u]) for u in ugids])
for u in ugids
    if any(dd[u] .== most_sleeps)
        global p2gid, p2min, p2
        p2gid = u
        p2min = findall(x->x==most_sleeps, dd[u])[1] - 1
        p2 = p2gid * p2min
        break
    end
end
println("Part 2: ", p2gid, " * ", p2min, " = ", p2)
