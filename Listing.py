import dbm
import shelve
class Listing:
    count_id = 0
    try:
        db = shelve.open('listing', 'c')
    except dbm.error:
        db = shelve.open('listing', 'n')
    try:
        count_id = db['count_id']
    except:
        pass
    db.close()

    def __init__(self, title, brand, category, expiry_date, location, description, filename):
        Listing.count_id += 1
        self.__listing_id = Listing.count_id
        self.__title = title
        self.__brand = brand
        self.__category = category
        self.__expiry_date = expiry_date
        self.__location = location
        self.__description = description
        self.__filename = filename

    # accessor methods

    def get_filename(self):
        return self.__filename
    def get_listing_id(self):
        return self.__listing_id

    def get_title(self):
        return self.__title

    def get_brand(self):
        return self.__brand

    def get_category(self):
        return self.__category


    def get_expiry_date(self):
        return self.__expiry_date

    def get_location(self):
        return self.__location

    def get_description(self):
        return self.__description



    # mutator methods
    def set_filename(self, filename):
        self.__filename = filename

    def set_listing_id(self, listing_id):
        self.__listing_id = listing_id

    def set_title(self, title):
        self.__title = title

    def set_brand(self, brand):
        self.__brand = brand

    def set_category(self, category):
        self.__category = category


    def set_expiry_date(self, expiry_date):
        self.__expiry_date = expiry_date

    def set_location(self, location):
        self.__location = location

    def set_description(self, description):
        self.__description = description
