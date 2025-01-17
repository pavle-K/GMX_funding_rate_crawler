from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
from config.configure_driver import configure_driver

def GMX():
    print("Starting GMX data collection")
    all_data = []
    
    try:
        # Initial driver setup
        driver = configure_driver()
        driver.get("https://app.gmx.io/#/trade")
        time.sleep(3)

        # Get initial pair data
        initial_pair = driver.find_element(By.CSS_SELECTOR, 'div.SelectorBase-button').text
        initial_rates = driver.find_elements(By.CSS_SELECTOR, "span.flex.flex-row.items-center.gap-4")

        # Get list of all pairs
        button_selector = 'div.SelectorBase-button'
        button = driver.find_elements(By.CSS_SELECTOR, button_selector)[0]
        button.click()
        time.sleep(1)
        
        elements = driver.find_elements(By.CSS_SELECTOR, "tr.group\\/row.cursor-pointer")
        pairs_data = []
        
        for element in elements:
            info = element.text.split('\n')
            pairs_data.append({
                'pair': info[0],
                'details': info[1:] if len(info) > 1 else []
            })
            
        print(f"Found {len(pairs_data)} trading pairs")

        # Process each pair one by one
        for i, pair_data in enumerate(pairs_data):
            try:
                # Skip if it's the initial pair
                if pair_data['pair'] == initial_pair:
                    continue
                
                # Click dropdown
                button = driver.find_elements(By.CSS_SELECTOR, button_selector)[0]
                button.click()
                time.sleep(1)
                
                # Find and click the pair
                current_elements = driver.find_elements(By.CSS_SELECTOR, "tr.group\\/row.cursor-pointer")
                for element in current_elements:
                    if element.text.startswith(pair_data['pair']):
                        element.click()
                        time.sleep(2)
                        break
                
                # Get rates
                rate_elements = driver.find_elements(By.CSS_SELECTOR, "span.flex.flex-row.items-center.gap-4")
                if len(rate_elements) >= 2:
                    data = {
                        'pair': pair_data['pair'],
                        'long_position_rate': rate_elements[0].text,
                        'short_position_rate': rate_elements[1].text
                    }
                    all_data.append(data)
                    print(f"Collected data for {pair_data['pair']} ({i+1}/{len(pairs_data)})")
                    
                    # Update JSON file after each successful collection
                    with open('output/gmx_funding_rates_progress.json', 'w') as f:
                        json.dump(all_data, f, indent=4)
                
            except Exception as e:
                print(f"Error collecting data for {pair_data['pair']}: {str(e)}")
                continue

        driver.quit()
        
        # Final data is already saved in progress file
        print(f"\nCompleted! Collected data for {len(all_data)} pairs")
        return all_data

    except Exception as e:
        print(f"Error in main process: {str(e)}")
        if 'driver' in locals():
            driver.quit()
        return None

if __name__ == "__main__":
    data = GMX()
    if data:
        print("Data collection complete!")