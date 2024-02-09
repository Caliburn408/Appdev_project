import os

from Dib import Dib
from reviewdb import Review
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from Forms import CreateUserForm, CreateListingForm, LoginForm, CreateReviewForm
from werkzeug.utils import secure_filename
from geopy.distance import geodesic
import shelve, User, Listing, os, bcrypt
import cgitb

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for sessions

UPLOAD_FOLDER = '/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


upload_dir = os.path.join(os.path.dirname(__file__), 'static/uploads')
if not os.path.exists(upload_dir):
   os.mkdir(upload_dir)

app.config['UPLOAD_FOLDER'] = upload_dir


@app.route('/listings')
def listings():
    with shelve.open('listing.db') as db:
        listings = list(db.values())
    return jsonify(listings)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        username = login_form.username.data
        password = login_form.password.data

        # Authenticate user
        users_dict = {}
        db = shelve.open('user', 'r')
        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from user.db.")
        db.close()

        found_user = None
        for user in users_dict.values():
            if user.get_username() == username and user.get_password() == password:
                found_user = user
                break

        if found_user:
            session['user_id'] = found_user.get_user_id()
            return redirect(url_for('yourhome'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', form=login_form, error=error)

    return render_template('login.html', form=login_form)


@app.route('/yourhome')
def yourhome():
    listing_dict = {}
    db = shelve.open('listing', 'r')
    try:
        listing_dict = db['listing']
    except:
        pass
    db.close()

    listing_list = []
    for key in listing_dict:
        listing = listing_dict.get(key)
        listing_list.append(listing)

    return render_template('yourhome.html', count=len(listing_list), listing_list=listing_list)



@app.route('/retrieveListing')
def retrieve_listing():
    listing_dict = {}
    db = shelve.open('listing', 'r')
    try:
        listing_dict = db['listing']
    except:
        pass
    db.close()

    listing_list = []
    for key in listing_dict:
        listing = listing_dict.get(key)
        listing_list.append(listing)

    return render_template('retrieveListing.html', count=len(listing_list), listing_list=listing_list)

@app.route('/retrieveUsers')
def retrieve_users():
    users_dict = {}
    db = shelve.open('user', 'r')
    try:
        users_dict = db['Users']
    except:
        pass
    db.close()

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template('retrieveUsers.html', count=len(users_list), users_list=users_list)

@app.route('/')
def home():
    listing_dict = {}
    db = shelve.open('listing', 'r')
    try:
        listing_dict = db['listing']
    except:
        pass
    db.close()

    listing_list = []
    for key in listing_dict:
        listing = listing_dict.get(key)
        listing_list.append(listing)

    return render_template('home.html', count=len(listing_list), listing_list=listing_list)

@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')

@app.route('/createUser', methods=['GET', 'POST'])
def create_user():
    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        db = shelve.open('user', 'c')
        
        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from user.db.")

            password = create_user_form.password.data.encode('utf-8')
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        user = User.User(create_user_form.first_name.data, create_user_form.last_name.data, create_user_form.gender.data, create_user_form.username.data, create_user_form.email.data, create_user_form.password.data)
        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict

        db.close()

        return redirect(url_for('retrieve_users'))
    return render_template('createUser.html', form=create_user_form)


@app.route('/createListing', methods=['GET', 'POST'])
def create_listing():
    create_listing_form = CreateListingForm(request.form)
    if request.method == 'POST' and create_listing_form.validate():
        listing_dict = {}
        db = shelve.open('listing', 'c')

        try:
            listing_dict = db['listing']
        except:
            print("Error in retrieving Listings from listing.db.")

        # Get the uploaded file
        file = request.files['photo']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        listing = Listing.Listing(create_listing_form.title.data, create_listing_form.brand.data,
                                  create_listing_form.category.data, create_listing_form.expiry_date.data,
                                  create_listing_form.location.data, create_listing_form.description.data,
                                  filename)
        listing_dict[listing.get_listing_id()] = listing
        db['listing'] = listing_dict

        db.close()

        return redirect(url_for('retrieve_listing'))
    return render_template('createListing.html', form=create_listing_form)



@app.route('/updateUser/<int:user_id>/', methods=['GET', 'POST'])
def update_user(user_id):

    update_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('user', 'c')
        users_dict = db['Users']

        user = users_dict.get(user_id)
        user.set_first_name(update_user_form.first_name.data)
        user.set_last_name(update_user_form.last_name.data)
        user.set_gender(update_user_form.gender.data)
        user.set_username(update_user_form.username.data)
        user.set_email(update_user_form.email.data)
        user.set_password(update_user_form.password.data)

        db['Users'] = users_dict
        db.close()

        user = users_dict.get(user_id)
        update_user_form.first_name.data = user.get_first_name()
        update_user_form.last_name.data = user.get_last_name()
        update_user_form.gender.data = user.get_gender()
        update_user_form.username.data = user.get_username()
        update_user_form.email.data = user.get_email()
        update_user_form.password.data = user.get_password()
        return redirect(url_for('retrieve_users'))
    else:

        return render_template('updateUser.html', form=update_user_form)



@app.route('/updateListing/<int:listing_id>/', methods=['GET', 'POST'])
def update_listing(listing_id):
    update_listing_form = CreateListingForm(request.form)
    if request.method == 'POST' and update_listing_form.validate():
        listing_dict = {}
        db = shelve.open('listing', 'c')
        listing_dict = db['listing']

        listing = listing_dict.get(listing_id)
        listing.set_title(update_listing_form.title.data)
        listing.set_brand(update_listing_form.brand.data)
        listing.set_category(update_listing_form.category.data)
        listing.set_expiry_date(update_listing_form.expiry_date.data)
        listing.set_location(update_listing_form.location.data)
        listing.set_description(update_listing_form.description.data)

        db['listing'] = listing_dict
        db.close()

        return redirect(url_for('retrieve_listing'))
    else:
        listing_dict = {}
        db = shelve.open('listing', 'c')
        listing_dict = db['listing']
        db.close()

        listing = listing_dict.get(listing_id)
        update_listing_form.title.data = listing.get_title()
        update_listing_form.brand.data = listing.get_brand()
        update_listing_form.category.data = listing.get_category()
        update_listing_form.expiry_date.data = listing.get_expiry_date()
        update_listing_form.location.data = listing.get_location()
        update_listing_form.description.data = listing.get_description()

        return render_template('updateListing.html', form=update_listing_form)

@app.route('/deleteUser/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    users_dict = {}
    db = shelve.open('user', 'w')
    users_dict = db['Users']

    users_dict.pop(user_id)

    db['Users'] = users_dict
    db.close()

    return redirect(url_for('retrieve_users'))

@app.route('/deleteListing/<int:listing_id>', methods=['GET', 'POST'])
def delete_listing(listing_id):
    listing_dict = {}
    db = shelve.open('listing', 'w')
    listing_dict = db['listing']

    listing_dict.pop(listing_id)

    db['listing'] = listing_dict
    db.close()

    return redirect(url_for('retrieve_listing'))

@app.route("/search", methods=["GET", "POST"])
def search():
    listing_dict = {}
    db = shelve.open('listing', 'r')
    try:
        listing_dict = db['listing']
    except:
        pass
    db.close()

    query = request.form.get("query")
    results = []

    if query:
        # Case-insensitive search in title
        for key in listing_dict:
            listing = listing_dict.get(key)
            if query.lower() in listing._Listing__title.lower():
                results.append(listing)

    return render_template("results.html", query=query, results=results)

@app.route('/grains')
def grains():
    listing_dict = {}
    db = shelve.open('listing', 'r')
    try:
        listing_dict = db['listing']
    except:
        pass
    db.close()

    listing_list = []
    for key in listing_dict:
        listing = listing_dict.get(key)
        if listing._Listing__category == 'Grains':
            listing_list.append(listing)

    return render_template('grains.html', count=len(listing_list), listing_list=listing_list)

@app.route('/cannedfoods')
def cannedfoods():
    listing_dict = {}
    db = shelve.open('listing', 'r')
    try:
        listing_dict = db['listing']
    except:
        pass
    db.close()

    listing_list = []
    for key in listing_dict:
        listing = listing_dict.get(key)
        if listing._Listing__category == 'Canned Foods':
            listing_list.append(listing)

    return render_template('cannedfoods.html', count=len(listing_list), listing_list=listing_list)

@app.route('/dairy')
def dairy():
    listing_dict = {}
    db = shelve.open('listing', 'r')
    try:
        listing_dict = db['listing']
    except:
        pass
    db.close()

    listing_list = []
    for key in listing_dict:
        listing = listing_dict.get(key)
        if listing._Listing__category == 'Dairy':
            listing_list.append(listing)

    return render_template('dairy.html', count=len(listing_list), listing_list=listing_list)

@app.route('/fruits&vegetables')
def fruitsNvegetables():
    listing_dict = {}
    db = shelve.open('listing', 'r')
    try:
        listing_dict = db['listing']
    except:
        pass
    db.close()

    listing_list = []
    for key in listing_dict:
        listing = listing_dict.get(key)
        if listing._Listing__category == 'Fruits & Vegetables':
            listing_list.append(listing)

    return render_template('fruits&vegetables.html', count=len(listing_list), listing_list=listing_list)

@app.route('/beverages')
def beverages():
    listing_dict = {}
    db = shelve.open('listing', 'r')
    try:
        listing_dict = db['listing']
    except:
        pass
    db.close()

    listing_list = []
    for key in listing_dict:
        listing = listing_dict.get(key)
        if listing._Listing__category == 'beverages':
            listing_list.append(listing)

    return render_template('beverages.html', count=len(listing_list), listing_list=listing_list)

@app.route('/all')
def all():
    listing_dict = {}
    db = shelve.open('listing', 'r')
    try:
        listing_dict = db['listing']
    except:
        pass
    db.close()

    listing_list = []
    for key in listing_dict:
        listing = listing_dict.get(key)
        listing_list.append(listing)

    return render_template('all.html', count=len(listing_list), listing_list=listing_list)

@app.route('/reviewpage/<int:seller_id>/<int:buyer_id>/<int:item_id>', methods=['GET', 'POST']) 
def reviewPage(seller_id, buyer_id, item_id): 
 
    form = CreateReviewForm(request.form) 
 
    if request.method == 'POST' and form.validate(): 
 
        review_dict = {} 
        db = shelve.open('review.db') 
        try: 
            review_dict = db['Reviews'] 
        except: 
            print('Error in retrieving review database') 
 
        review = Review(seller_id, buyer_id, item_id, form.rating.data, form.review.data) 
        review_dict[review.get_id()] = review 
        db['Reviews'] = review_dict 
        db.close() 
        return redirect('/') 
 
    if request.method == 'GET':
 
        return render_template('yourhome.html', form=form)




 
@app.route('/tableofreviews') 
def reviewtable(): 
    db = shelve.open('review.db', 'r') 
    review_dict = {} 
    try: 
        review_dict = db['Reviews'] 
    except: 
        print('Error in retrieving reviews from database') 
 
    return render_template('tableofreviews.html', reviewlist=review_dict.values()) 
 
@app.route('/editreview/<int:id>', methods=['GET', 'POST']) 
def editedreview(id): 
    form = CreateReviewForm(request.form) 
    db = shelve.open('review.db', 'w') 
    review_dict = {} 
    try: 
        review_dict = db['Reviews'] 
    except: 
        print('Error accessing review database') 
    if request.method == 'POST': 
 
        review = review_dict[id] 
        review.set_review(form.review.data) 
        review.set_rating(form.rating.data) 
        db['Reviews'] = review_dict 
        db.close() 
        return redirect('/') 
 
    if request.method == 'GET': 
        review = review_dict[id] 
        form.review.data = review.get_review() 
        form.rating.data = review.get_rating() 
        return render_template('reviewpage.html', form=form) 
 
@app.route('/deletereview/<int:id>') 
def deletereview(id): 
    db = shelve.open('review.db') 
    review_dict = {} 
    try: 
        review_dict = db['Reviews'] 
    except: 
        print('Error in retrieving reviews from database') 
    del review_dict[id] 
    db['Reviews'] = review_dict 
    db.close() 
    return redirect('/') 


@app.route('/shoppingcart/<int:id>') 
def shoppingcart(id):
    return render_template('shoppingcart.html')


@app.route('/dib/<int:id>', methods=['GET', 'POST'])
def dib(id):
    user_id = session.get('user_id')

    # Create a new Dib object
    dib = Dib(user_id, id)

    # Save the Dib to the database
    dib_dict = {}
    db = shelve.open('dib', 'c')
    try:
        dib_dict = db['Dibs']
    except:
        print("Error in retrieving Dibs from dib.db.")

    dib_dict[dib.get_dib_id()] = dib
    db['Dibs'] = dib_dict
    db.close()



    form = CreateReviewForm(request.form)
    return render_template('reviewpage.html', form=form)


@app.route('/listing/<int:listing_id>')
def listing(listing_id):
    listing_dict = {}
    db = shelve.open('listing', 'r')
    try:
        listing_dict = db['listing']
    except:
        pass
    db.close()

    listing = listing_dict.get(listing_id)

    return render_template('listing.html', listing=listing)



if __name__ == '__main__':
    app.run()

