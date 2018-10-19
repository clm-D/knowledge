
import random
from datetime import datetime

def get_order_sn():
    sn = ''
    s = '1234567890asdfghjklpoiuytrewqzxcvbnm'
    for i in range(10):
        sn += random.choice(s)
    sn += datetime.now().strftime('%Y%m%d%H%M%S')
    return sn