import shelve
from BaseClass import BaseClass

class Dib(BaseClass):
    def __init__(self, user_id, listing_id):
        BaseClass.count_id += 1
        self.__dib_id = Dib.count_id
        self.__user_id = user_id
        self.__listing_id = BaseClass.count_id

    def get_dib_id(self):
        return self.__dib_id

    def get_user_id(self):
        return self.__user_id

    def get_listing_id(self):
        return self.__listing_id
