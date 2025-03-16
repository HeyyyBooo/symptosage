from flask import Flask, render_template, request, redirect, url_for, session , flash
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
import requests
from datetime import datetime
from bson.objectid import ObjectId
import humanize

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secure key


app.config["MONGO_URI"] = "mongodb+srv://narzee:E2VZaSQ8i3WtfHQM@cluster0.trbt0.mongodb.net/Symptosage?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

posts_collection =mongo.db["forum_posts"]
FASTAPI_URL = "http://192.168.0.104:5002/predict"
disease_data = {
    'ACNE': ["Maintain good skincare habits, use topical treatments, and consider prescription medications.", "Dermatologist"],
    'ARTHRITIS': ["Medications, physical therapy, and lifestyle changes.", "Rheumatologist"],
    'BRONCHIAL ASTHMA': ["Use inhalers as prescribed, identify and avoid triggers.", "Pulmonologist"],
    'CERVICAL SPONDYLOSIS': ["Physical therapy, pain medications, and lifestyle modifications.", "Orthopedic Specialist"],
    'CHICKEN POX': ["Rest, antiviral medications, and symptom relief.", "General Physician"],
    'COMMON COLD': ["Rest, hydration, and over-the-counter medications.", "General Physician"],
    'DENGUE': ["Rest, hydration, and medical monitoring.", "Infectious Disease Specialist"],
    'DIMORPHIC HEMORRHOIDS': ["Dietary changes, topical treatments, and surgery if needed.", "General Surgeon"],
    'FUNGAL INFECTION': ["Antifungal medications, hygiene, and avoiding damp environments.", "Dermatologist"],
    'HYPERTENSION': ["Lifestyle changes, medications, and regular monitoring.", "Cardiologist"],
    'IMPETIGO': ["Antibiotics, hygiene, and keeping areas clean.", "Dermatologist"],
    'JAUNDICE': ["Rest, hydration, and treating the underlying cause.", "Hepatologist"],
    'MALARIA': ["Antimalarial medications, rest, and supportive care.", "Infectious Disease Specialist"],
    'MIGRAINE': ["Identify triggers, use medications, and lifestyle changes.", "Neurologist"],
    'PNEUMONIA': ["Antibiotics, rest, and supportive care.", "Pulmonologist"],
    'PSORIASIS': ["Topical treatments, medications, and lifestyle adjustments.", "Dermatologist"],
    'TYPHOID': ["Antibiotics, hydration, and rest.", "Infectious Disease Specialist"],
    'VARICOSE VEINS': ["Compression stockings, lifestyle changes, and medical procedures.", "Vascular Surgeon"],
    'ALLERGY': ["Avoid allergens, use antihistamines, and consider immunotherapy.", "Allergist"],
    'DIABETES': ["Medications, insulin therapy, dietary changes, and monitoring.", "Endocrinologist"],
    'DRUG REACTION': ["Discontinue the drug, seek medical attention.", "General Physician"],
    'GERD': ["Medications, lifestyle changes, and surgery if severe.", "Gastroenterologist"],
    'PEPTIC ULCER DISEASE': ["Medications, antibiotics for H. pylori, and lifestyle changes.", "Gastroenterologist"],
    'URINARY TRACT INFECTION': ["Antibiotics, fluids, and hygiene.", "Urologist"]
}


@app.template_filter('humanize_time')
def humanize_time(timestamp):
    return humanize.naturaltime(datetime.utcnow() - timestamp)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        dob = request.form['dob']
        email = request.form['mail']
        phoneNo = request.form['phoneno']
        
        if mongo.db.users.find_one({"username": username}):
            flash("Username already exists!","error")
            return render_template('register.html')

        
        mongo.db.users.insert_one({
            "username": username,
            "password": password,
            "dob": dob,
            "email": email,
            "phoneNo": phoneNo
        })
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = mongo.db.users.find_one({"username": username})
        if user and bcrypt.check_password_hash(user['password'], password):
            # Store user in session
            session['user_id'] = str(user["_id"])
            session['username'] = user["username"]
            session['email'] = user["email"]
            session['dob'] = user["dob"]
            session['phoneNo'] = user["phoneNo"]
            return redirect(url_for('index')) 
        
        flash("Invalid credentials!", "error")
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()  
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    solution = None
    doctor = None
    error = None

    if request.method == 'POST':
        symptoms = request.form.get('features')
        if symptoms:
            try:
                response = requests.post(FASTAPI_URL, json={"features": symptoms})
                if response.status_code == 200:
                    prediction = response.json().get("prediction", "Error in prediction")
                    
                    
                    if prediction in disease_data:
                        solution, doctor = disease_data[prediction]
                    
                    
                    if 'user_id' in session:
                        timestamp = datetime.now()
                        mongo.db.predictions.insert_one({
                            "user_id": session['user_id'], 
                            "symptoms": symptoms, 
                            "prediction": prediction,
                            "solution": solution,
                            "doctor": doctor,
                            "date": timestamp.strftime("%Y-%m-%d"),
                            "time": timestamp.strftime("%H:%M:%S")
                        })
                else:
                    error = f"Error: {response.status_code}, {response.text}"
            except requests.exceptions.RequestException as e:
                error = f"Request failed: {e}"
        else:
            error = "Please enter some symptoms."

    return render_template('index.html', prediction=prediction, solution=solution, doctor=doctor, error=error, session=session)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))  

    records = mongo.db.predictions.find({"user_id": session['user_id']})
    records=list(records)
    return render_template('dashboard.html', records=records, session=session)


@app.route("/forum", methods=["GET", "POST"])
def forum():
    if request.method == "POST":
        if "username" in session:
            title = request.form.get("title")
            content = request.form.get("content")
            if title and content:
                new_post = {
                    "username": session["username"],
                    "title": title,
                    "content": content,
                    "replies": [],
                    "timestamp": datetime.utcnow()
                }
                posts_collection.insert_one(new_post)
                return redirect(url_for("forum"))
        else:
            return redirect(url_for("login"))
    
    posts = list(posts_collection.find().sort("timestamp", -1))
    return render_template("forum.html", posts=posts)

@app.route("/reply/<post_id>", methods=["POST"])
def reply(post_id):
    if "username" in session:
        reply_content = request.form.get("reply_content")
        if reply_content:
            posts_collection.update_one({"_id": ObjectId(post_id)}, {"$push": {"replies": {"username": session["username"], "content": reply_content, "timestamp": datetime.utcnow()}}})
    return redirect(url_for("forum"))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
