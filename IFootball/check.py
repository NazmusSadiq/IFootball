from Queries import Queries

x = Queries.get_competition_stats(2018)
y = Queries.get_competition_statstest(2018)

print(len(x),len(y),x==y)