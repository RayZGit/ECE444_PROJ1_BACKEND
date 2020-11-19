import pyrebase
from flask import Flask,jsonify

class fire:
    firebaseConfig = {
        "apiKey": "AIzaSyBW9aHSDinhjUdZ0SMp5GZ0I4DwU4BJyb0",
        "authDomain": "ece444-recipe.firebaseapp.com",
        "databaseURL": "https://ece444-recipe.firebaseio.com",
        "projectId": "ece444-recipe",
        "storageBucket": "ece444-recipe.appspot.com",
        "messagingSenderId": "246271267675",
        "appId": "1:246271267675:web:4fff647c6555bd8fd3807e",
        "measurementId": "G-5M61G8JNFM"
    }

    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    db = firebase.database()

    def signIn(self,email,password):
        # auth.sign_in_with_email_and_password('ruizhou@gmail.com','sky123')
        try:
            self.auth.sign_in_with_email_and_password(email,password)
        except:
            return False
        
        return True
    
    def signUp(self,email,password):
        try:
            self.auth.create_user_with_email_and_password(email,password)
        except Exception as e:
           return False
        
        return True
        













# class fire:
#     cred = credentials.Certificate("ece444-recipe-firebase-adminsdk-g82vb-e4b4d2e638.json")
#     firebase_admin.initialize_app(cred)
#     db = firestore.client()
#     userlist = db.collection(u'users').document(u'auth')

#     def signUp():
#         return userlist
    