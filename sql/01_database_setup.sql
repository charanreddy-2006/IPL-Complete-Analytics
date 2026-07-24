-- ==========================================
-- IPL TEAM PERFORMANCE ANALYSIS
-- ==========================================


-- Total matches won by each team

SELECT
    winner,
    COUNT(*) AS total_wins
FROM matches
WHERE winner IS NOT NULL
GROUP BY winner
ORDER BY total_wins DESC;



-- Most participated teams

SELECT
    team,
    COUNT(*) AS matches_played
FROM
(
    SELECT team1 AS team
    FROM matches

    UNION ALL

    SELECT team2 AS team
    FROM matches
)
GROUP BY team
ORDER BY matches_played DESC;