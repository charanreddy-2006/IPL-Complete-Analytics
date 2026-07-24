-- ==========================================
-- IPL SEASON ANALYSIS
-- ==========================================


-- Matches per season

SELECT
    season,
    COUNT(DISTINCT match_id) AS matches
FROM matches
GROUP BY season
ORDER BY season;



-- Season winners

SELECT
    season,
    winner
FROM matches
WHERE winner IS NOT NULL
ORDER BY season;