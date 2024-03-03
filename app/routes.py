
from app import app

@app.route('/')
@app.route('/bananas')
@app.route('/fact-prod-calc')
def homepage():
  user = {'username': 'GT'}
  return user
