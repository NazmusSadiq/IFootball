from Queries import Queries

class Stats:
    def get_competition_standings(competition_id):    
        # Get the standings using the get_competition_standings function
        ucl_standings = Queries.get_competition_standings(competition_id)
    
        # If standings were fetched successfully, return them
        if ucl_standings:
            return ucl_standings
        else:
            return "No data available for UCL standings."

