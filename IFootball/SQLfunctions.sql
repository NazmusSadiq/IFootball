DELIMITER //

CREATE FUNCTION fetch_teams()
RETURNS TEXT
DETERMINISTIC
BEGIN
    DECLARE team_list TEXT DEFAULT '';
    
    -- Concatenating team names into a single string
    SELECT GROUP_CONCAT(team_name SEPARATOR ', ') INTO team_list FROM teams;

    RETURN team_list;
END //

CREATE FUNCTION get_team_id_by_name(p_full_name VARCHAR(255))
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE team_id INT DEFAULT NULL;
    
    SELECT t.team_id INTO team_id 
    FROM teams t 
    WHERE t.team_name = p_full_name 
    LIMIT 1;

    RETURN team_id;
END //


CREATE FUNCTION get_team_full_name_by_id(p_team_id INT)
RETURNS VARCHAR(255)
DETERMINISTIC
BEGIN
    DECLARE team_name VARCHAR(255) DEFAULT NULL;
    
    SELECT t.team_name INTO team_name 
    FROM teams t 
    WHERE t.team_id = p_team_id 
    LIMIT 1;

    RETURN team_name;
END //

CREATE PROCEDURE get_last_matches(
    IN p_team_id INT,
    IN p_limit INT
)
BEGIN
    SELECT 
        m.match_id, 
        t1.short_name AS home_team, 
        t2.short_name AS away_team, 
        COALESCE(s.full_time_home, 'N/A') AS score1, 
        COALESCE(s.full_time_away, 'N/A') AS score2, 
        DATE_FORMAT(m.match_utc_date, '%Y-%m-%d') AS match_date, 
        c.competition_name,  
        m.matchday,
        m.home_team_id,
        m.away_team_id,
        m.subscribed            
    FROM matches m
    JOIN teams t1 ON m.home_team_id = t1.team_id
    JOIN teams t2 ON m.away_team_id = t2.team_id
    LEFT JOIN scores s ON m.match_id = s.match_id
    JOIN competitions c ON m.competition_id = c.competition_id 
    WHERE (m.home_team_id = p_team_id OR m.away_team_id = p_team_id) 
      AND m.match_utc_date <= NOW()
    ORDER BY m.match_utc_date ASC
    LIMIT p_limit;
END //


CREATE PROCEDURE get_team_stats_in_fav(IN p_team_id INT)
BEGIN
    CREATE TEMPORARY TABLE IF NOT EXISTS temp_team_stats AS
    (
        SELECT 
            c.competition_name, 
            c.competition_id,
            COUNT(m.match_id) AS total_matches,
            SUM(CASE 
                WHEN (m.home_team_id = p_team_id AND s.full_time_home > s.full_time_away) 
                  OR (m.away_team_id = p_team_id AND s.full_time_away > s.full_time_home) 
                THEN 1 ELSE 0 
            END) AS wins,
            SUM(CASE 
                WHEN s.full_time_home = s.full_time_away THEN 1 
                ELSE 0 
            END) AS draws,
            SUM(CASE 
                WHEN (m.home_team_id = p_team_id AND s.full_time_home < s.full_time_away) 
                  OR (m.away_team_id = p_team_id AND s.full_time_away < s.full_time_home) 
                THEN 1 ELSE 0 
            END) AS losses,
            SUM(CASE 
                WHEN m.home_team_id = p_team_id THEN s.full_time_home 
                ELSE s.full_time_away 
            END) AS goals_scored,
            SUM(CASE 
                WHEN m.home_team_id = p_team_id THEN s.full_time_away 
                ELSE s.full_time_home 
            END) AS goals_conceded
        FROM matches m
        JOIN scores s ON m.match_id = s.match_id
        JOIN competitions c ON m.competition_id = c.competition_id
        WHERE m.home_team_id = p_team_id OR m.away_team_id = p_team_id
        GROUP BY c.competition_id
    );

    -- Biggest Wins
    CREATE TEMPORARY TABLE IF NOT EXISTS temp_biggest_win AS
    (
        SELECT 
            c.competition_name,
            m.match_utc_date,
            t2.short_name AS opponent,
            GREATEST(ABS(s.full_time_home - s.full_time_away), 0) AS goal_difference,
            CASE 
                WHEN m.home_team_id = p_team_id THEN s.full_time_home 
                ELSE s.full_time_away 
            END AS team_goals,
            CASE 
                WHEN m.home_team_id = p_team_id THEN s.full_time_away 
                ELSE s.full_time_home 
            END AS opponent_goals,
            m.matchday 
        FROM matches m
        JOIN teams t2 ON (m.home_team_id = t2.team_id OR m.away_team_id = t2.team_id) AND t2.team_id != p_team_id
        JOIN scores s ON m.match_id = s.match_id
        JOIN competitions c ON m.competition_id = c.competition_id
        WHERE (m.home_team_id = p_team_id OR m.away_team_id = p_team_id) 
          AND ((m.home_team_id = p_team_id AND s.full_time_home > s.full_time_away) 
            OR (m.away_team_id = p_team_id AND s.full_time_away > s.full_time_home))
        ORDER BY goal_difference DESC, m.match_utc_date DESC
        LIMIT 1
    );

    -- Biggest Losses
    CREATE TEMPORARY TABLE IF NOT EXISTS temp_biggest_loss AS
    (
        SELECT 
            c.competition_name,
            m.match_utc_date,
            t2.short_name AS opponent,
            GREATEST(ABS(s.full_time_home - s.full_time_away), 0) AS goal_difference,
            CASE 
                WHEN m.home_team_id = p_team_id THEN s.full_time_home 
                ELSE s.full_time_away 
            END AS team_goals,
            CASE 
                WHEN m.home_team_id = p_team_id THEN s.full_time_away 
                ELSE s.full_time_home 
            END AS opponent_goals,
            m.matchday 
        FROM matches m
        JOIN teams t2 ON (m.home_team_id = t2.team_id OR m.away_team_id = t2.team_id) AND t2.team_id != p_team_id
        JOIN scores s ON m.match_id = s.match_id
        JOIN competitions c ON m.competition_id = c.competition_id
        WHERE (m.home_team_id = p_team_id OR m.away_team_id = p_team_id) 
          AND ((m.home_team_id = p_team_id AND s.full_time_home < s.full_time_away) 
            OR (m.away_team_id = p_team_id AND s.full_time_away < s.full_time_home))
        ORDER BY goal_difference DESC, m.match_utc_date DESC
        LIMIT 1
    );

    -- Final Output
    SELECT 
        ts.competition_name,
        ts.competition_id,
        ts.total_matches,
        ts.wins,
        ts.draws,
        ts.losses,
        ts.goals_scored,
        ts.goals_conceded,
        (ts.goals_scored - ts.goals_conceded) AS goal_difference,
        bw.match_utc_date AS biggest_win_date,
        bw.opponent AS biggest_win_opponent,
        bw.goal_difference AS biggest_win_goal_difference,
        bw.team_goals AS biggest_win_team_goals,
        bw.opponent_goals AS biggest_win_opponent_goals,
        bl.match_utc_date AS biggest_loss_date,
        bl.opponent AS biggest_loss_opponent,
        bl.goal_difference AS biggest_loss_goal_difference,
        bl.team_goals AS biggest_loss_team_goals,
        bl.opponent_goals AS biggest_loss_opponent_goals
    FROM temp_team_stats ts
    LEFT JOIN temp_biggest_win bw ON ts.competition_name = bw.competition_name
    LEFT JOIN temp_biggest_loss bl ON ts.competition_name = bl.competition_name;

    -- Drop temporary tables to clean up
    DROP TEMPORARY TABLE temp_team_stats;
    DROP TEMPORARY TABLE temp_biggest_win;
    DROP TEMPORARY TABLE temp_biggest_loss;
END //


CREATE PROCEDURE get_next_matches(IN team_id INT, IN limit_count INT)
BEGIN
    SELECT 
        m.match_id, 
        ht.short_name AS home_team, 
        at.short_name AS away_team, 
        m.match_utc_date, 
        c.competition_name,   
        m.matchday,
        m.home_team_id,
        m.away_team_id,
        m.subscribed          
    FROM matches m
    JOIN teams ht ON m.home_team_id = ht.team_id
    JOIN teams at ON m.away_team_id = at.team_id
    JOIN competitions c ON m.competition_id = c.competition_id
    WHERE (m.home_team_id = team_id OR m.away_team_id = team_id) 
      AND m.match_utc_date > NOW()
    ORDER BY m.match_utc_date ASC
    LIMIT limit_count;
END //


CREATE PROCEDURE get_competition_standings(IN competition_id INT)
BEGIN
    SELECT 
        t.short_name AS team_name, 
        t.team_id,
        SUM(CASE 
            WHEN (m.home_team_id = t.team_id AND s.full_time_home > s.full_time_away) OR 
                 (m.away_team_id = t.team_id AND s.full_time_away > s.full_time_home) THEN 3
            WHEN s.full_time_home = s.full_time_away THEN 1
            ELSE 0
        END) AS points,
        SUM(CASE 
            WHEN (m.home_team_id = t.team_id AND s.full_time_home > s.full_time_away) OR 
                 (m.away_team_id = t.team_id AND s.full_time_away > s.full_time_home) THEN 1
            ELSE 0
        END) AS wins,
        SUM(CASE WHEN s.full_time_home = s.full_time_away THEN 1 ELSE 0 END) AS draws,
        SUM(CASE 
            WHEN (m.home_team_id = t.team_id AND s.full_time_home < s.full_time_away) OR 
                 (m.away_team_id = t.team_id AND s.full_time_away < s.full_time_home) THEN 1
            ELSE 0
        END) AS losses,
        SUM(CASE 
            WHEN m.home_team_id = t.team_id THEN s.full_time_home
            ELSE s.full_time_away
        END) AS goals_scored,
        SUM(CASE 
            WHEN m.home_team_id = t.team_id THEN s.full_time_away
            ELSE s.full_time_home
        END) AS goals_conceded,
        (SUM(CASE 
            WHEN m.home_team_id = t.team_id THEN s.full_time_home
            ELSE s.full_time_away
        END) - SUM(CASE 
            WHEN m.home_team_id = t.team_id THEN s.full_time_away
            ELSE s.full_time_home
        END)) AS goal_difference
    FROM teams t
    JOIN matches m ON (m.home_team_id = t.team_id OR m.away_team_id = t.team_id)
    JOIN scores s ON m.match_id = s.match_id
    WHERE m.competition_id = competition_id
    GROUP BY t.short_name, t.team_id
    ORDER BY points DESC, goal_difference DESC, goals_scored DESC;
END //

CREATE PROCEDURE get_competition_stats(IN competition_id INT)
BEGIN
    SELECT 
        t.short_name AS team_name,
        SUM(CASE 
                WHEN (m.home_team_id = t.team_id AND s.full_time_home > s.full_time_away) OR 
                     (m.away_team_id = t.team_id AND s.full_time_away > s.full_time_home) THEN 1 
                ELSE 0 
            END) AS wins,
        SUM(CASE WHEN s.full_time_home = s.full_time_away THEN 1 ELSE 0 END) AS draws,
        SUM(CASE 
                WHEN (m.home_team_id = t.team_id AND s.full_time_home < s.full_time_away) OR 
                     (m.away_team_id = t.team_id AND s.full_time_away < s.full_time_home) THEN 1 
                ELSE 0 
            END) AS losses,
        SUM(CASE 
            WHEN m.home_team_id = t.team_id THEN s.full_time_home 
            ELSE s.full_time_away 
        END) AS goals_scored,
        SUM(CASE 
            WHEN m.home_team_id = t.team_id THEN s.full_time_away 
            ELSE s.full_time_home 
        END) AS goals_conceded,
        MIN(COALESCE(ts.yellow_cards, 5)) AS yellow_cards,  
        MIN(COALESCE(ts.red_cards, 5)) AS red_cards,
        MAX(COALESCE(ts.total_shots, 5)) AS total_shots,
        MAX(COALESCE(ts.on_target, 5)) AS on_target,
        MAX(COALESCE(ts.offsides, 5)) AS offsides,
        MAX(COALESCE(ts.fouls, 5)) AS fouls
    FROM teams t
    JOIN matches m ON (m.home_team_id = t.team_id OR m.away_team_id = t.team_id)
    JOIN scores s ON m.match_id = s.match_id
    LEFT JOIN team_stats ts ON ts.team_id = t.team_id AND ts.competition_id = m.competition_id
    WHERE m.competition_id = competition_id
    GROUP BY t.short_name
    ORDER BY t.short_name ASC;
END //


DELIMITER ;
