from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time,random
import json


def process_player(index,player_name, team,url,driver):
    
    records = []
    driver.get(url)
    time.sleep(random.uniform(10,20))
    if index % 14 == 0:
        driver.refresh()
    
    driver.execute_script(f"window.scrollBy(0, {random.randint(200,1000)});")

    
    player_details_container= driver.find_element(By.CSS_SELECTOR, "div.ds-grid")
    player_details = player_details_container.find_elements(By.CSS_SELECTOR, ":scope > div") 
    details = {}

    for player_detail in player_details:
        try:
            label = player_detail.find_element(By.CSS_SELECTOR, "p").text.strip().lower()
            value_element = player_detail.find_element(By.CSS_SELECTOR, "p+span")

            if value_element:
                value = value_element.text.strip() 
                details[label] = value
        except Exception:
            continue
    
    try:
        player_description = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.ci-player-bio-content > p:not(:has(h2))")
                )
        ).text.strip()
    except Exception as e:
        player_description = ""
    
    image = driver.find_element(By.CSS_SELECTOR, f'img[alt^="{player_name.split()[0]}"]').get_attribute("src")

    record = {
        "name": player_name,
        "team": team,
        "battingStyle": details.get('batting style'),
        "bowlingStyle": details.get('bowling style'),
        "playingRole": details.get('playing role'),
        "description": player_description,
        "image_url": image
    }

    records.append(record)

    
    return records

def main():

    player_info = []
    driver = uc.Chrome()
    with open('t20_scraped_data/player_url_cleaned.json') as f:
        players = json.load(f)
    
    
    for index, player in enumerate(players, start=1):
        player_name, team, url = player['playerName'],player['team'],player['url']
        print(index, player_name)

        try:
            player_info.extend(process_player(index,player_name,team,url,driver))
        
        except Exception as e:
            print(f'{player_name} : {e}')
        
        if index % 20 == 0:
            driver.quit()
            delay = random.uniform(5,15)
            time.sleep(delay)
            driver = uc.Chrome()

    with open("t20_scraped_data/player_summary.json", 'w', encoding='utf-8') as f:
        json.dump(player_info, f, indent=4,ensure_ascii=False)

    driver.quit()


if __name__ == "__main__":
    
    main()
    