# SymptoSage: AI-Powered Symptom Analysis & Diagnosis

SymptoSage is a **Flask-based web application** that uses **Machine Learning** to predict diseases based on user-provided symptoms. It consists of three main components:

- **Model** (Machine Learning model for disease prediction)
- **Backend FastAPI** (Handles API requests for predictions)
- **Flask App** (User interface for symptom input and additional features)
- **Kubernetes** (For managing the conatiners in one clusture)

---

## 📂 Folder Structure

```
📦 SymptoSage
├── 📂 Model                # Machine learning model (Pickle file, scripts)
├── 📂 Backend FastAPI      # FastAPI-based backend for model inference
├── 📂 Flask App            # Flask web application with MongoDB integration
├── 📂 Kubernetes           # For managing the Docker containers in one clusture

```

---

## 🚀 Features

### ✅ **Flask App**
- User authentication (Login/Register with MongoDB Atlas)
- Disease prediction based on symptoms
- User dashboard with **past predictions & history**
- **Community forum** for discussion & health advice

### ✅ **FastAPI Backend**
- Handles **model inference requests** efficiently
- Exposes a **API** for Flask app integration

### ✅ **Machine Learning Model**
- Uses **Natural Language Processing (NLP)** "The Bag of Words" for symptom processing
- Built using **Naïve Bayes Classifier** using Vectorization
- Classfies into 20+ Diseases

### ✅ **Database Integration**
- **MongoDB Atlas** stores user profiles, past predictions, and forum posts for better user connectivity.

### ✅ **Scalability with Kubernetes**
- **Load-balanced one Clusture** for better performance

---
## Screenshots
![Screenshot 2025-03-17 003732](https://github.com/user-attachments/assets/412079cd-18ba-4d5f-9793-e80b9a5813ff) 
![Screenshot 2025-03-17 003651](https://github.com/user-attachments/assets/9f15de6f-e38e-4088-9c28-e8b24e75eeb8)
![Screenshot 2025-03-17 003710](https://github.com/user-attachments/assets/4cb09994-312c-4d60-b85b-f16dd685f662)

---
## 🛠️ Setup Guide

### 1️⃣ **Clone the Repository**
```sh
git clone https://github.com/HeyyyBooo/symptosage.git
cd symptosage
```

### 2️⃣ **Set Up the Python Environment**
```sh
cd Backend FastAPI
pip install -r requirements.txt
cd ..
cd Flask App
pip install -r requirements.txt
```

### 3️⃣ **Run the FastAPI Backend**
```sh
cd Backend FastAPI
uvicorn app:app --host 0.0.0.0 --port 5002
cd ..
```

### 4️⃣ **Run the Flask App**
```sh
cd Flask App
python app.py
cd ..
```

---

"Dont Forget to update new api link in app.py of flask App"
## 🐳 Deploying with Docker

```sh
cd Backend FastAPI
docker build -t symptoapi .
docker run -p 5002:8000 symtoapi
cd ..
cd Flask App
docker build -t symptosage .
docker run -p 5000:5000 symptosage
```

---

## ☁️ Deploying with Kubernetes
(minikube)

```sh
cd kubernetes
kubectl apply -f fastapi-deployment.yaml
kubectl apply -f fastapi-service.yaml
kubectl apply -f flask-deployment.yaml
kubectl apply -f flask-service.yaml
```

Check running pods:
```sh
kubectl get pods
```

---

## 🤝 Contributing
Feel free to **fork** this repository and submit a **pull request** if you'd like to improve the project!

---

## 📜 License
This project is licensed under the MIT License.

---

## 📧 Contact
For any questions or suggestions, reach out at **narzeenishant@yahoo.com**.

🚀 **Happy Coding!**

