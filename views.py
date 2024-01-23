from flask import render_template, request, url_for, redirect
from app import app, db
from models import User
from utils import validate_reg, validate_login


@app.route('/')
def index():
    return render_template('index.html')


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


@app.route('/worldcloud')
def wordcloud():
    return render_template('wordcloud.html')


@app.route('/sentiment_analysis')
def sentiments_analysis():
    return render_template('detailed_sentiment.html')


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
