from .functions import getData
from app import app

@app.route('/')
def homepage():
  return getData("Captain of Industry", parameter="recipes")