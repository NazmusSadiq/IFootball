class QueryTexts:
    last_matches_query = """
        SELECT 
            m.match_id, 
            t1.short_name AS home_team, 
            t2.short_name AS away_team, 
            s.full_time_home, 
            s.full_time_away, 
            m.match_utc_date, 
            c.competition_name,  
            m.matchday,
            m.home_team_id,
            m.away_team_id,
            m.subscribed            
        FROM matches m
        JOIN teams t1 ON m.home_team_id = t1.team_id
        JOIN teams t2 ON m.away_team_id = t2.team_id
        LEFT JOIN scores s ON m.match_id = s.match_id
        JOIN competitions c ON m.competition_id = c.competition_id -- Join to get competition name
        WHERE (m.home_team_id = %s OR m.away_team_id = %s) 
          AND m.match_utc_date <= NOW()
        ORDER BY m.match_utc_date ASC
        LIMIT %s
        """

    biggest_win_query = """
        SELECT 
            c.competition_name,
            m.match_utc_date,
            t2.short_name AS opponent,
            GREATEST(ABS(s.full_time_home - s.full_time_away), 0) AS goal_difference,
            CASE 
                WHEN m.home_team_id = %s THEN s.full_time_home 
                ELSE s.full_time_away 
            END AS team_goals,
            CASE 
                WHEN m.home_team_id = %s THEN s.full_time_away 
                ELSE s.full_time_home 
            END AS opponent_goals,
            m.matchday 
        FROM matches m
        JOIN teams t2 ON (m.home_team_id = t2.team_id OR m.away_team_id = t2.team_id) AND t2.team_id != %s
        JOIN scores s ON m.match_id = s.match_id
        JOIN competitions c ON m.competition_id = c.competition_id
        WHERE (m.home_team_id = %s OR m.away_team_id = %s) 
          AND ((m.home_team_id = %s AND s.full_time_home > s.full_time_away) OR (m.away_team_id = %s AND s.full_time_away > s.full_time_home))
        ORDER BY c.competition_name, goal_difference DESC, m.match_utc_date DESC
        """
        
    biggest_loss_query = """
        SELECT 
            c.competition_name,
            m.match_utc_date,
            t2.short_name AS opponent,
            GREATEST(ABS(s.full_time_home - s.full_time_away), 0) AS goal_difference,
            CASE 
                WHEN m.home_team_id = %s THEN s.full_time_home 
                ELSE s.full_time_away 
            END AS team_goals,
            CASE 
                WHEN m.home_team_id = %s THEN s.full_time_away 
                ELSE s.full_time_home 
            END AS opponent_goals,
            m.matchday 
        FROM matches m
        JOIN teams t2 ON (m.home_team_id = t2.team_id OR m.away_team_id = t2.team_id) AND t2.team_id != %s
        JOIN scores s ON m.match_id = s.match_id
        JOIN competitions c ON m.competition_id = c.competition_id
        WHERE (m.home_team_id = %s OR m.away_team_id = %s) 
          AND ((m.home_team_id = %s AND s.full_time_home < s.full_time_away) OR (m.away_team_id = %s AND s.full_time_away < s.full_time_home))
        ORDER BY c.competition_name, goal_difference DESC, m.match_utc_date DESC
        """
        
    next_matches_query = """
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
        JOIN competitions c ON m.competition_id = c.competition_id  -- Join to get competition name
        WHERE (m.home_team_id = %s OR m.away_team_id = %s) 
          AND m.match_utc_date > NOW()
        ORDER BY m.match_utc_date ASC
        LIMIT %s
        """
        
    overall_team_stats_query = """
        SELECT 
            c.competition_name, 
            COUNT(m.match_id) AS total_matches,
            SUM(CASE 
                WHEN (m.home_team_id = %s AND s.full_time_home > s.full_time_away) OR (m.away_team_id = %s AND s.full_time_away > s.full_time_home) THEN 1 
                ELSE 0 
            END) AS wins,
            SUM(CASE 
                WHEN s.full_time_home = s.full_time_away THEN 1 
                ELSE 0 
            END) AS draws,
            SUM(CASE 
                WHEN (m.home_team_id = %s AND s.full_time_home < s.full_time_away) OR (m.away_team_id = %s AND s.full_time_away < s.full_time_home) THEN 1 
                ELSE 0 
            END) AS losses,
            SUM(CASE 
                WHEN m.home_team_id = %s THEN s.full_time_home 
                ELSE s.full_time_away 
            END) AS goals_scored,
            SUM(CASE 
                WHEN m.home_team_id = %s THEN s.full_time_away 
                ELSE s.full_time_home 
            END) AS goals_conceded
        FROM matches m
        JOIN scores s ON m.match_id = s.match_id
        JOIN competitions c ON m.competition_id = c.competition_id
        WHERE m.home_team_id = %s OR m.away_team_id = %s
        GROUP BY c.competition_name
        """
        
    competition_standings_query = """
        SELECT 
            t.short_name,
            SUM(CASE 
                WHEN (m.home_team_id = t.team_id AND s.full_time_home > s.full_time_away) OR (m.away_team_id = t.team_id AND s.full_time_away > s.full_time_home) THEN 3 
                WHEN s.full_time_home = s.full_time_away THEN 1 
                ELSE 0 
            END) AS points,
            SUM(CASE 
                WHEN (m.home_team_id = t.team_id AND s.full_time_home > s.full_time_away) OR (m.away_team_id = t.team_id AND s.full_time_away > s.full_time_home) THEN 1 
                ELSE 0 
            END) AS wins,
            SUM(CASE WHEN s.full_time_home = s.full_time_away THEN 1 ELSE 0 END) AS draws,
            SUM(CASE 
                WHEN (m.home_team_id = t.team_id AND s.full_time_home < s.full_time_away) OR (m.away_team_id = t.team_id AND s.full_time_away < s.full_time_home) THEN 1 
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
        WHERE m.competition_id = %s
        GROUP BY t.short_name
        ORDER BY points DESC, goal_difference DESC, goals_scored DESC
        """
        
    competition_standings_near_team_query = """
        SELECT 
            t.team_id,
            t.short_name,
            SUM(CASE 
                WHEN (m.home_team_id = t.team_id AND s.full_time_home > s.full_time_away) OR (m.away_team_id = t.team_id AND s.full_time_away > s.full_time_home) THEN 3 
                WHEN s.full_time_home = s.full_time_away THEN 1 
                ELSE 0 
            END) AS points,
            SUM(CASE 
                WHEN (m.home_team_id = t.team_id AND s.full_time_home > s.full_time_away) OR (m.away_team_id = t.team_id AND s.full_time_away > s.full_time_home) THEN 1 
                ELSE 0 
            END) AS wins,
            SUM(CASE WHEN s.full_time_home = s.full_time_away THEN 1 ELSE 0 END) AS draws,
            SUM(CASE 
                WHEN (m.home_team_id = t.team_id AND s.full_time_home < s.full_time_away) OR (m.away_team_id = t.team_id AND s.full_time_away < s.full_time_home) THEN 1 
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
        WHERE m.competition_id = %s
        GROUP BY t.team_id, t.short_name
        ORDER BY points DESC, goal_difference DESC, goals_scored DESC
        """
       
    competition_stats_query = """
        SELECT 
        t.short_name,
        SUM(CASE 
                WHEN (m.home_team_id = t.team_id AND s.full_time_home > s.full_time_away) OR (m.away_team_id = t.team_id AND s.full_time_away > s.full_time_home) THEN 1 
                ELSE 0 
            END) AS wins,
            SUM(CASE WHEN s.full_time_home = s.full_time_away THEN 1 ELSE 0 END) AS draws,
            SUM(CASE 
                WHEN (m.home_team_id = t.team_id AND s.full_time_home < s.full_time_away) OR (m.away_team_id = t.team_id AND s.full_time_away < s.full_time_home) THEN 1 
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
        0 AS yellow_cards,  
        0 AS red_cards,
        0 AS total_shots,
        0 AS on_target,
        0 AS offsides,
        0 AS fouls
    FROM teams t
    JOIN matches m ON (m.home_team_id = t.team_id OR m.away_team_id = t.team_id)
    JOIN scores s ON m.match_id = s.match_id
    WHERE m.competition_id = %s
    GROUP BY t.short_name
    ORDER BY t.short_name ASC
        """
    
    def get_fixtures_query(placeholders):
        fixtures_query = f"""
            SELECT
                m.match_utc_date,
                m.matchday,
                t1.short_name AS home_team,
                t2.short_name AS away_team,
                s.full_time_home AS home_score,
                s.full_time_away AS away_score,
                m.competition_id,
                m.home_team_id,
                m.away_team_id,
                m.match_id,
                m.subscribed,
                CASE 
                    WHEN m.match_utc_date < NOW() THEN 'Last Match'
                    ELSE 'Next Match'
                END AS match_status
            FROM matches m
            JOIN teams t1 ON m.home_team_id = t1.team_id
            JOIN teams t2 ON m.away_team_id = t2.team_id
            JOIN scores s ON m.match_id = s.match_id
            WHERE m.competition_id IN ({placeholders})
            AND m.match_utc_date BETWEEN DATE_SUB(CURDATE(), INTERVAL %s WEEK)  -- From 'last' weeks ago
                                AND DATE_ADD(CURDATE(), INTERVAL %s WEEK)  -- To 'next' weeks in future
            ORDER BY m.match_utc_date ASC
            """
        
        return fixtures_query
        
    subscribed_matches_query = """
        SELECT 
            m.match_utc_date,
            m.matchday,
            t1.short_name AS home_team,
            t2.short_name AS away_team,
            s.full_time_home AS home_score,
            s.full_time_away AS away_score,
            m.competition_id,
            m.match_id,
            m.home_team_id,
            m.away_team_id,
            m.subscribed
        FROM matches m
        JOIN teams t1 ON m.home_team_id = t1.team_id
        JOIN teams t2 ON m.away_team_id = t2.team_id
        LEFT JOIN scores s ON m.match_id = s.match_id
        WHERE m.subscribed = 'Yes' 
        AND m.match_utc_date BETWEEN DATE_SUB(CURDATE(), INTERVAL %s WEEK)  -- From 'last' weeks ago
                                AND DATE_ADD(CURDATE(), INTERVAL %s WEEK)  -- To 'next' weeks in future
        ORDER BY m.match_utc_date ASC
        """
        
    add_to_existing_competition_query = """
            INSERT INTO competitions (competition_id, competition_name, competition_code, competition_type, competition_emblem)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                competition_name=VALUES(competition_name), 
                competition_code=VALUES(competition_code), 
                competition_type=VALUES(competition_type), 
                competition_emblem=VALUES(competition_emblem)
        """