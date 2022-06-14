# Scraping 2022 MLB Betting Odds
# Saves data in .csv file named '2022_MLB_BettingOdds.csv'

# Import Packages
from re import L
import time
from numpy import NaN
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create a list of dates to scrape data from
todays_date = '2022-06-10'
## 2022 Opening Day was 2022-04-07
dates = pd.date_range('2022-04-07', todays_date)

# Create empty lists to store data scraped from each game
date = []
away_team_name = []
away_team_abbr = []
home_team_name = []
rot_num_away_team = []
rot_num_home_team = []
away_team_runline_open = []
away_team_runline_open_odds = []
away_team_runline_close = []
away_team_runline_close_odds = []
home_team_runline_open = []
home_team_runline_open_odds = []
home_team_runline_close = []
home_team_runline_close_odds = []
away_team_moneyline_open = []
away_team_moneyline_close = []
home_team_moneyline_open = []
home_team_moneyline_close = []
over_open = []
over_open_odds = []
over_close = []
over_close_odds = []
under_open = []
under_open_odds = []
under_close = []
under_close_odds = []

# Desired URL
url = 'https://www.actionnetwork.com/mlb/odds'
# Initiate Driver
driver = webdriver.Chrome(service=Service('/Users/jake/chromedriver'))
# Launch the Site
driver.get(url)

try:

    for i in range(len(dates)):

        # Wait for game table to load
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[3]/div/div/table/tbody/tr[1]/td[1]/div/a/div[1]/div/div[1]'))
            )  

        # Ensure Table has updated - only way I could get this to work
        time.sleep(2)

        # Find the current date of the games being scraped
        current_date = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[2]/div[2]/div[1]/span')
        print(current_date.text)

        # Find the rows containing the desired odds
        ## Note: find_elements will return a list
        rows = driver.find_elements(By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[3]/div/div/table/tbody/tr')  

        # Find the number of games to be scraped from the current day
        game_count = int(len(rows) / 4)
        print("Games Today: ", game_count)

        # Identify the corresponding rows for each game
        ## Note: Each game is given 4 rows, so I created a dictionary to store the groups of rows for each game
        template = "Game {}:"
        game_rows = dict()
        start = 0
        stop = 4

        for i in range(game_count):
            game_rows.update({template.format(i+1): rows[start:stop]})
            start += 4
            stop += 4

        # Loop through the games and add the data to their respective lists
        for game in game_rows:

            ## Add the date
            date.append(current_date.text)
            
            ## First Row, First Cell - Team Names and Rotation Numbers
            away_team_name.append(game_rows[game][0].find_element(By.XPATH,'./td[1]/div/a/div[1]/div/div[2]/div[1]/span').text)
            rot_num_away_team.append(game_rows[game][0].find_element(By.XPATH,'./td[1]/div/a/div[1]/div/div[2]/div[3]').text)
            home_team_name.append(game_rows[game][0].find_element(By.XPATH,'./td[1]/div/a/div[2]/div/div[2]/div[1]').text)
            rot_num_home_team.append(game_rows[game][0].find_element(By.XPATH,'./td[1]/div/a/div[2]/div/div[2]/div[3]').text)

            ## First Row, Second Cell - Opening Run Line Odds
            away_team_runline_open.append(game_rows[game][0].find_element(By.XPATH,'./td[2]/div/div[1]/div[1]').text)
            away_team_runline_open_odds.append(game_rows[game][0].find_element(By.XPATH,'./td[2]/div/div[1]/div[2]/div').text)
            home_team_runline_open.append(game_rows[game][0].find_element(By.XPATH,'./td[2]/div/div[2]/div[1]').text)
            home_team_runline_open_odds.append(game_rows[game][0].find_element(By.XPATH,'./td[2]/div/div[1]/div[2]/div').text)

            ## First Row, Third Cell - Best Closing Run Line Odds
            try:
                away_team_runline_close.append(game_rows[game][0].find_element(By.XPATH,'./td[3]/div/div[1]/div/span[1]').text)
            except:
                away_team_runline_close.append(NaN)

            try:
                away_team_runline_close_odds.append(game_rows[game][0].find_element(By.XPATH,'./td[3]/div/div[1]/div/span[2]').text)
            except:
                away_team_runline_close_odds.append(NaN)

            try:
                home_team_runline_close.append(game_rows[game][0].find_element(By.XPATH,'./td[3]/div/div[2]/div/span[1]').text)
            except:
                home_team_runline_close.append(NaN)

            try:
                home_team_runline_close_odds.append(game_rows[game][0].find_element(By.XPATH,'./td[3]/div/div[2]/div/span[2]').text)
            except:
                home_team_runline_close_odds.append(NaN)

            ## Second Row, Second Cell - Opening ML Odds 
            away_team_moneyline_open.append(game_rows[game][1].find_element(By.XPATH,'./td[2]/div/div[1]/div[1]').text)
            home_team_moneyline_open.append(game_rows[game][1].find_element(By.XPATH,'./td[2]/div/div[2]/div[1]').text)

            ## Second Row, Third Cell - Best Closing ML Odds
            try:
                away_team_moneyline_close.append(game_rows[game][1].find_element(By.XPATH,'./td[3]/div/div[1]/div/span[1]').text)
            except:
                away_team_moneyline_close.append(NaN)
            try:
                home_team_moneyline_close.append(game_rows[game][1].find_element(By.XPATH,'./td[3]/div/div[2]/div/span[1]').text)
            except:
                home_team_moneyline_close.append(NaN)

            ## Third Row, Second Cell - Opening O/U and Odds
            over_open.append(game_rows[game][2].find_element(By.XPATH,'./td[2]/div/div[1]/div[1]').text)
            over_open_odds.append(game_rows[game][2].find_element(By.XPATH,'./td[2]/div/div[1]/div[2]/div').text)
            under_open.append(game_rows[game][2].find_element(By.XPATH,'./td[2]/div/div[2]/div[1]').text)
            under_open_odds.append(game_rows[game][2].find_element(By.XPATH,'./td[2]/div/div[2]/div[2]/div').text)

            ## Third Row, Third Cell - Best Closing O/U and Odds
            try:
                over_close.append(game_rows[game][2].find_element(By.XPATH,'./td[3]/div/div[1]/div/span[1]').text)
            except:
                over_close.append(NaN)
            
            try:
                over_close_odds.append(game_rows[game][2].find_element(By.XPATH,'./td[3]/div/div[1]/div/span[2]').text)
            except:
                over_close_odds.append(NaN)
            
            try:
                under_close.append(game_rows[game][2].find_element(By.XPATH,'./td[3]/div/div[2]/div/span[1]').text)
            except:
                under_close.append(NaN)
            
            try:
                under_close_odds.append(game_rows[game][2].find_element(By.XPATH,'./td[3]/div/div[2]/div/span[2]').text)
            except:
                under_close_odds.append(NaN)

        # Click the arrow to get the next days games
        try:
            driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[2]/div[2]/div[1]/button').click()
        except:
            print("Finished Scraping")
finally:
    driver.quit()

# Create the final data frame by combining the lists
len_df = pd.DataFrame(
    {'date':len(date),
    'rot_num_away_team':len(rot_num_away_team),
    'away_team_name':len(away_team_name),
    'rot_num_home_team':len(rot_num_home_team),
    'home_team_name':len(home_team_name),
    'away_team_runline_open':len(away_team_runline_open),
    'away_team_runline_open_odds':len(away_team_runline_open_odds),
    'home_team_runline_open':len(home_team_runline_open),
    'home_team_runline_open_odds':len(home_team_runline_open_odds),
    'away_team_runline_close':len(away_team_runline_close),
    'away_team_runline_close_odds':len(away_team_runline_close_odds),
    'home_team_runline_close': len(home_team_runline_close),
    'home_team_runline_close_odds':len(home_team_runline_close_odds),
    'away_team_moneyline_open':len(away_team_moneyline_open),
    'home_team_moneyline_open':len(home_team_moneyline_open),
    'away_team_moneyline_close':len(away_team_moneyline_close),
    'home_team_moneyline_close':len(home_team_moneyline_close),
    'over_open':len(over_open),
    'over_open_odds':len(over_open_odds),
    'under_open':len(under_open),
    'under_open_odds':len(under_open_odds),
    'over_close':len(over_close),
    'over_close_odds':len(over_close_odds),
    'under_close':len(under_close),
    'under_close_odds':len(under_close_odds)},
    index = [0]
    )

len_df.to_csv('list_lengths.csv', index=True)
print(len_df)

# Create the final data frame by combining the lists
df = pd.DataFrame(
    {'date':date,
    'rot_num_away_team':rot_num_away_team,
    'away_team_name':away_team_name,
    'rot_num_home_team':rot_num_home_team,
    'home_team_name':home_team_name,
    'away_team_runline_open':away_team_runline_open,
    'away_team_runline_open_odds':away_team_runline_open_odds,
    'home_team_runline_open':home_team_runline_open,
    'home_team_runline_open_odds':home_team_runline_open_odds,
    'away_team_runline_close':away_team_runline_close,
    'away_team_runline_close_odds':away_team_runline_close_odds,
    'home_team_runline_close': home_team_runline_close,
    'home_team_runline_close_odds':home_team_runline_close_odds,
    'away_team_moneyline_open':away_team_moneyline_open,
    'home_team_moneyline_open':home_team_moneyline_open,
    'away_team_moneyline_close':away_team_moneyline_close,
    'home_team_moneyline_close':home_team_moneyline_close,
    'over_open':over_open,
    'over_open_odds':over_open_odds,
    'under_open':under_open,
    'under_open_odds':under_open_odds,
    'over_close':over_close,
    'over_close_odds':over_close_odds,
    'under_close':under_close,
    'under_close_odds':under_close_odds
    })

df.to_csv('2022_MLB_BettingOdds.csv', index=False)
print(df)

# print("Away Team Name: ", away_team_name)
# print("Home Team Name: ", home_team_name)
# print("Away Team Rot Num: ", rot_num_away_team)
# print("Home Team Rot Num: ", rot_num_home_team)