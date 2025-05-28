class Showtime:
    def __init__(self, date, screen_type, time, remain_seat, tot_seat):
        self.date = date
        self.screen_type = screen_type
        self.time = time
        self.remain_seat = remain_seat
        self.tot_seat = tot_seat

    def display(self):
        print(f"{self.date} {self.screen_type}")
        print(f"{self.time} {self.remain_seat} / {self.tot_seat}\n")

    def get_date(self):
        return self.date

    def get_time(self):
        return self.time

    def get_remain_seat(self):
        return self.remain_seat

    def get_tot_seat(self):
        return self.tot_seat
