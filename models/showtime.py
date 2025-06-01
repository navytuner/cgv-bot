class Showtime:
    def __init__(self, date, screen_type, time, remain_seat, tot_seat):
        self.date = date
        self.screen_type = screen_type
        self.time = time
        self.remain_seat = remain_seat
        self.tot_seat = tot_seat

    def display_showtime(self):
        print(
            f"{self.date} {self.screen_type} {self.time} {self.remain_seat}석 / {self.tot_seat}석"
        )

    def get_showtime_info(self):
        date = f"{int(self.date[4:6])}월{int(self.date[6:8])}일"
        return f"{date} {self.screen_type} {self.time} {self.remain_seat}석 / {self.tot_seat}석"

    def get_date(self):
        return self.date

    def get_time(self):
        return self.time

    def get_remain_seat(self):
        return self.remain_seat

    def get_tot_seat(self):
        return self.tot_seat
