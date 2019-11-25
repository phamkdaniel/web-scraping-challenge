from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

import scrape_mars


app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route('/')
def index():
    # Find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template('index.html', info=mars_data)


@app.route('/scrape')
def scrape():
    # run scrape function
    mars_data = scrape_mars.scrape()

    # update Mongo databse
    mongo.db.collection.update({}, mars_data, upsert=True)

    # redirect to home page
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)
