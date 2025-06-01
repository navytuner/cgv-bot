from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from .movie import Movie


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
        href_css_selector = f'a[href*="date={date}"]'

        driver.get(url_base)
        wait = WebDriverWait(driver, 15)

        # Find link with given date and click it
        wait.until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrm_movie_time_table"))
        )
        link = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, href_css_selector))
        )
        link.click()

        # Switch to new iframe with given date
        driver.switch_to.default_content()
        wait.until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrm_movie_time_table"))
        )

        return BeautifulSoup(driver.page_source, "html.parser")

    def display_movies(self):
        for movie in self.movies:
            movie.display_movieinfo()
            movie.display_showtimes()
            print()

    def get_movie(self, title_search):
        for movie in self.movies:
            if title_search in movie.get_title():
                return movie

    def fetch_movies(self, date):
        # Fetch page source
        driver = self._init_web_driver()
        soup = self._get_page_source(driver, date)

        sect_showtimes = soup.find("div", class_="sect-showtimes")
        ul = sect_showtimes.find("ul")
        li_list = ul.find_all("li", recursive=False)

        for _, li in enumerate(li_list):
            info_movie = li.select_one("div.info-movie")

            title = info_movie.select_one("a > strong").text.strip()
            genre = info_movie.select("i")[1].text.strip()
            runtime = info_movie.select("i")[2].text.strip()[:-1]
            open_date = info_movie.select("i")[3].text.split()[0]
            movie = Movie(title, genre, runtime, open_date)

            halls = li.select("div.type-hall")
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
                    # print(timetbl_info)
                    if timetbl_info and timetbl_info.has_attr("data-seatremaincnt"):
                        # print(timetbl_info)
                        remain_seat = int(timetbl_info.get("data-seatremaincnt"))
                    else:
                        remain_seat = 0
                    movie.insert_showtime(
                        date, screen_type, time, remain_seat, tot_seat
                    )
            self.movies.append(movie)
        driver.quit()
        print("fetch movies successfully")


# theater = Theater()
# theater.fetch_movies("20250602")
# theater.display_movies()
