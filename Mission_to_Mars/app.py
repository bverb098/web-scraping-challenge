from flask import Flask, jsonify,render_template, redirect
from flask_pymongo import PyMongo
from pandas import json_normalize
import scrape_mars

#create isntance of flask app
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html",mars=mars)


@app.route("/scrape")
def scraper():
    mars=mongo.db.mars
    mars_data=scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

@app.route("/jsondic")
def marsdic():
    mars=mongo.db.mars.find_one()
    return print(mars)

if __name__ == "__main__":
    app.run(debug=True)
