from datetime import date, timedelta, datetime


def get_start_of_week_datetime():
    current_date = date.today()
    start_of_week = current_date - timedelta(days= current_date.weekday())
    start_of_week_dt = datetime(start_of_week.year, start_of_week.month, start_of_week.day)
    return str(start_of_week_dt)


def get_current_day_name():
    days = {0:"Monday", 1:"Tuesday", 2:"Wednesday", 3:"Thursday", 4:"Friday", 5:"Saturday", 6:"Sunday"}
    current_date = date.today()
    return days[current_date.weekday()]
