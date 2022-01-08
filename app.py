from flask import Flask, render_template, redirect, url_for     #use flask to render template, redirect to another url and to create a url
from flask_pymongo import PyMongo                               # use pymongo to interact with mongo db
import scraping                                                 # to use our scraping code convert jupyter notebook to python

app = Flask(__name__)

# use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"  # app.config tells python our app will connect to Mongo via Uniform Resource Identifier (like a URL)
                                                                # the URI specifies the app to reach Mongo through localhost server port 27017 via database mars_app
mongo = PyMongo(app)

### Flask routes ###

@app.route("/")                                                 # displays index.html as home page
def index():
    mars = mongo.db.mars.find_one()                             # use pymongo to find mars collection and assign path to mars variable
    return render_template("index.html", mars=mars)             # flask returns webpage using index.html file as template and the mars collection for content

@app.route("/scrape")                                           
def scrape():
    mars = mongo.db.mars                                        # new variable points to mongo database
    mars_data = scraping.scrape_all()                           # store all scraped data in new variable, where is the scrape_all function in scraping.py?
    mars.update_one({}, {"$set":mars_data}, upsert=True)        # update_one updates the database, syntax: .update_one(query_parameter, {"$set": data}, options)
                                                                # document modified/inserted/$set with mars_data. query_parameter is empty {} to update the first matching document in collection. upsert=True creates new document and always saves new data if it doesn't already exist. 
    return redirect('/', code=302)                              # redirect back to '/' after successfully scraping data

if __name__ == "__main__":                                      # tells flask to run code
    app.run()