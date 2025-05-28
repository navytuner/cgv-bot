from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from movie import Movie


class Theater:
    def __init__(self, areacode="01", theatercode="0013"):
        # Default theater: CGV Yongsan
        self.areacode = areacode
        self.theatercode = theatercode
        self.movies = []

    def _init_web_driver(self):
        chromeOptions = webdriver.ChromeOptions()
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=chromeOptions
        )
        return driver

    def _get_page_source(self, driver, date):
        url_base = f"http://www.cgv.co.kr/theaters/?theaterCode={self.theatercode}"
        url_target_date = f'a[href="./iframeTheater.aspx?areacode={self.areacode}&theatercode={self.theatercode}&date={date}&screencodes=&screenratingcode=&regioncode="]'

        # Switch to target date source
        driver.get(url_base)
        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, url_target_date))
        )
        link.click()

        # Switch to iframe and get page source
        iframe = driver.find_element(By.ID, "ifrm_movie_time_table")
        driver.switch_to.frame(iframe)
        return BeautifulSoup(driver.page_source, "html.parser")

    def _create_movie_obj(self, li):
        info_movie = li.select_one("div > div.info-movie")
        title = info_movie.select_one("a > strong").text.strip()
        genre = info_movie.select("i")[1].text.strip()
        runtime = info_movie.select("i")[2].text.strip()
        open_date = info_movie.select("i")[3].text.split()[0]
        movie = Movie(title, genre, runtime, open_date)

    def display_movies(self):
        for movie in self.movies:
            movie.display_showtimes()

    def fetch_movies(self, date):
        # Fetch page source
        driver = self._init_web_driver()
        soup = self._get_page_source(driver, date)

        sect_showtimes = soup.find("div", class_="sect-showtimes")
        ul = sect_showtimes.find("ul")

        for li in ul.find_all("li"):
            movie = self._create_movie_obj(li)

            halls = li.select("div > div.type-hall")
            for hall in halls:
                screen_type_span = hall.select_one("span.screentype")
                if screen_type_span:
                    screen_type = screen_type_span.select_one("span").text.strip()
                else:
                    # screen_type = hall.select("ul > li")[1].text.strip()
                    screen_type = "LASER"
                tot_seat = int(
                    hall.select("div.info-hall > ul > li")[2].text.split()[1][:-1]
                )

                timetbls = hall.select("div.info-timetable > ul > li")
                for timetbl in timetbls:
                    time = timetbl.select_one("em").text.strip()
                    timetbl_info = timetbl.select_one("a")
                    if timetbl_info:
                        remain_seat = int(timetbl_info["data-seatremaincnt"])
                    else:
                        remain_seat = 0
                    movie.insert_showtime(
                        date, screen_type, time, remain_seat, tot_seat
                    )


theater = Theater()
theater.fetch_movies("20250529")
theater.display_movies()
