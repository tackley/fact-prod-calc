from .data import getData
from flask import Flask

app = Flask(__name__)

@app.route('/')
def homepage():
  return getData("Captain of Industry", parameter="machines")