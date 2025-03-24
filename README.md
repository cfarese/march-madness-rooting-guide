# March Madness Rooting Guide

A Python tool that helps you determine which team to root for in March Madness games based on your bracket picks and potential tournament outcomes.

## Features

- Calculates win probabilities based on KenPom ratings
- Simulates tournament outcomes using Monte Carlo simulation
- Shows both short-term and long-term rooting interests
- Provides detailed statistics about potential points and tournament outcomes

## Usage

```bash
python3 march_rooting_guide.py results.json team1 team2 round_num picks/*.json
```

### Arguments:
- `results.json`: The current tournament results file
- `team1`: First team in the matchup
- `team2`: Second team in the matchup
- `round_num`: The round number where the game is played (1-6)
- `picks/*.json`: Path to bracket pick files

### Example:
```bash
python3 march_rooting_guide.py results.json Michigan Michigan_State 4 picks/*.json
```

## Output

The tool will show:
- Estimated spread and win probabilities
- Short-term rooting interests (based on immediate points)
- Long-term rooting interests (based on tournament outcomes)
- Detailed statistics for each player's bracket

## Requirements

- Python 3.x
- Required packages:
  - pandas
  - json
  - math
  - random

## Files

- `march_rooting_guide.py`: Main script
- `kenpom.json`: KenPom ratings data
- `results.json`: Current tournament results
- `picks/*.json`: Individual bracket picks