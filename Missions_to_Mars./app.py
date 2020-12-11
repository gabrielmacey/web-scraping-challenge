#Import Flask
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

# Set route
@app.route('/')
def index():
    planet_mars = mongo.db.marspage.find_one()
    return render_template("index.html", planet_mars = planet_mars)


@app.route('/scrape')
def scraper():
    marspage = mongo.db.marspage
    mars_stuff = scrape_mars.scrape()
    marspage.update({}, mars_stuff, upsert=True)
    print(marspage)
    return redirect("/", code=302)