from flask import Flask,jsonify
import uuid

class User:

    def signup(self):
        user = {
            "_id": "",
            "name": "",
            "email": "",
            "password": ""
        }

        return jsonify(user), 200