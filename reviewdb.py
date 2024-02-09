import shelve

class Review:

    count_id = 0
    db = shelve.open('review_id')
    try:
        count_id = db['count_id']
    except:
        pass
    db.close()


    def __init__(self, donor_id, item_id, dibber_id, rating, review):
        Review.count_id += 1
        self.__id = Review.count_id
        db = shelve.open('review_id')
        db['count_id'] = Review.count_id
        db.close()
        self.__donor_id = donor_id
        self.__dibber_id = dibber_id
        self.__rating = rating
        self.__review = review
        self.__item_id = item_id


    def get_id(self):
        return self.__id

    def get_donor_id(self):
        return self.__donor_id

    def get_dibber_id(self):
        return self.__dibber_id

    def get_rating(self):
        return self.__rating

    def get_review(self):
        return self.__review
    def get_item_id(self):
        return self.__item_id



        # mutator methods

    def set_donor_id(self, donor_id):
        self.__donor_id = donor_id

    def set_dibber_id(self, dibber_id):
        self.__dibber_id = dibber_id

    def set_rating(self, rating):
        self.__rating = rating

    def set_review(self, review):
        self.__review = review
    def set_item_id(self, item_id):
        self.__item_id = item_id



