from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time
import json
    
def process_match(url, driver):

    driver.get(url)
    time.sleep(6)
    team_name_elements = driver.find_elements(By.CSS_SELECTOR, "span.ds-text-header-5")
    all_tables_elements = driver.find_elements(By.CSS_SELECTOR, "div>table")

    all_batting = []
    all_bowling = []
    all_player_url = []

    team1 = team_name_elements[0].text
    team2 = team_name_elements[1].text
    match = f"{team1} Vs {team2}"

    for i in range(0, len(all_tables_elements), 2):
        batting_table_element = all_tables_elements[i]
        bowling_table_element = all_tables_elements[i+1]

        if i == 0:
            batting_team = team1
            bowling_team = team2
        else:
            batting_team = team2
            bowling_team = team1

        batting_data , player_url = parse_batting_table(batting_table_element, match, batting_team)
        all_batting.extend(batting_data)
        all_player_url.extend(player_url)

        bowling_data , player_url = parse_bowling_table(bowling_table_element, match,bowling_team)
        all_bowling.extend(bowling_data)
        all_player_url.extend(player_url)

    
    return all_batting , all_bowling , all_player_url

def parse_batting_table(table_element, match, team_name):
    rows = table_element.find_elements(By.CSS_SELECTOR, "tbody tr:not(.ds-hidden)")
    records = []
    player_urls = []
    batting_pos = 1
    for row in rows:
        col_data = row.find_elements(By.CSS_SELECTOR, "td")        

        if col_data[0].text.lower() == "extras":
            break

        player_url_element = col_data[0].find_element(By.TAG_NAME, "a")
        player_name = player_url_element.text.strip()

        record = {
            "match": match,
            "teamInnings": team_name,
            "battingPos": batting_pos,
            "batsmanName": player_name,
            "dismissal": col_data[1].text.strip(),            
            "runs": col_data[2].text.strip(),
            "balls": col_data[3].text.strip(),
            "minutes":col_data[4].text.strip(),
            "4s":col_data[5].text.strip(),
            "6s": col_data[6].text.strip(),
            "SR": col_data[7].text.strip()
        }

        url = {
            "playerName" : player_name,
            "team": team_name,
            "url" : player_url_element.get_attribute("href")
        }
        
        records.append(record)
        player_urls.append(url)
        batting_pos += 1
    
    return records, player_urls


def parse_bowling_table(table, match, team_name):
    rows = table.find_elements(By.CSS_SELECTOR, "tbody tr:not(.ds-hidden)")
    records = []
    player_urls = []

    for row in rows:
        cols_data = row.find_elements(By.CSS_SELECTOR, "td")

        player_url_element = cols_data[0].find_element(By.TAG_NAME, "a")
        player_name = player_url_element.text.strip()

        record = {
            "match": match,
            "bowlingTeam": team_name,
            "bowlerName": player_name,
            "overs": cols_data[1].text.strip(),
            "maiden": cols_data[2].text.strip(),
            "runs": cols_data[3].text.strip(),
            "wickets": cols_data[4].text.strip(),
            "economy": cols_data[5].text.strip(),
            "0s": cols_data[6].text.strip(),
            "wides": cols_data[7].text.strip(),
            "noBalls": cols_data[8].text.strip()
        }

        url = {
            "playerName" : player_name,
            "team": team_name,
            "url" : player_url_element.get_attribute("href")
        }
        records.append(record)
        player_urls.append(url)
    
    return records,player_urls

def main():

    driver = uc.Chrome()

    with open("t20_scraped_data/match_url.json", "r") as f:
        matches = json.load(f)
    
    all_batting = []
    all_bowling = []
    all_player = []

    for match in matches:
        url = match["scorecard_url"]

        try:

            batting_data, bowling_data, player_data = process_match(url, driver)

            all_batting.extend(batting_data)
            all_bowling.extend(bowling_data)
            all_player.extend(player_data)

        except Exception as e:

            print(e)

    with open("t20_scraped_data/batting_summary.json", 'w', encoding='utf-8') as f:
        json.dump(all_batting, f, indent=4,ensure_ascii=False)

    with open("t20_scraped_data/bowling_summary.json", 'w', encoding='utf-8') as f:
        json.dump(all_bowling, f, indent=4,ensure_ascii=False)

    with open("t20_scraped_data/player_url.json", 'w', encoding='utf-8') as f:
        json.dump(all_player, f, indent=4,ensure_ascii=False)

    driver.quit()    


if __name__ == "__main__":
    main()