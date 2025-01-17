from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path 
import os
import shutil

def configure_driver():
    # Set environment variables first
    os.environ['WDM_LOCAL'] = '1'
    os.environ['WDM_CACHE_DIR'] = os.path.dirname(os.path.abspath(__file__))
    
    wd_path = os.getcwd().replace("\\","/")
    driver_path = 'chromedriver.exe' if os.name == 'nt' else 'chromedriver'
    
    # Check if chromedriver exists
    if not os.path.exists(os.path.join(wd_path, driver_path)):
        print("Chromedriver not found. Downloading...")
        path = ChromeDriverManager().install()
        service = Service(path)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        shutil.move(path, os.path.join(wd_path, driver_path))
        return driver

    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(options=chrome_options, service=service)
        return driver
    except Exception as e:
        if "Current browser version" in str(e) or "This version of ChromeDriver only supports" in str(e):
            print("ERROR: Chromedriver outdated. Updating...")
            
            # Download and install the new ChromeDriver
            path = ChromeDriverManager().install()
            service = Service(path)
            driver = webdriver.Chrome(service=service, options=chrome_options)

            # Remove the old chromedriver and fetch the new one
            if os.path.exists(os.path.join(wd_path, driver_path)):
                os.remove(os.path.join(wd_path, driver_path))
            shutil.move(path, os.path.join(wd_path, driver_path))

            return driver
        else:
            print(e)
            raise