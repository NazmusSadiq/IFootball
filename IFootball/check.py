from Queries import Queries

# x = Queries.get_competition_stats(2018)
# y = Queries.get_competition_statstest(2018)
x= Queries.get_team_stats_in_fav(90)
print(x)
y = Queries.get_team_stats_in_favtest(90)

print(len(x), len(y), x==y)