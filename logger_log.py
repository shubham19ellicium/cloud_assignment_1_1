from datetime import datetime

def log_info(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_log_entry = f"{timestamp}: INFO : {message}\n"
    return new_log_entry

def log_error(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_log_entry = f"{timestamp}: ERROR : {message}\n"
    return new_log_entry

def log_exception(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_log_entry = f"{timestamp}: EXCEPTION : {message}\n"
    return new_log_entry

def log_critical(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_log_entry = f"{timestamp}: CRITICAL : {message}\n"
    return new_log_entry

def log_warning(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_log_entry = f"{timestamp}: WARNING : {message}\n"
    return new_log_entry

