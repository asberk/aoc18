day = "05"
lines = open("inputs/$(day).txt") do f
    readlines(f); #
end


function checkTypePolarity(a, b)
    sameType = (lowercase(a) == lowercase(b))
    oppositePolarity = (a ≠ b)
    return (sameType & oppositePolarity)
end


function collapse(s)
    if length(s) < 3
        return(s)
    end
    i = 1
    while i <= length(s)
        a = s[i]
        if i == length(s)
            global b = s[i-1]
        else
            global b = s[i+1]
        end
        if checkTypePolarity(a,b)
            s = (s[1:(i-1)] * s[(i+2):end])
            i -= 1
        else
            i += 1
        end
        if i < 1
            i = 1
        end
    end
    s
end


# test = "dabAcCaCBAcCcBaDdAba"
# input = test
input = lines[1]
println("Part 1: ", length(collapse(input)))

function removeAndReact(s, a)
    ss = replace(replace(s, a=>""), uppercase(a)=>"")
    c = collapse(ss)
    length(c)
end
min_length = length(input)
for a in 'a':'z'
    len = removeAndReact(input, a)
    if len < min_length
        global min_length = len
    end
end
println("Part 2: ", min_length)
