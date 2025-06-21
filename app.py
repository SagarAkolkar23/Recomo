from flask import Flask, render_template, request, redirect, session, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import os
from recommender import get_recommendations, get_books_list
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") or "dev_secret_key"


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  
    app.run(host='0.0.0.0', port=port)

# Debug prints
print("GEMINI_API_KEY loaded:", bool(os.getenv("GEMINI_API_KEY")))
print("MONGO_URI starts with:", os.getenv("MONGO_URI")[:20] if os.getenv("MONGO_URI") else "None")

# MongoDB setup
client = MongoClient(os.getenv("MONGO_URI"))
db = client["recomo"]
users = db["users"]
preferences = db["user_preferences"]

def get_search_history(username):
    history_cursor = preferences.find({"username": username}).sort("_id", -1)
    history = []
    for doc in history_cursor:
        if "searched_at" in doc and doc["searched_at"]:
            doc["searched_at_str"] = doc["searched_at"].strftime('%Y-%m-%d %H:%M:%S')
        else:
            doc["searched_at_str"] = "Unknown"
        history.append(doc)
    return history


@app.route('/')
def index():
    if "username" in session:
        return render_template('index.html', username=session["username"])
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.find_one({"username": username}):
            return "Username already exists. Try logging in."
        hashed_password = generate_password_hash(password)
        users.insert_one({"username": username, "password": hashed_password})
        return redirect(url_for('login'))
    return render_template('signUp.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.find_one({"username": username})
        if user and check_password_hash(user["password"], password):
            session["username"] = username
            return redirect(url_for('index'))
        else:
            return "Invalid username or password."
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect(url_for('login'))

@app.route('/results', methods=['POST'])
def recommend():
    if "username" not in session:
        return redirect(url_for("login"))

    preference = request.form.get('preference')
    print(f"Received preference from user '{session['username']}': {preference}")
    print("Received preference:", preference)
    if not preference or preference.strip() == "":
        return "Please provide your preferences.", 400

    try:
        preferences.insert_one({
            "username": session["username"],
            "preference": preference,
            "searched_at": datetime.utcnow()
        })
    except Exception as e:
        print(f"Error inserting preference into DB: {e}")
        return "Failed to save your preferences. Please try again.", 500

    recommendations = get_recommendations(preference)
    if not recommendations:
        return "Sorry, couldn't get recommendations right now.", 500

    return render_template('results.html', recommendations=recommendations)

@app.route('/history')
def history():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    history = get_search_history(username)
    return render_template("history.html", history=history, username=username)

# Show the book preferences form
@app.route('/books_pref', methods=['GET'])
def books_pref():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("books_pref.html")

# Handle form submission and show recommendations
@app.route('/bookresults', methods=['POST'])
def bookresults():
    if "username" not in session:
        return redirect(url_for("login"))

    preference = request.form.get('preference')
    print(f"Received book preference from user '{session['username']}': {preference}")

    if not preference or preference.strip() == "":
        return "Please provide your preferences.", 400

    try:
        preferences.insert_one({
            "username": session["username"],
            "preference": preference,
            "type": "book",
            "searched_at": datetime.utcnow()
        })
    except Exception as e:
        print(f"Error inserting book preference into DB: {e}")
        return "Failed to save your preferences. Please try again.", 500

    recommendations = get_books_list(preference)
    if not recommendations:
        return "Sorry, couldn't fetch book recommendations right now.", 500

    return render_template('bookRecommendations.html', recommendations=recommendations)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)