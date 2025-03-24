import json
import sys
import pandas as pd
import copy
import math

with open(sys.argv[1], "r") as file:
    bracket = json.load(file)

r2results = bracket.get("r2", [])
sixteenresults = bracket.get("sixteen", [])
eightresults = bracket.get("eight", [])
fourresults = bracket.get("four", [])
championshipresults = bracket.get("championship", [])
winnerresults = bracket.get("winner", [])
eliminatedr1 = bracket.get("eliminatedr1", [])
eliminatedr2 = bracket.get("eliminatedr2", [])
eliminatedsixteen = bracket.get("eliminatedsixteen", [])
eliminatedeight = bracket.get("eliminatedeight", [])
eliminatedfour = bracket.get("eliminatedfour", [])
eliminatedchampionship = bracket.get("eliminatedchampionship", [])
totalresults = [r2results, sixteenresults, eightresults, fourresults, championshipresults, winnerresults, eliminatedr1, eliminatedr2,
                eliminatedsixteen, eliminatedeight, eliminatedfour, eliminatedchampionship]

team1 = sys.argv[2]
team2 = sys.argv[3]
round_num = sys.argv[4] ##provide the round the game is played in

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
    x = (arg.replace('.json', ''))
    x = x.replace('picks/', '')
    players.append(x)

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
        for team in (givenresults[6] + givenresults[7]):
            if(team in sixteenpicks[i]):
                possibleScore -= 2
        for team in (givenresults[6] + givenresults[7] + givenresults[8]):
            if(team in eightpicks[i]):
                possibleScore -= 4
        for team in (givenresults[6] + givenresults[7] + givenresults[8] + givenresults[9]):
            if(team in fourpicks[i]):
                possibleScore -= 8
        for team in (givenresults[6] + givenresults[7] + givenresults[8] + givenresults[9] + givenresults[10]):
            if(team in championshippicks[i]):
                possibleScore -= 16
        for team in (givenresults[6] + givenresults[7] + givenresults[8] + givenresults[9] + givenresults[10] + givenresults[11]):
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

team1results = copy.deepcopy(totalresults)
team1results[int(round_num)-1].append(team1)
team1results[6 + int(round_num)-1].append(team2)

team1PointsTotals = calculator(team1results)

## Now for team 2

team2results = copy.deepcopy(totalresults)
team2results[int(round_num)-1].append(team2)
team2results[6 + int(round_num)-1].append(team1)

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

def normal_cdf(x, mean=0, std=1):
    #Approximate the cumulative distribution function for a normal distribution
    z = (x - mean) / (std * math.sqrt(2))
    return 0.5 * (1 + math.erf(z))

def odds_calculator(teamA, teamB): ## args should be team names

    with open("kenpom.json", "r") as file:
        kenpom = json.load(file)
        kenpom1 = kenpom.get(teamA)
        kenpom2 = kenpom.get(teamB)

    spread = (kenpom1 - kenpom2) * 0.68
    spread = round(spread / 0.5) * 0.5

    team1_win_prob = normal_cdf(spread / 9.5)
    team2_win_prob = 1 - team1_win_prob

    return [spread, team1_win_prob, team2_win_prob]

odds_array = odds_calculator(team1, team2)
spread = odds_array[0]
team1_win_prob = odds_array[1]
team2_win_prob = odds_array[2]

print("")
if(team1_win_prob > team2_win_prob):
    print("The spread is estimated to be -" + str(spread) + " in favor of " + team1)
elif(team1_win_prob < team2_win_prob):
    print("The spread is estimated to be +" + str(spread) + " in favor of " + team2)
print("")
print(team1 + " has an estimated win probability of " + str(round(team1_win_prob * 100, 2)) + "%")
print(team2 + " has an estimated win probability of " + str(round(team2_win_prob * 100, 2)) + "%")

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

df = df.sort_values(by=['Points', 'Potential'], ascending=[False, False])
print(df.to_string(index=False))