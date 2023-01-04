import csv

with open('result.txt', 'r') as f:
    red = 0
    black = 0
    draw = 0
    step = 0
    numGames = 0
    reader = csv.reader(f, delimiter=' ')
    for row in reader:
        numGames += 1
        if row[0] == 'Red':
            red += 1
        elif row[0] == 'Black':
            black += 1
        else:
            draw += 1
        step += int(row[3])
    print('# of games: ', numGames)
    print('Red winning rate: ', red / numGames)
    print('Black winning rate: ', black / numGames)
    print('Draw rate: ', draw / numGames)
    print('Average step: ', step / numGames)
