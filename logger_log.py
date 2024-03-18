from datetime import datetime
import pytz

def get_local_time():
    utc_now = datetime.now(pytz.utc)
    local_tz = pytz.timezone('Asia/Kolkata')
    local_time = utc_now.astimezone(local_tz)

    formatted_time = local_time.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time

def log_info(message):
    timestamp = get_local_time()
    new_log_entry = f"{timestamp}: INFO : {message}\n"
    return new_log_entry

def log_error(message):
    timestamp = get_local_time()
    new_log_entry = f"{timestamp}: ERROR : {message}\n"
    return new_log_entry

def log_exception(message):
    timestamp = get_local_time()
    new_log_entry = f"{timestamp}: EXCEPTION : {message}\n"
    return new_log_entry

def log_critical(message):
    timestamp = get_local_time()
    new_log_entry = f"{timestamp}: CRITICAL : {message}\n"
    return new_log_entry

def log_warning(message):
    timestamp = get_local_time()
    new_log_entry = f"{timestamp}: WARNING : {message}\n"
    return new_log_entry

