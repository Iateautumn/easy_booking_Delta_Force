from datetime import datetime, timedelta


time_slot_map = {
    0: {'start': '08:00:00', 'end': '08:45:00'},
    1: {'start': '08:45:00', 'end': '09:40:00'},
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
    "8:00:00": 0,
    "8:55:00": 1,
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