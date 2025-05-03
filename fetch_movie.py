from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests

# Execute Chrome
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Theater variables
areacode = '01'
theaterCode = '0013'
date = '20250503'

# connect cgv iframe
url = f"http://www.cgv.co.kr/theaters/?areacode={areacode}&theaterCode={theaterCode}&date={date}#menu"
driver.get(url)
iframe = driver.find_element(By.ID, "ifrm_movie_time_table")
driver.switch_to.frame(iframe)

soup = BeautifulSoup(driver.page_source, 'html.parser')

# Select only imax movies
imax = soup.select('span.imax')
for item in imax:
    col_times = item.find_parent('div', class_='col-times')
    info_movie = col_times.select_one('div.info-movie')
    title = info_movie.select_one('a > strong').text.strip()
    open_date = ' '.join(info_movie.select('i')[3].text.split())
    print(title)
    print(open_date)

    timetable = item.find_parent('div', class_='type-hall').select_one('div.info-timetable')
    movies = timetable.select('a')
    for movie in movies:
        time = movie['data-playstarttime']
        seat = movie['data-seatremaincnt']
        print(f"start time: {time[:2] + ':' + time[2:]}")
        print(f"# of seats: {seat}")
        