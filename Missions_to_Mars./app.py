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
    marspage = mongo.db.marspages.find_one()
    return render_template("index.html", marspage=marspage)


@app.route('/scrape')
def scraper():
    marspages = mongo.db.marspages
    mars_stuff = scrape_mars.scraped_planet()
    marspages.update({}, mars_stuff, upsert=True)
    print(mars)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
