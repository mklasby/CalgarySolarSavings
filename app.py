import json
from flask import *
from flask import render_template

# creates a Flask application, named app
from templates.stats import get_figs

app = Flask(__name__, static_url_path='/static', template_folder='static', )


# a route where we will display a welcome message via an HTML template
@app.route("/")
@app.route("/index.html")
def home():
    return render_template("index.html")

@app.route("/availability.html")
def availability():
    return render_template("availability.html")

@app.route("/ownership.html")
def owner():
    return render_template("ownership.html")

@app.route("/stats.html")
def page3():
    fig1,fig2,fig3,fig4=get_figs()
    return render_template("stats.html",f1=fig1,f2=fig2,f3=fig3,f4=fig4)




# run the application
if __name__ == "__main__":
    app.run(debug=True)
