# A: random set, B: random set
# A: random set, B: fixed set
# A: fixed size, B: fixed set
# A: fixed size, B: fixed size

# 2 random sets
# random set and fixed set
# fixed-size set and fixed set
# 2 fixed-size sets (different sizes)

"""
1. Perform N experiments. Each experiment consists of the following steps
    1.1. Generate one or two sets (random or of given size)
    1.2. Calculate set-to-set similarity
2. Aggregate the results into NDarray.
3. Save this NDarray.
4. p-value := number of entries in this array more extreme than given value.
"""
