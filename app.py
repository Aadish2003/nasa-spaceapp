from flask import Flask, redirect, render_template, request, session, flash, abort
from flask_session import Session
import os
from datetime import datetime, timedelta
import database as data
from werkzeug.security import generate_password_hash
import random
import time

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
Session(app)

db = data.db()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', msg="404 Page not found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', msg="500 Internal server error"), 500


@app.route("/")
def home():
    if 'user' in session:
        return redirect('/home')
    return render_template('welcome.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        fname = request.form.get('Firstname')
        lname = request.form.get('Lastname')
        email = request.form.get('email')
        password = generate_password_hash(request.form.get('password'))
        phone = request.form.get('Phone')
        gender = request.form.get('gender')

        dob = request.form.get('dob')
        dob_date = datetime.strptime(dob, '%Y-%m-%d')
        today = datetime.now()
        age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))

        if age < 18:
            flash('You must be 18 or older to register.')
            return render_template('register.html')
        else:
            if data.check_username(db, username):
                flash('Username already exists. Login if you have account or choose another username.')
                return render_template('register.html')
            else:
                try:
                    data.add_user(db, username, password, fname, lname, email, phone, gender, dob)
                    flash('You have successfully registered. Please login to continue.')
                    return redirect('/login')
                except:
                    flash('Error while registering. Please try again. You might have entered wrong data.')
                    return render_template('register.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        if result := data.login(db, username, password):
            session['user'] = {
                'username': result[0],
                'firstname': result[1],
                'lastname': result[2],
                'email': result[3],
                'phone': result[4],
                'dob': result[5],
                'gender': result[7],
            }
            return redirect('/home')
        else:
            flash('Invalid username or password.')
            return render_template('login.html')


@app.route("/home")
def user_home():
    if 'user' in session:
        return render_template("main.html", user=session['user'])
    else:
        return redirect("/login")


@app.route("/planet/<planet>")
def planet(planet):
    if 'user' in session:
        planet = planet.capitalize()
        if data.is_planet(db, planet):
            distance, desc, moons, time, nearest = data.planet_data(db, planet)
            spaceships = data.spaceships(db, planet)
            return render_template("planet.html", user=session['user'], planet=planet, time=time, distance=distance, description=desc, moons=moons, spaceships=spaceships, nearest=nearest)
        else:
            abort(404)
    else:
        return redirect("/login")


@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect("/")


@app.route("/user/<username>")
def profile(username):
    if session['user'].get('username') == username:
        return render_template("profile.html", user=session['user'])
    else:
        return redirect("/")


@app.route("/<planet>/locations")
def locations(planet):
    if 'user' in session:
        planet = planet.capitalize()
        if data.is_planet(db, planet):
            locations = data.location_data(db, planet)
            hospitals=random.randint(7,10)
            hotels=random.randint(10,20)
            tourist_attractions=random.randint(15,20)
            spaceports=random.randint(1,4)
            random.seed(time.time())
            def generate_random_coordinates(n):
                x = set()
                while len(x) < n:
                    x.add(random.uniform(5, 95))
                y = list(range(1, 23))
                y = random.choices(y, k=n)
                ret = list()
                for x, y in zip(x, y):
                    ret.append({'x': x, 'y': y})
                return ret
            hospitals_coordinates = generate_random_coordinates(hospitals)
            hotels_coordinates = generate_random_coordinates(hotels)
            tourist_attractions_coordinates = generate_random_coordinates(tourist_attractions)
            spaceports_coordinates = generate_random_coordinates(spaceports)
            return render_template("location.html", locations=locations, planet=planet, hospitals_coordinates=hospitals_coordinates, hotels_coordinates=hotels_coordinates,tourist_attractions_coordinates=tourist_attractions_coordinates, spaceports_coordinates=spaceports_coordinates)
        else:
            abort(404)
    else:
        return redirect("/")
