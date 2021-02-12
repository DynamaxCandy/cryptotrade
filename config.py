import time
API_key = ''

Secret_Key = ''

DB_FILE = 'crypt.db'

def epoch2human(epoch):
    return time.strftime('%Y-%m-%d %H:%M:%S',
        time.localtime(int(epoch)/1000))