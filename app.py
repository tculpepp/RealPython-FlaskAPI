# app.py

from flask import render_template # Remove: import Flask
# Remove: import connexion
import config
from models import Person

app = config.connex_app
app.add_api(config.basedir / "swagger.yml")

# To connect the API configuration file with your Flask app,
# you must reference swagger.yml in your app.py file

@app.route("/")
def home():
    people = Person.query.all()
    return render_template("home.html", people=people)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)