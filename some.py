from math import log


def function():
    probability_sum = 0   
     # first of all, we have formula like - sigma p(x) * log 2 p(x)
    # x is just a variable, like if we have AAAA, then x will be A, but we should transfer this to a number.
    name = "AABB"
    p = 0
    total = 0
    dict = {}
    for letter in name:
        if letter in dict:
            dict[letter] += 1 # we are just adding value
        else:
            dict[letter] = 1

    for i in dict:
        p = dict[i] / len(name)
        total += -1 * p * log(p, 2)

    print(total) 



function()