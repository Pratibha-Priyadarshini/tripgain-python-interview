import pandas as pd

# Load the dataset
df = pd.read_csv('matches.csv')


# Q1. Load the dataset and show basic information
print("Q1. Dataset Overview")

print(f"\nTotal number of matches: {len(df)}")
print(f"\nColumn names:\n{list(df.columns)}")
print(f"\nFirst 5 rows:")
print(df.head())
print(f"\nData Description:")
print(df.describe())
print(f"\nData Info:")
print(df.info())

# Q2. Player with most "Player of the Match" awards in close games
print("Q2. Most Player of the Match Awards in Close Games")

# Filter matches decided by 1 run or 1 wicket
close_matches = df[
    ((df['win_by_runs'] == 1) | (df['win_by_wickets'] == 1))
]

# Count Player of the Match awards
player_awards = close_matches['player_of_match'].value_counts()
print(f"\nPlayer with most 'Player of the Match' awards in close games:")
print(f"{player_awards.index[0]}: {player_awards.iloc[0]} awards")
print(f"\nTop 5 players:")
print(player_awards.head())

# Q3. Wankhede Stadium - Win by batting first vs second
print("Q3. Wankhede Stadium - Batting First vs Second")

wankhede = df[df['venue'] == 'Wankhede Stadium']
wins_batting_first = len(wankhede[wankhede['win_by_runs'] > 0])
wins_batting_second = len(wankhede[wankhede['win_by_wickets'] > 0])

print(f"\nWins by batting first (runs): {wins_batting_first}")
print(f"Wins by batting second (wickets): {wins_batting_second}")

if wins_batting_first > wins_batting_second:
    print(f"\nResult: More common to win by batting first at Wankhede Stadium")
else:
    print(f"\nResult: More common to win by batting second at Wankhede Stadium")

# Q4. Team with highest wins by margin > 50 runs
print("Q4. Team with Most Wins by Margin > 50 Runs")

big_wins = df[df['win_by_runs'] > 50]
team_big_wins = big_wins['winner'].value_counts()

print(f"\nTeam with highest number of wins by margin > 50 runs:")
print(f"{team_big_wins.index[0]}: {team_big_wins.iloc[0]} wins")
print(f"\nTop 5 teams:")
print(team_big_wins.head())

# Q5. Toss winner who set target and won
print("Q5. Toss Winner Set Target and Won")

# Team won toss, chose to bat first (set target), and won the match
toss_bat_win = df[
    (df['toss_winner'] == df['winner']) & 
    (df['toss_decision'] == 'bat')
]

print(f"\nNumber of times toss winner set target and won: {len(toss_bat_win)}")

# Q6. Which umpire officiated more KKR matches
print("Q6. Umpire with More KKR Matches")

# Filter matches involving Kolkata Knight Riders
kkr_matches = df[
    (df['team1'] == 'Kolkata Knight Riders') | 
    (df['team2'] == 'Kolkata Knight Riders')
]

# Count umpire appearances
umpire1_count = kkr_matches['umpire1'].value_counts()
umpire2_count = kkr_matches['umpire2'].value_counts()

# Combine both umpire columns
all_umpires = pd.concat([kkr_matches['umpire1'], kkr_matches['umpire2']])
umpire_total = all_umpires.value_counts()

print(f"\nTotal KKR matches: {len(kkr_matches)}")
print(f"\nTop umpires in KKR matches:")
print(umpire_total.head())

# Compare umpire1 vs umpire2 position
total_umpire1_appearances = len(kkr_matches['umpire1'].dropna())
total_umpire2_appearances = len(kkr_matches['umpire2'].dropna())

print(f"\nTotal umpire1 position appearances in KKR matches: {total_umpire1_appearances}")
print(f"Total umpire2 position appearances in KKR matches: {total_umpire2_appearances}")
