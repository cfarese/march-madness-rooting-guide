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

                _, probA, _ = odds_calculator(teamA, teamB)
                winner = teamA if random.random() < probA else teamB
                loser = teamB if winner == teamA else teamA

                current_round.append(winner)
                eliminated.append(loser)

        # Score the result
        sim_scores = calculator(sim_results)[0]
        max_score = max(sim_scores)
        wins = [1 if score == max_score else 0 for score in sim_scores]
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