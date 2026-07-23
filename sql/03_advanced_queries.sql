SELECT batter,
SUM(runs_scored) AS Total_Runs
FROM ipl_matches
GROUP BY batter
ORDER BY Total_Runs DESC
LIMIT 10;
SELECT bowler,
COUNT(player_out) AS Wickets
FROM ipl_matches
WHERE player_out IS NOT NULL
GROUP BY bowler
ORDER BY Wickets DESC
LIMIT 10;
SELECT winner,
COUNT(*) AS Wins
FROM ipl_matches
GROUP BY winner
ORDER BY Wins DESC;
SELECT venue,
COUNT(*) AS Matches
FROM ipl_matches
GROUP BY venue
ORDER BY Matches DESC;
