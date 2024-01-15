import pyrebase
import json
from pprint import pprint

firebase_config = {
    "apiKey": "AIzaSyAHljBQLx5D9tLSlNupUs1EW6HUy2zvM0I",
    "authDomain": "mydecisionhub.firebaseapp.com",
    "databaseURL": "https://your-firebase-project.firebaseio.com",
    "projectId": "mydecisionhub",
    "storageBucket": "mydecisionhub.appspot.com",
    "messagingSenderId": "238521415926",
    "appId": "1:238521415926:web:0ea18dc05db6054c8714d7"
}
firebase=pyrebase.initialize_app(firebase_config)
auth=firebase.auth()
def signup(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        auth.send_email_verification(user["idToken"])
    except Exception as e:
        if "EMAIL_EXISTS" in e.strerror:
            return "E-mail already exists", "error"
        elif "WEAK_PASSWORD" in e.strerror:
            return "Password should be atleast 6 characters", "error"
        else:
            return e.strerror, "error"
    else:
        return "Successfully signed up", "success"

def signin(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        isVerified = auth.get_account_info(user["idToken"])["users"][0]["emailVerified"]
        
        if isVerified:
            return "Successfully logged in", "success"
        else:
            auth.send_email_verification(user["idToken"])
            return "email not verified", "success"
    
    except Exception as e:
        if "INVALID_PASSWORD" in e.strerror:
            return "Incorrect password", "error"
        elif "EMAIL_NOT_FOUND" in e.strerror:
            return "Incorrect e-mail", "error"

# signup = signup("asdf123@gmail.com", "123456")
# print(signup)

# login = login("asdf123@gmail.com", "123456")
# print(login)

