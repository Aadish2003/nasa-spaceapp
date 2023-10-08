import mysql.connector
from werkzeug.security import check_password_hash


def db():
    return mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="nasa"
)

def check_username(mydb, username):
    with mydb.cursor() as cr:
        cr.execute("SELECT username FROM users WHERE USERNAME = %s;", (username,))
        result = cr.fetchone()
    return len(result) == 1 if result else False

def add_user(mydb, username, password, fname, lname, email, phone, gender, dob):
    with mydb.cursor() as cr:
        cr.execute("INSERT INTO users(username, password, first_name, last_name, email, phone, gender, dob) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (username, password, fname, lname, email, phone, gender, dob,))
        mydb.commit()

def login(mydb, username, password):
    with mydb.cursor() as cr:
        cr.execute("SELECT password FROM users WHERE username = %s;", (username,))
        hashed_password = cr.fetchone()
        if hashed_password:
            if check_password_hash(hashed_password[0], password):
                cr.execute("SELECT * FROM users WHERE username = %s;", (username,))
                return cr.fetchone()
    return False

def planet_data(db, planet):
    with db.cursor() as cr:
        cr.execute("SELECT distance_in_mil, description, moons, travel_time, next_nearest FROM planets WHERE name = %s;", (planet,))
        return cr.fetchone()

def is_planet(db, planet):
    with db.cursor() as cr:
        cr.execute("SELECT id FROM planets WHERE name = %s", (planet,))
        result = cr.fetchone()
        return len(result) == 1

def location_data(db, planet):
    with db.cursor() as cr:
        cr.execute("SELECT locations.name, locations.description, locations.price, locations.tourist_rating, locations.hotels, locations.hospitals, locations.tourist_attractions, locations.spaceports, locations.activities, locations.entertainment, locations.climate, locations.events FROM locations JOIN planets ON locations.planet = planets.id WHERE planets.name = %s", (planet,))
        return cr.fetchall()

def spaceships(db, planet):
    with db.cursor() as cr:
        cr.execute("SELECT spaceships.name, spaceships.leaving_date, spaceships.price, spaceships.capacity FROM spaceships JOIN planets ON spaceships.planet = planets.id WHERE planets.name = %s", (planet,))
        return cr.fetchall()