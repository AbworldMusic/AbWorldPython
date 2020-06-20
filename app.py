from flask import Flask, render_template, redirect, request
from flask_bootstrap import Bootstrap
app = Flask(__name__)

Bootstrap(app)

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/enrollment')
def enrollment():
    if request.method == "GET":

        return render_template("enrollment.html")

if __name__ == '__main__':
    app.run(debug=True)