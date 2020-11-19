from flask import Flask 
from app import app
from user.models import User
from flask import Blueprint

db_api = Blueprint('routes', __name__)

@db_api.route('/user/signup', methods=['GET'])
def signup():
    return User().signup()
