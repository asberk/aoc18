changes = open("inputs/01.txt") do f
    parse.(Int64, readlines(f));#
end

# answer to part 1
p1 = sum(changes);

print("Part 1: ", p1)

print("\nPart 2: ")

n_changes = length(changes)

freq = 0
j = 1
FLAG = true;
observed = Dict();
observed[0] = 1;

while FLAG
    global freq
    global j
    global FLAG
    global observed
    
    freq += changes[j];
    if haskey(observed, freq)
        observed[freq] += 1
        FLAG = false;
        print(freq, '\n');
        break
    else
        observed[freq] = 1
        j += 1
        if j > n_changes
            j = 1
        end
    end
end
    

