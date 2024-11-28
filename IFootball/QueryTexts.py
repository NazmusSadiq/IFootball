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
    team_stats_in_fav = """
        SELECT 
            c.competition_name, 
            c.competition_id,
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
        GROUP BY c.competition_id
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
            t.short_name,t.team_id,
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
        GROUP BY t.short_name, t.team_id
        ORDER BY points DESC, goal_difference DESC, goals_scored DESC
        """
       
    custom_competition_standings_query = """
        SELECT 
            t.team_name,
            COALESCE(SUM(CASE 
                WHEN (m.home_team_id = t.team_id AND s.full_time_home > s.full_time_away) OR 
                     (m.away_team_id = t.team_id AND s.full_time_away > s.full_time_home) THEN 3 
                WHEN s.full_time_home = s.full_time_away THEN 1 
                ELSE 0 
            END), 0) AS points,
            COALESCE(SUM(CASE 
                WHEN (m.home_team_id = t.team_id AND s.full_time_home > s.full_time_away) OR 
                     (m.away_team_id = t.team_id AND s.full_time_away > s.full_time_home) THEN 1 
                ELSE 0 
            END), 0) AS wins,
            COALESCE(SUM(CASE WHEN s.full_time_home = s.full_time_away THEN 1 ELSE 0 END), 0) AS draws,
            COALESCE(SUM(CASE 
                WHEN (m.home_team_id = t.team_id AND s.full_time_home < s.full_time_away) OR 
                     (m.away_team_id = t.team_id AND s.full_time_away < s.full_time_home) THEN 1 
                ELSE 0 
            END), 0) AS losses,
            COALESCE(SUM(CASE 
                WHEN m.home_team_id = t.team_id THEN s.full_time_home 
                ELSE s.full_time_away 
            END), 0) AS goals_scored,
            COALESCE(SUM(CASE 
                WHEN m.home_team_id = t.team_id THEN s.full_time_away 
                ELSE s.full_time_home 
            END), 0) AS goals_conceded,
            COALESCE(SUM(CASE 
                WHEN m.home_team_id = t.team_id THEN s.full_time_home 
                ELSE s.full_time_away 
            END), 0) - 
            COALESCE(SUM(CASE 
                WHEN m.home_team_id = t.team_id THEN s.full_time_away 
                ELSE s.full_time_home 
            END), 0) AS goal_difference
        FROM custom_teams t
        LEFT JOIN custom_matches m ON (m.home_team_id = t.team_id OR m.away_team_id = t.team_id) AND m.competition_id = %s
        LEFT JOIN scores s ON m.match_id = s.match_id
        WHERE t.competition_id = %s
        GROUP BY t.team_name
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
        WHERE m.competition_id = %s
        GROUP BY t.short_name
        ORDER BY t.short_name ASC;

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
        
    comp_previous_match_query = """
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
            m.subscribed,
            m.competition_id           
        FROM matches m
        JOIN teams t1 ON m.home_team_id = t1.team_id
        JOIN teams t2 ON m.away_team_id = t2.team_id
        LEFT JOIN scores s ON m.match_id = s.match_id
        JOIN competitions c ON m.competition_id = c.competition_id
            WHERE m.match_utc_date < NOW() and m.competition_id = %s
            ORDER BY m.match_utc_date DESC
            LIMIT 1;
        """  
        
    comp_next_match_query = """
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
            m.subscribed,
            m.competition_id          
        FROM matches m
        JOIN teams t1 ON m.home_team_id = t1.team_id
        JOIN teams t2 ON m.away_team_id = t2.team_id
        LEFT JOIN scores s ON m.match_id = s.match_id
        JOIN competitions c ON m.competition_id = c.competition_id
            WHERE m.match_utc_date > %s AND c.competition_id = %s
            ORDER BY m.match_utc_date DESC
            LIMIT 1;
            """
            
    query_top_scorers = """
        SELECT 
            ps.player_name,
            MAX(ps.team_name),
            SUM(ps.goals) AS total_goals
        FROM player_stats ps
        WHERE ps.competition_id = %s
        GROUP BY ps.player_name
        ORDER BY total_goals DESC
        LIMIT 5;
        """
        
    query_top_assists = """
        SELECT 
            ps.player_name,
            MAX(ps.team_name),
            SUM(ps.assists) AS total_assists
        FROM player_stats ps
        WHERE ps.competition_id = %s
        GROUP BY ps.player_name
        ORDER BY total_assists DESC
        LIMIT 5;
        """

    query_top_yellow_cards = """
        SELECT 
            ps.player_name,
            MAX(ps.team_name),
            SUM(ps.yellow_cards) AS total_yellow_cards
        FROM player_stats ps
        WHERE ps.competition_id = %s
        GROUP BY ps.player_name
        ORDER BY total_yellow_cards DESC
        LIMIT 5;
        """
        
    query_top_red_cards = """
        SELECT 
            ps.player_name,
            MAX(ps.team_name),
            SUM(ps.red_cards) AS total_red_cards
        FROM player_stats ps
        WHERE ps.competition_id = %s
        GROUP BY ps.player_name
        ORDER BY total_red_cards DESC
        LIMIT 5;
        """
        
    query_top_clean_sheets = """
        SELECT 
            ps.player_name,
            MAX(ps.team_name),
            SUM(ps.clean_sheets) AS total_clean_sheets
        FROM player_stats ps
        WHERE ps.competition_id = %s
        GROUP BY ps.player_name
        ORDER BY total_clean_sheets DESC
        LIMIT 5;
        """