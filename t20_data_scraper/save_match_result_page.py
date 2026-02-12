from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time
import json

#---------------CONFIG-------------------------------
URL = "https://www.espncricinfo.com/records/tournament/team-match-results/icc-men-s-t20-world-cup-2024-15946"

# # Start browser
driver = uc.Chrome()

# ---------- FETCH ----------
driver.get(URL)

# Give the page time to fully load
time.sleep(6)
# To store the match summary
match_summary = []
# To store the scorecard URL
match_url = []

#Selecting each rows of the match and storing it as a list
rows = driver.find_elements(By.CSS_SELECTOR, "table>tbody>tr")

# Looping through the list and storing individual data in a dict
for row in rows:
    table_data = row.find_elements(By.TAG_NAME, "td")

    scorecard_element = table_data[6].find_element(By.TAG_NAME, "a")
    match_summary.append({
        "team1": table_data[0].text,
        "team2" : table_data[1].text,
        "winner":table_data[2].text,
        "margin":table_data[3].text,
        "ground":table_data[4].text,
        "matchDate":table_data[5].text,
        "scorecard":scorecard_element.text,
    })

    match_url.append({
        "scorecard":scorecard_element.text,
        "scorecard_url":scorecard_element.get_attribute("href")
    })

# Storing it as a JSON file
with open("t20_scraped_data/match_summary.json", 'w', encoding='utf-8') as f:
    json.dump(match_summary, f, indent=4,ensure_ascii=False)

with open("t20_scraped_data/match_url.json", "w", encoding='utf-8') as f:
    json.dump(match_url,f,indent=4,ensure_ascii=False)
  
driver.quit()


