from selenium import webdriver
import time
from csv import writer
from selenium.webdriver.firefox.options import Options as firefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import os
import alive_progress
from alive_progress import alive_bar



def song_scrapper(url):
    """
    Scraps the global top 20 songs from the spotify playlist.
    Currently works only for spotify website.
    
    url (string): urls pointing to spotify playlist
    """
    options = firefoxOptions()
    options.add_argument('--headless')
    options.set_preference("browser.tabs.warnOnClose", False)
    options.set_preference("dom.disable_beforeunload", True)
    service = Service(r"/geckodriver/geckodriver.exe")
    driver = webdriver.Firefox(options=options,  service=service)
    driverversion = driver.capabilities['moz:geckodriverVersion']
    browserversion = driver.capabilities['browserVersion']
    print('\n')
    print('Mounting drivers...')
    print(f'Driver version: gecko-{driverversion}')
    print(f'browser found: {driver.name}-{browserversion}')
    driver.get(url)
    time.sleep(10)

    songs = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((
        By.CSS_SELECTOR, '.h4HgbO_Uu1JYg5UGANeQ.wTUruPetkKdWAR1dd6w4')))

    songs = songs[0:20]
    
    
    
    with open('spotify.csv', 'w', encoding='utf8', newline='') as f:
        csv_writer = writer(f)
        header = ['Rank', 'Title', 'Artists', 'Album', 'Date', 'Track length']
        if f.tell() == 0:
            csv_writer.writerow(header)
        
        with alive_bar(len(songs),bar='blocks', title='Scrapping:', spinner= 'waves' ) as bar:    
            for song in songs:
                song = song.text.split('\n')
                Rank = song[0]
                Title = song[1]
                Artists = song[2]
                Album = song[3]
                Date = song[4]
                Track_length = song[5]
                info = [Rank, Title, Artists, Album, Date, Track_length]
                csv_writer.writerow(info) 
                bar()                            
    print('\x1b[0;32;40m' + 'Done Scrapping.' + '\x1b[0m')
    print('Driver dismounted.')
    print('Firefox processes killed.')
    print('\n')
    driver.quit()
    # os.system('cmd /k "taskkill /F /IM firefox.exe /T"')       
