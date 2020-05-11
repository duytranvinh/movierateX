from flask import current_app as app
from flask import render_template, flash, redirect, url_for, request, jsonify, json, session
from . import db
from .forms import LoginForm, RegistrationForm, ResetForm
from .models import User, Post, Feedback
from flask_login import current_user, login_user, logout_user, login_required, login_manager
from werkzeug.urls import url_parse
import random, string, html, re, uuid
from sqlalchemy.orm import Session
import requests

# -------------------------------------------------------------------------------------------------------------------------
# ----- Index
# -------------------------------------------------------------------------------------------------------------------------
@app.route('/')
def home():
    '''Main home page

    :return: Display a set of items
    '''
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    
    form=LoginForm()
    return render_template('index.html', user=current_user, form=form)
    
# -------------------------------------------------------------------------------------------------------------------------
@app.route('/index')
@login_required
def index():
    '''Main home page (Logged in)

    *login required*

    :return: Display a set of items
    '''
    form=LoginForm()
    
    admin = 1 if current_user.email == 'admin' else None
    
    return render_template('index.html', user=current_user, form=form, admin=admin)

# -------------------------------------------------------------------------------------------------------------------------
# ----- View Individual item
# -------------------------------------------------------------------------------------------------------------------------
@app.route('/item/<string:id>', methods=['GET', 'POST'])
def item(id):
    '''Individual item page

    :return: Display item detail
    '''
    admin = 1 if current_user.is_authenticated and current_user.email == 'admin' else None
    
    # get JSON data from themoviedb
    try:
        data = getJSON("https://api.themoviedb.org/3/movie/"+id+"?api_key=09644c0c348cd25bd283e666341d2720&language=en-US");
    except Exception as e:
        return redirect(url_for('index'))
        
    try:
        omdb = getJSON("http://www.omdbapi.com/?apikey=647812cf&i="+data['imdb_id']);
    except Exception as e:
        return redirect(url_for('index'))
    
    try:
        reviews = getJSON("https://api.themoviedb.org/3/movie/"+id+"/reviews?api_key=09644c0c348cd25bd283e666341d2720&language=en-US&page=1");
    except Exception as e:
        return redirect(url_for('index'))
    
    # Rating color
    if data['vote_average'] == 'N/A':
        data['ratingColor'] = "white"
    else:
        if float(data['vote_average']) < 5:
            data['ratingColor'] = "yellow"
        elif float(data['vote_average']) > 5 and float(data['vote_average']) < 7.5:
            data['ratingColor'] = "orange"
        elif float(data['vote_average']) > 7.5:
            data['ratingColor'] = "red"
    
    # if title is empty use name instead
    data['title'] = data['name'] if data['title'] is None else data['title'];
    
    # get user review from database
    dbReviews = Post.query.filter_by(item_id=data['id']).all()
    
    form=LoginForm()
    return render_template('item.html', user=current_user, admin=admin, form=form, data=omdb, data2=data, reviews=reviews, dbReviews=dbReviews)
    
# -------------------------------------------------------------------------------------------------------------------------
# Get JSON Function
# -------------------------------------------------------------------------------------------------------------------------
def getJSON(url):
    try:
        uResponse = requests.get(url)
    except requests.ConnectionError:
       return "Connection Error"  
    Jresponse = uResponse.text
    return json.loads(Jresponse)
# -------------------------------------------------------------------------------------------------------------------------
# ----- Submit User Review
# -------------------------------------------------------------------------------------------------------------------------
@app.route('/submitReview', methods=['POST'])
@login_required
def submitReview():
    data = request.form
    if data['comment']:
        newPost = Post(user_id=current_user.id, 
                      username=current_user.username, 
                       item_id=data['id'], 
                        rating=data['rating'],
                       content=data['comment'])
        
        try:
            db.session.add(newPost)
            db.session.commit()
        except Exception as e:
            print("FAILED entry: "+str(e));
            
    return redirect('/item/'+data['id']);
    
# -------------------------------------------------------------------------------------------------------------------------
# ----- Submit User feedback to email
# -------------------------------------------------------------------------------------------------------------------------
@app.route('/send_fb', methods=['POST'])
def send_fb():
    if request.method == 'POST':
        # check if the post request has the fb_email part
        if request.form['fb_email'] == '':
            return 'Error: Need an email'

        # check if the post request has the fb_comment part
        if request.form['fb_comment'] == '':
            return 'Error: Comment is empty'
            
        new_fb = Feedback(email=request.form['fb_email'], 
                      comment=request.form['fb_comment'])
        try:
            db.session.add(new_fb)
            db.session.commit()
        except Exception as e:
            print("FAILED entry: "+str(e));
            
        return "Thank you for your feedback!"
        
    return "Have a good day!"
    
# -------------------------------------------------------------------------------------------------------------------------
@app.route('/feedback')
@login_required
def feedback():
    '''Main home page (Logged in)

    *login required*

    :return: Display a set of items
    '''
    # get user feedback from database
    query = Feedback.query.order_by(Feedback.id.desc()).all()
    
    feedbacks = []
    
    for item in query:
        temp = {
            'email': item.email,
            'comment': item.comment
        }
        feedbacks.append(temp)
    
    return json.dumps(feedbacks)


# -------------------------------------------------------------------------------------------------------------------------
# ----- User login & Registation / Logout
# -------------------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Login Function

    :return:Get radio form "login-option" to route functions to Login, Logout or Registration


    sign-in
    +++++++

    :return: Get user's input email and password, then validate and authenticate the user.


    sign-up
    +++++++

    :return: Get user's filled form data, then validate and create a new user.


    reset-login
    +++++++++++

    :return: Get user's input email, then validate the email on file and send a reset password email to the user's email.
    '''
        # if user logged in, go to main home page
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # get post data of radio button 'login-option'
    option = request.form.get('login-option')
    form = LoginForm()
    form.login_message = ""
    

    # if radio is sign-in, autheticate user
    if (option == "sign-in"):
        # validate form
        if form.validate_on_submit():
            print('validating')
            # look at first result first()
            user = User.query.filter_by(email=form.email.data).first()

            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('index'))

            #login_user(user, remember=form.remember_me.data)
            login_user(user)

            # return to page before user got asked to login
            next_page = request.args.get('next')

            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')

            return redirect(next_page)

        print('unable to login')
        return render_template('index.html', user=current_user, form=form)

    # if sign-up validate registration form and create user
    elif (option == "sign-up"):
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(email=form.email.data.lower(
            ), firstname=form.firstname.data, lastname=form.lastname.data)
            user.set_password(form.password.data)
            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                print("\n FAILED entry: {}\n".format(json.dumps(data)))
                print(e)
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
        return render_template('index.html', user=current_user, form=form, loginOption=option)

    # reset-login
    elif (option == "reset-login"):
        form = ResetForm()
        flash('reset function not set yet')
        return render_template('index.html', user=current_user, form=form, loginOption=option)

    return render_template('index.html', user=current_user, form=form)
# -------------------------------------------------------------------------------------------------------------------------
@app.route('/logout')
@login_required
def logout():
    '''Logout Function

    *login required*

    :return: Log the user out
    '''
    logout_user()
    return redirect(url_for('index'))
# -------------------------------------------------------------------------------------------------------------------------
# ----- Admin & skrunkworks stuff
# -------------------------------------------------------------------------------------------------------------------------
@app.route('/db')
@login_required
def showdb():
    if current_user.email == "admin":
        Users = User.query.all()
        Posts = Post.query.order_by(Post.id.desc()).all()
        Feedbacks = Feedback.query.order_by(Feedback.id.desc()).all()
        
        for post in Posts:
            post.body = post.body[0:100]

        return render_template('result.html', Users=Users, Posts=Posts, Feedbacks=Feedbacks)

    return redirect(url_for('index'))
# -------------------------------------------------------------------------------------------------------------------------
@app.route('/delfb/<int:id>', methods=['GET'])
@login_required
def delfb(id):
    if current_user.email == "admin":
        feedback = Feedback.query.filter_by(id=id).first()
        if feedback is None:
            return "id not found"
        else:
            db.session.delete(feedback)
            db.session.commit()

        return redirect(url_for('showdb'))

    return redirect(url_for('index'))
# -------------------------------------------------------------------------------------------------------------------------
@app.route('/delr/<int:id>', methods=['GET'])
@login_required
def delr(id):
    if current_user.email == "admin":
        post = Post.query.filter_by(id=id).first()
        if post is None:
            return "id not found"
        else:
            db.session.delete(post)
            db.session.commit()

        return redirect(url_for('showdb'))

    return redirect(url_for('index'))
# -------------------------------------------------------------------------------------------------------------------------
@app.route('/delid/<int:id>', methods=['GET'])
@login_required
def delID(id):
    if current_user.email == "admin":
        user = User.query.filter_by(id=id).first()
        if user is None:
            return "id not found"
        else:
            db.session.delete(user)
            db.session.commit()

        return redirect(url_for('showdb'))

    return redirect(url_for('index'))
# -------------------------------------------------------------------------------------------------------------------------
@app.route('/db_init')
def fillCheck():
    db.create_all()
    user = User.query.first()
    if user is not None:
        return str(user.email)
    addadmin()
    return redirect(url_for('showdb'))

def addadmin():
    admin = User(username='admin', firstname='admin', lastname='admin', email='admin')
    admin.set_password('1234')
    
    try:
        db.session.add(admin)
        db.session.commit()
        
    except Exception as e:
        return "FAILED entry: "+str(e)
# -------------------------------------------------------------------------------------------------------------------------
@app.route('/db_clearposts')
@login_required
def clearPosts():
    if current_user.email == "admin":
        Post.query.delete()
        db.session.commit()
        return redirect(url_for('showdb'))

    return redirect(url_for('index'))
