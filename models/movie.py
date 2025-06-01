from .showtime import Showtime


class Movie:
    def __init__(self, title, genre, runtime, open_date):
        self.title = title
        self.genre = genre
        self.runtime = runtime
        self.open_date = open_date
        self.showtimes = []

    def get_title(self):
        return self.title

    def get_genre(self):
        return self.genre

    def get_runtime(self):
        return self.runtime

    def get_open_date(self):
        return self.open_date

    def get_showtimes(self):
        return self.showtimes

    def insert_showtime(self, date, screen_type, time, remain_seat, tot_seat):
        showtime = Showtime(date, screen_type, time, remain_seat, tot_seat)
        self.showtimes.append(showtime)

    def display_movieinfo(self):
        print(f"{self.title}")
        print(f"{self.genre} / {self.runtime}분 / {self.open_date} 개봉")

    def display_showtimes(self):
        for showtime in self.showtimes:
            showtime.display_showtime()

    def get_showtime_msg(self):
        msg = f"{self.title}\n"
        msg += f"{self.genre} / {self.runtime}분 / {self.open_date} 개봉\n\n"

        for showtime in self.showtimes:
            msg += showtime.get_showtime_info() + "\n"
        return msg
