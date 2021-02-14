import json
from flask import *
from flask import render_template
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app, ctrl
from layouts import *
import callbacks


# creates a Flask application, named app
app = Flask(__name__, static_url_path='/static', template_folder='static', )


# a route where we will display a welcome message via an HTML template
@app.route("/")

# @app.route("/index.html")
# def home():
#     return render_template("index.html")

# @app.route("/avalibility.html")
# def availability():
#     return render_template("avalibility.html")

# @app.route("/ownership.html")
# def owner():
#     return render_template("ownership.html")

# @app.route("/page3.html")
# def page3():
#     return render_template("page3.html")

# @app.route("./test.html")




# run the application
if __name__ == "__main__":
    app.run(debug=True)
