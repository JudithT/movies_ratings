"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import(Flask, render_template,redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie,connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route('/users')
def user_list():
    """Show list of Users"""

    users = User.query.all()

    return render_template("user_list.html", users=users)


@app.route('/movies')
def all_movies():
    movies = Movie.query.order_by('title').all()

    return render_template("movies.html", movies=movies)


@app.route('/movies/<movie_id>')
def movie(movie_id):
    movie=Movie.query.filter_by(movie_id=movie_id).first()
    ratings = movie.ratings

    print("AAA",movie)
    print("BBB",ratings)

    return render_template("moviepage.html", movie=movie,ratings=ratings)


@app.route('/users/<user_id>')
def userpage(user_id):
    """Show list of Users"""
    user = User.query.filter_by(user_id = user_id).first()
    ratings=Rating.query.filter_by(user_id=user_id).all()
    print("=====>1",user)
    print("=====>2",ratings)
    # ratings = user.ratings


    return render_template("user.html", users=user, ratings=ratings)




@app.route('/Processregister', methods=["POST"])
def register_process():

    password=request.form.get("password")
    email=request.form.get("email")
    age=request.form.get("age")
    zipcode=request.form.get("zipcode")


    user_email = User.query.filter_by(email=email).first()
    if user_email:
        flash("email is already in the database")
    else:
        flash("Successful registration")
        user = User(email = email, password=password, age=age, zipcode=zipcode)
        db.session.add(user)
        db.session.commit()


    return redirect('/')





@app.route('/register', methods=["GET"])
def registration_form():
    return render_template('register.html')


@app.route('/login', methods=["GET"])
def loginform():
    return render_template("login.html")


@app.route('/login', methods=["POST"])
def processlogin():
    password = request.form.get("password")
    email= request.form.get("email")
    user = User.query.filter_by(email=email, password=password).first()

    if user:
        session['user_id'] = user.user_id
        flash("Logged in ")
        return redirect('/')
    else:
        return redirect('/login')



@app.route('/logout')
def logout():
    session['user_id'] = None
    return redirect('/')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
