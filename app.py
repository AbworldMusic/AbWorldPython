from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
app = Flask(__name__)

Bootstrap(app)
@app.route('/')
def index():
    return "Hello World!"

if __name__ == '__main__':
    app.run()