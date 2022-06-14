import pandas as pd

# Date Range
todays_date = '2022-06-08'
dates = pd.date_range('2022-04-07', todays_date)
# print(dates)

# Seq skipping Nth element
rows = list(range(1,34))
game_count= int(len(rows) / 4)
print(game_count)

start = 1
stop = 5
template = "Game {}:"
game_rows = dict()

for i in range(game_count):
    game_rows.update({template.format(i+1): rows[start:stop]})
    start += 4
    stop += 4

print(game_rows)

for game in game_rows:
    print(game)
    # for j in range(4):
    print(game_rows[game][0])
    print(game_rows[game][1])
    print(game_rows[game][2])
    print(game_rows[game][3])

# for game in game_rows:
    # print(game_rows[game][1])



