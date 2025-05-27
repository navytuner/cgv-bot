from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

class Theater:
    def __init__(self, areaCode='01', theaterCode='0013', date='2025.05.06'):
        self.areaCode = areaCode
        self.theaterCode = theaterCode
        self.date = date
        self.movies = []

    def get_date(self):
        return self.date

    def get_movie(self, title):
        for movie in self.movies:
            if (movie["title"] == title):
                return movie
        return None
    
    def fetch_movie(self):
        # Execute browser
        chromeOptions = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chromeOptions)

        # Fetch page source
        url = f"http://www.cgv.co.kr/theaters/?areacode={self.areaCode}&theaterCode={self.theaterCode}&date={self.date}#menu"
        driver.get(url)
        iframe = driver.find_element(By.ID, "ifrm_movie_time_table")
        driver.switch_to.frame(iframe)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Select only IMAX movies
        imax = soup.select('span.imax')
        for item in imax:
            colTimes = item.find_parent('div', class_='col-times')
            infoMovie = colTimes.select_one('div.info-movie')
            typeHall = item.find_parent('div', class_='type-hall')
            infoHall = typeHall.select_one('div.info-hall')
            infoTimetable = typeHall.select_one('div.info-timetable')

            # movie info
            title = infoMovie.select_one('a > strong').text.strip()
            openDate = infoMovie.select('i')[3].text.split()[0]
            totSeat = infoHall.select('li')[2].text.split()[1][:-1]
            movie = {
                "title": title,
                "openDate": openDate,
                "totSeat": totSeat,
                "plays": []
            }

            plays = typeHall.select_one('div.info-timetable').select('a')
            for play in plays:
                time = play['data-playstarttime'][:2] + ':' + play['data-playstarttime'][2:]
                remainSeat = play['data-seatremaincnt']

                # append play info
                movie["plays"].append({
                    "time": time,
                    "remainSeat": remainSeat, 
                })

            # Insert movie info
            self.movies.append(movie)