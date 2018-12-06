day = "03"
lines = open("inputs/$(day).txt") do f
    readlines(f); #
end


println("Day $day")


function parseClaim(s)
    (id, ss) = split(s, " @ ")
    id = id[2:end]
    (p0, p1) = split(ss, ": ")
    (x0, y0) = split(p0, ",")
    (x1, y1) = split(p1, "x")
    id = parse(Int64, id)
    x0 = parse(Int64, x0)
    y0 = parse(Int64, y0)
    x1 = parse(Int64, x1)
    y1 = parse(Int64, y1)
    return (id, x0, y0, x0 + x1 - 1, y0 + y1 - 1)
end

function areaOfOverlap(lines)
    M = zeros(1000, 1000);
    for s in lines
        (uid, ux0, uy0, ux1, uy1) = parseClaim(s)
        for x in ux0:ux1
            for y in uy0:uy1
                M[x+1, y+1] += 1
            end
        end
    end
    sum(M .> 1)
end

p1 = areaOfOverlap(lines)

println("Part 1: ", string(p1))

function overlapping(v, w)
    if isa(v, String)
        v = parseClaim(v)
    end
    if isa(w, String)
        w = parseClaim(w)
    end
    (vid, vx0, vy0, vx1, vy1) = v
    (wid, wx0, wy0, wx1, wy1) = w
    qx = (vx0 <= wx0) & (wx0 <= vx1)
    rx = (wx0 <= vx0) & (wx1 >= vx0) #(vx0 <= wx1) & (wx1 <= vx1)
    qy = (vy0 <= wy0) & (wy0 <= vy1)
    ry = (wy0 <= vy0) & (wy1 >= vy0) #(vy0 <= wy1) & (wy1 <= vy1)
    (qx & qy) | (qx & ry) | (rx & qy) | (rx & ry)
end

O = zeros(length(lines), length(lines))
possibles=[]
for (i, s1) in enumerate(lines)
    for (j, s2) in enumerate(lines[i+1:end])
        O[i,i+j] = overlapping(s1, s2)
        O[i+j,i] = O[i,i+j]
    end
    if all(O[i,:] .== 0)
       push!(possibles, parseClaim(s1)[1])
       break
   end
end
print("Part 2: ")
println.(possibles)
