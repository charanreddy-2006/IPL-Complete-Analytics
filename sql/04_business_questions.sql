SELECT batter,
SUM(runs_scored) AS Runs
FROM ipl_matches
GROUP BY batter
ORDER BY Runs DESC
LIMIT 10;
SELECT bowler,
COUNT(player_out) AS Wickets
FROM ipl_matches
WHERE player_out IS NOT NULL
GROUP BY bowler
ORDER BY Wickets DESC
LIMIT 10;
SELECT player_of_match,
COUNT(*) AS Awards
FROM ipl_matches
GROUP BY player_of_match
ORDER BY Awards DESC
LIMIT 10;
SELECT toss_winner,
COUNT(*) AS Toss_Wins
FROM ipl_matches
GROUP BY toss_winner
ORDER BY Toss_Wins DESC;
