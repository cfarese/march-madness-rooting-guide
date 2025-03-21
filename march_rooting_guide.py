import json
import sys
import pandas as pd

with open(sys.argv[1], "r") as file:
    bracket = json.load(file)

r2results = bracket.get("r2", [])
sixteenresults = bracket.get("sixteen", [])
eightresults = bracket.get("eight", [])
fourresults = bracket.get("four", [])
championshipresults = bracket.get("championship", [])
winnerresults = bracket.get("winner", [])
eliminatedresults = bracket.get("eliminated", [])

totalresults = [r2results, sixteenresults, eightresults, fourresults, championshipresults, winnerresults, eliminatedresults]

team1 = sys.argv[2]
team2 = sys.argv[3]
round = sys.argv[4] ##provide the round the game is played in

r2picks = []
sixteenpicks = []
eightpicks = []
fourpicks = []
championshippicks = []
winnerpicks = []

players = []

for arg in sys.argv[5:]:
    with open(arg, "r") as file:
        bracket = json.load(file)

    r2picks.append(bracket.get("r2", []))
    sixteenpicks.append(bracket.get("sixteen", []))
    eightpicks.append(bracket.get("eight", []))
    fourpicks.append(bracket.get("four", []))
    championshippicks.append(bracket.get("championship", []))
    winnerpicks.append(bracket.get("winner", []))


for arg in sys.argv[5:]:
    players.append(arg.replace('.json', ''))

def calculator(givenresults):
    i = 0
    score = 0
    possibleScore = 192

    players_points = []
    players_possible_points = []

    while(i < len(players)):
        for result in givenresults[0]:
            if(result in r2picks[i]):
                score += 1
        for result in givenresults[1]:
            if(result in sixteenpicks[i]):
                score += 2
        for results in givenresults[2]:
            if(results in eightpicks[i]):
                score += 4
        for result in givenresults[3]:
            if(result in fourpicks[i]):
                score += 8
        for result in givenresults[4]:
            if(result in championshippicks[i]):
                score += 16
        for result in givenresults[5]:
            if(result in winnerpicks[i]):
                score += 32

        for team in givenresults[6]:
            if(team in r2picks[i]):
                possibleScore -= 1
        for team in givenresults[6]:
            if(team in sixteenpicks[i]):
                possibleScore -= 2
        for team in givenresults[6]:
            if(team in eightpicks[i]):
                possibleScore -= 4
        for team in givenresults[6]:
            if(team in fourpicks[i]):
                possibleScore -= 8
        for team in givenresults[6]:
            if(team in championshippicks[i]):
                possibleScore -= 16
        for team in givenresults[6]:
            if(team in winnerpicks[i]):
                possibleScore -= 32

        players_points.append(score)
        players_possible_points.append(possibleScore)

        possibleScore = 192
        score = 0
        i += 1

    return [players_points, players_possible_points]

actualPointsTotals = calculator(totalresults)

## Now we calculate it if team 1 wins

team1results = totalresults
team1results[int(round)-1].append(team1)
team1results[6].append(team2)

team1PointsTotals = calculator(team1results)

## Now for team 2

team2results = totalresults
team2results[int(round)-1].append(team2)
team2results[int(round)-1].remove(team1)
team2results[6].append(team1)
team2results[6].remove(team2)

team2PointsTotals = calculator(team2results)

shortTermRoot1 = []
shortTermRoot2 = []
longTermRoot1 = []
longTermRoot2 = []

j = 0
while(j < len(players)):
    if(team1PointsTotals[0][j] > actualPointsTotals[0][j]):
        shortTermRoot1.append(players[j])
    elif (team2PointsTotals[0][j] > actualPointsTotals[0][j]):
        shortTermRoot2.append(players[j])

    if (max(team1PointsTotals[1])-team1PointsTotals[1][j] < max(team2PointsTotals[1])-team2PointsTotals[1][j]):
        longTermRoot1.append(players[j])
    elif (max(team2PointsTotals[1])-team2PointsTotals[1][j] < max(team1PointsTotals[1])-team1PointsTotals[1][j]):
        longTermRoot2.append(players[j])

    j += 1

print("")
print("The following players are rooting for " + team1 + " short term:")
print(shortTermRoot1)
print("")
print("The following players are rooting for " + team2 + " short term:")
print(shortTermRoot2)
print("")
print("")
print("The following players are rooting for " + team1 + " long term:")
print(longTermRoot1)
print("")
print("The following players are rooting for " + team2 + " long term:")
print(longTermRoot2)
print("")
df = pd.DataFrame({
    'Player': players,
    'Points': actualPointsTotals[0],
    'Potential': actualPointsTotals[1],
    f'{team1} Pts': team1PointsTotals[0],
    f'{team1} Pot': team1PointsTotals[1],
    f'{team2} Pts': team2PointsTotals[0],
    f'{team2} Pot': team2PointsTotals[1],
})

print(df.to_string(index=False))