# Importing dependencies
from flask import Flask

# Creating new FLask app instance
app = Flask(__name__)

# CREATING ROUTES
# Define app starting point or 'root'
@app.route('/' )

# Route 1
@app.route('/')
def hello_world():
    return 'Hello World'
