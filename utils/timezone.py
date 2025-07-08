from datetime import datetime
import pytz

def jst_now():
    JST = pytz.timezone("Asia/Tokyo")
    return datetime.now(JST)