from showtime import Showtime


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

    def insert_showtime(self, date, screen_type, time, remain_seat, tot_seat):
        showtime = Showtime(date, screen_type, time, remain_seat, tot_seat)
        self.showtimes.append(showtime)

    def display_showtimes(self):
        for showtime in self.showtimes:
            showtime.display()
