from datetime import datetime, timedelta


time_slot_map = {
    0: {'start': '08:00:00', 'end': '08:45:00'},
    1: {'start': '08:55:00', 'end': '09:40:00'},
    2: {'start': '10:00:00', 'end': '10:45:00'},
    3: {'start': '10:55:00', 'end': '11:40:00'},
    4: {'start': '14:00:00', 'end': '14:45:00'},
    5: {'start': '14:55:00', 'end': '15:40:00'},
    6: {'start': '16:00:00', 'end': '16:45:00'},
    7: {'start': '16:55:00', 'end': '17:40:00'},
    8: {'start': '19:00:00', 'end': '19:45:00'},
    9: {'start': '19:55:00', 'end': '20:40:00'},
}

slot_time_map = {
    "08:00:00": 0,
    "08:55:00": 1,
    "10:00:00": 2,
    "10:55:00": 3,
    "14:00:00": 4,
    "14:55:00": 5,
    "16:00:00": 6,
    "16:55:00": 7,
    "19:00:00": 8,
    "19:55:00": 9
}


def add_time(date_str, time_str):

    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    time_obj = datetime.strptime(time_str, '%H:%M:%S')

    time_delta = timedelta(hours=time_obj.hour, minutes=time_obj.minute, seconds=time_obj.second)

    combined_date = date_obj + time_delta

    return combined_date


def is_same_date(time_str1, time_str2, format_str1='%Y-%m-%d', format_str2='%Y-%m-%d %H:%M:%S'):
    datetime1 = datetime.strptime(time_str1, format_str1)
    datetime2 = datetime.strptime(time_str2, format_str2)
    return datetime1.date() == datetime2.date()

def get_time_slot(time_str, format_str='%Y-%m-%d %H:%M:%S'):

    time_obj = datetime.strptime(time_str, format_str)
    return slot_time_map[str(time_obj.strftime("%H:%M:%S"))]

def get_current_date(format_str='%Y-%m-%d'):
    return str(datetime.today().strftime(format_str))

def get_date_time(time_str, origin_format = "%Y-%m-%d %H:%M:%S",date_format='%Y-%m-%d',time_format='%H:%M:%S'):
    time_obj = datetime.strptime(time_str, origin_format)
    date_obj = time_obj.strftime(date_format)
    time_obj = time_obj.strftime(time_format)
    return str(date_obj), str(time_obj)
