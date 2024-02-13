import datetime

class Helper:
    def __init__(self):
        pass

    def convert_timestamp_datetime(self, unix_timestamp):
        date_time = datetime.datetime.fromtimestamp(int(unix_timestamp))
        return date_time.strftime("%Y-%m-%d %H:%M:%S")