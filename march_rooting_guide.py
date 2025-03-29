import json
import sys
from operator import truediv

import pandas as pd
import copy
import math
import random

simulations = 1_000

if "-prob" in sys.argv:
    isprob = True
    sys.argv.remove("-prob")

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
totalresults = [r2results, sixteenresults, eightresults, fourresults, championshipresults, winnerresults, eliminatedr1,
                eliminatedr2,
                eliminatedsixteen, eliminatedeight, eliminatedfour, eliminatedchampionship]

team1 = sys.argv[2]
team2 = sys.argv[3]
round_num = sys.argv[4]  ##provide the round the game is played in

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
    x = x.rsplit('/', 1)[-1]
    players.append(x)


def calculator(givenresults):
    i = 0
    score = 0
    possibleScore = 192

    players_points = []
    players_possible_points = []

    while (i < len(players)):
        for result in givenresults[0]:
            if (result in r2picks[i]):
                score += 1
        for result in givenresults[1]:
            if (result in sixteenpicks[i]):
                score += 2
        for result in givenresults[2]:
            if (result in eightpicks[i]):
                score += 4
        for result in givenresults[3]:
            if (result in fourpicks[i]):
                score += 8
        for result in givenresults[4]:
            if (result in championshippicks[i]):
                score += 16
        for result in givenresults[5]:
            if (result in winnerpicks[i]):
                score += 32

        for team in givenresults[6]:
            if (team in r2picks[i]):
                possibleScore -= 1
        for team in (givenresults[6] + givenresults[7]):
            if (team in sixteenpicks[i]):
                possibleScore -= 2
        for team in (givenresults[6] + givenresults[7] + givenresults[8]):
            if (team in eightpicks[i]):
                possibleScore -= 4
        for team in (givenresults[6] + givenresults[7] + givenresults[8] + givenresults[9]):
            if (team in fourpicks[i]):
                possibleScore -= 8
        for team in (givenresults[6] + givenresults[7] + givenresults[8] + givenresults[9] + givenresults[10]):
            if (team in championshippicks[i]):
                possibleScore -= 16
        for team in (
                givenresults[6] + givenresults[7] + givenresults[8] + givenresults[9] + givenresults[10] + givenresults[
            11]):
            if (team in winnerpicks[i]):
                possibleScore -= 32

        players_points.append(score)
        players_possible_points.append(possibleScore)

        possibleScore = 192
        score = 0
        i += 1

    return [players_points, players_possible_points]


actualPointsTotals = calculator(totalresults)

## Now we calculate it if team 1 wins

## Team1 wins
forced_team1 = copy.deepcopy(totalresults)
forced_team1[int(round_num) - 1] = [team1]
forced_team1[6 + int(round_num) - 1] = [team2]
team1PointsTotals = calculator(forced_team1)

## Team2 wins
forced_team2 = copy.deepcopy(totalresults)
forced_team2[int(round_num) - 1] = [team2]
forced_team2[6 + int(round_num) - 1] = [team1]
team2PointsTotals = calculator(forced_team2)

shortTermRoot1 = []
shortTermRoot2 = []
longTermRoot1 = []
longTermRoot2 = []


def normal_cdf(x, mean=0, std=1):
    # Approximate the cumulative distribution function for a normal distribution
    z = (x - mean) / (std * math.sqrt(2))
    return 0.5 * (1 + math.erf(z))


def odds_calculator(teamA, teamB):  ## args should be team names

    with open("kenpom.json", "r") as file:
        kenpom = json.load(file)
        kenpom1 = kenpom.get(teamA)
        kenpom2 = kenpom.get(teamB)

    spread = (kenpom1 - kenpom2) * 0.68
    spread = round(spread / 0.5) * 0.5

    team1_win_prob = normal_cdf(spread / 9.5)
    team2_win_prob = 1 - team1_win_prob

    return [spread, team1_win_prob, team2_win_prob]


def monte_carlo(results, team1, team2, round_num, team1_win_prob, team2_win_prob):
    team1_counts = [0] * len(players)
    team2_counts = [0] * len(players)

    def simulate(results, force_winner):
        sim_results = copy.deepcopy(results)
        insert_into_round = int(round_num) - 1

        # Get the teams from the previous round
        prev_round_teams = sim_results[insert_into_round - 1] if insert_into_round > 0 else []

        # Build the current round with the forced winner
        sim_results[insert_into_round] = []
        sim_results[insert_into_round + 6] = []

        # Process the previous round's teams in pairs
        for i in range(0, len(prev_round_teams), 2):
            if i + 1 >= len(prev_round_teams):
                break

            teamA = prev_round_teams[i]
            teamB = prev_round_teams[i + 1]

            # If this is the matchup we're forcing
            if (teamA == team1 and teamB == team2) or (teamA == team2 and teamB == team1):
                sim_results[insert_into_round].append(force_winner)
                sim_results[insert_into_round + 6].append(team2 if force_winner == team1 else team1)
            else:
                # Simulate this matchup normally
                _, probA, _ = odds_calculator(teamA, teamB)
                winner = teamA if random.random() < probA else teamB
                loser = teamB if winner == teamA else teamA
                sim_results[insert_into_round].append(winner)
                sim_results[insert_into_round + 6].append(loser)

        # Simulate the remaining tournament
        for round_index in range(insert_into_round + 1, 6):
            prev_round = sim_results[round_index - 1]
            sim_results[round_index] = []
            sim_results[round_index + 6] = []
            current_round = sim_results[round_index]
            eliminated = sim_results[round_index + 6]

            # Process teams in pairs
            for i in range(0, len(prev_round), 2):
                if i + 1 >= len(prev_round):
                    break

                teamA = prev_round[i]
                teamB = prev_round[i + 1]

                # Only simulate if we haven't already determined the winner
                if len(current_round) <= i // 2 or current_round[i // 2] == "":
                    _, probA, _ = odds_calculator(teamA, teamB)
                    winner = teamA if random.random() < probA else teamB
                    loser = teamB if winner == teamA else teamA
                    current_round.append(winner)
                    eliminated.append(loser)
                else:
                    # Use the already determined winner
                    winner = current_round[i // 2]
                    loser = teamB if winner == teamA else teamA
                    eliminated.append(loser)

        # Score the result
        sim_scores = calculator(sim_results)[0]
        max_score = max(sim_scores)

        # Find all players with the maximum score
        max_score_players = [i for i, score in enumerate(sim_scores) if score == max_score]
        # Randomly select one winner from those players
        winner_index = random.choice(max_score_players)
        wins = [0] * len(players)
        wins[winner_index] = 1
        return wins

    for _ in range(simulations):
        team1_win = simulate(totalresults, team1)
        team2_win = simulate(totalresults, team2)

        for i in range(len(players)):
            team1_counts[i] += team1_win[i]
            team2_counts[i] += team2_win[i]

    # Convert counts to percentages
    team1_probs = [round(c / simulations * 100, 2) for c in team1_counts]
    team2_probs = [round(c / simulations * 100, 2) for c in team2_counts]

    # Weighted average for baseline
    baseline = [
        round(team1_win_prob * t1 + team2_win_prob * t2, 2)
        for t1, t2 in zip(team1_probs, team2_probs)
    ]

    # Delta: who gains most from team1 winning vs team2 winning
    delta = [round(t1 - t2, 2) for t1, t2 in zip(team1_probs, team2_probs)]

    return [baseline, team1_probs, team2_probs, delta]


odds_array = odds_calculator(team1, team2)
spread = odds_array[0]
team1_win_prob = odds_array[1]
team2_win_prob = odds_array[2]

probability_of_winning = monte_carlo(totalresults, team1, team2, round_num, team1_win_prob, team2_win_prob)

j = 0
while (j < len(players)):
    if (team1PointsTotals[0][j] > actualPointsTotals[0][j]):
        shortTermRoot1.append(players[j])
    elif (team2PointsTotals[0][j] > actualPointsTotals[0][j]):
        shortTermRoot2.append(players[j])

    if (probability_of_winning[3][j] > 0):
        longTermRoot1.append(players[j])
    elif (probability_of_winning[3][j] < 0):
        longTermRoot2.append(players[j])

    j += 1

print("")
if (team1_win_prob > team2_win_prob):
    print("The spread is estimated to be -" + str(spread) + " in favor of " + team1)
elif (team1_win_prob < team2_win_prob):
    print("The spread is estimated to be " + str(spread) + " in favor of " + team2)
elif (team1_win_prob == team2_win_prob):
    print("The spread is evens")
print("")
print(team1 + " has an estimated win probability of " + str(round(team1_win_prob * 100, 2)) + "%")
print(team2 + " has an estimated win probability of " + str(round(team2_win_prob * 100, 2)) + "%")
print("")
print("Probabilities calculated based on " + str(simulations) + " simulations")
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
if(isprob):
    df = pd.DataFrame({
        'Player': players,
        'Win Prob': probability_of_winning[0],
        f'{team1} Win Prob': probability_of_winning[1],
        f'{team2} Win Prob': probability_of_winning[2],
        f'Delta': probability_of_winning[3]
    })
    df = df.sort_values(by=['Win Prob'], ascending=[False])
else:
    df = pd.DataFrame({
        'Player': players,
        'Points': actualPointsTotals[0],
        'Potential': actualPointsTotals[1],
        'Win Prob': probability_of_winning[0],
        f'{team1} Pts': team1PointsTotals[0],
        f'{team1} Pot': team1PointsTotals[1],
        f'{team1} Win Prob': probability_of_winning[1],
        f'{team2} Pts': team2PointsTotals[0],
        f'{team2} Pot': team2PointsTotals[1],
        f'{team2} Win Prob': probability_of_winning[2],
        f'Delta': probability_of_winning[3]
    })

    df = df.sort_values(by=['Points', 'Potential'], ascending=[False, False])
print(df.to_string(index=False))