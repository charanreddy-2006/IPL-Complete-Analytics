-- ==========================================
-- ADVANCED IPL ANALYSIS
-- ==========================================


-- Toss decision impact

SELECT
    toss_decision,
    COUNT(*) AS matches,
    SUM(
        CASE
            WHEN toss_winner = winner
            THEN 1
            ELSE 0
        END
    ) AS toss_win_match_win
FROM matches
GROUP BY toss_decision;



-- Venue with most matches

SELECT
    venue,
    COUNT(*) AS matches
FROM matches
GROUP BY venue
ORDER BY matches DESC
LIMIT 10;