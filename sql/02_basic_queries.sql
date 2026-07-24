-- ==========================================
-- IPL PLAYER ANALYSIS
-- ==========================================


-- Most Player of Match awards

SELECT
    player_of_match,
    COUNT(*) AS awards
FROM matches
WHERE player_of_match IS NOT NULL
GROUP BY player_of_match
ORDER BY awards DESC
LIMIT 10;



-- Top run scorers

SELECT
    batter,
    SUM(runs_scored) AS total_runs
FROM deliveries
GROUP BY batter
ORDER BY total_runs DESC
LIMIT 10;