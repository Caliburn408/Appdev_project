import dbm
import shelve


class BaseClass:
    try:
        db = shelve.open('base', 'c')
    except dbm.error:
        db = shelve.open('base', 'n')
    try:
        count_id = db['count_id']
    except:
        db['count_id'] = 0
        count_id = db['count_id']
    db.close()
