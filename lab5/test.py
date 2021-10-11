scoreboard_in = open('scoreboard.txt', 'r')
scoreboard = []


def funcSort(x):
    return int(x[1])


for line in scoreboard_in:
    current = line.split()
    scoreboard.append([current[0], current[1]])

print(scoreboard)
scoreboard.sort(key=funcSort)
print(scoreboard)
