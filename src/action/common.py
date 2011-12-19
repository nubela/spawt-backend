import datetime

def _get_2_weeks_date_before():
    now = datetime.datetime.now() 
    diff = datetime.timedelta(weeks=2)
    return (now - diff)