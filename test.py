hash = 31;
for char in "811312A":
    if char == "A":
        hash = hash * 31 + 65
    else:
        hash = hash * 31 + int(char) + 48
print(hash)
