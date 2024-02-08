from flask  import render_template, request, url_for, redirect, abort
from app    import app, db
from models import User

# Utilities functions
from utils.auth  import ( validate_reg, validate_login,)
from utils.sentiment_analysis import (
        get_top_five_negative_reviews,
        get_top_five_positive_reviews,
        count_bad_reviews,
        prepare_reviews
    )
import pandas as pd


@app.route('/')
def index():
    '''Homepage of the web application'''

    #Static data to show sentiment_analysis
    reviews = { 'good_percentage' : 60, 'bad_percentage'  : 40 }
    return render_template('index.html', reviews=reviews)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        response = request.form.to_dict()
        # validate the form response
        if validate_reg(response):
            user = User.query.filter_by(email=response.get('email')).first()
            # user with same email should not be already registered.
            if not user:
                user = User(first_name=response.get('first_name'), last_name=response.get('last_name'),
                            email=response.get('email'))
                user.set_password(response.get('password'))
                db.session.add(user)
                db.session.commit()

                # registration successful
                return redirect(url_for('login'))

    # for GET request and invalid form data , return register page
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        response = request.form.to_dict()
        # validate login form data
        if validate_login(response):
            user = User.query.filter_by(email=response.get('email')).first()
            #  check if user is registered
            if user:
                check = user.check_password(response.get('password'))
                # if password is correct
                if check:
                    # can flash login-success message
                    # We can also generate and return jwt token here
                    return redirect(url_for('index'))

    # for GET request and invalid form data , return login page
    return render_template('login.html')


@app.route('/map')
def map1():
    return render_template('map1.html')


@app.route('/wordcloud')
def wordcloud():
    return render_template('wordcloud.html')


@app.route('/sentiment_analysis')
def sentiments_analysis():
    '''Retrieve and visualize data from excel file'''

    reviews = []

    '''Ensuring - File reading & Proper Data availability '''
    try:
        df            = pd.read_excel('data/Beard-Trimmer.xlsx', index_col=None)
        total_reviews = len(df)

        # Following columns must present in excel file 
        required_columns = ['Reviewer_Name','Review_Text','Review_Stars','Review_Date']
        df               = df[required_columns]

        if df.empty: raise ValueError

    # Show No-Review-Found-Message, on file not found
    except FileNotFoundError:
        print('Error raised! - File not found')

    # Show No-Review-Found-Message, on invalid data found in CSV
    except (ValueError,KeyError):
        print('Error raised! - Invalid data found in excel file')

    except Exception as e:
        print('Unexpected exception raised - ',type(e))
        abort(500, 'An unexcepted error raised')

    else:
        # Sort reviews by REVIEWS_STARS
        df = df.sort_values(by='Review_Stars')

        total_reviews = len(df)

        # Collect top five positive & negative reviews
        good_reviews = get_top_five_positive_reviews(df, total_reviews)
        bad_reviews  = get_top_five_negative_reviews(df, 5)

        # Count bad reviews ( CONSIDERING rating < 3 as BAD )
        total_bad_reviews = count_bad_reviews(df)

        # Prepare data for templates
        reviews = prepare_reviews( good_reviews,
                                   bad_reviews,
                                   total_reviews,
                                   total_bad_reviews )
        # Debugging
        print('Prepared reviews data - ',reviews)

    # FileNotFoundError, Invalid Data: leads to 'No Review Found Error Message'  
    return render_template('sentiment_analysis.html', reviews=reviews )


# Showing data from excel file
@app.route('/feature_breakdown')
def feature_breakdown():
    return render_template('feature_breakdown.html')


@app.route('/suggestions')
def suggestions():
    return render_template('suggestions.html')


@app.route('/competitor_analysis')
def comp_analysis():
    return render_template('All_textual.html')


@app.route('/product_list')
def prod_list():
    return render_template('tables.html')
