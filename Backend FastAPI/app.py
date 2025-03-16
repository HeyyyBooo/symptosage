from fastapi import FastAPI, HTTPException
import joblib
import numpy as np
from pydantic import BaseModel
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import nltk
import re

nltk.download('stopwords')

app = FastAPI()


model_path = "symp.pkl"  
vectorizer_path = "vector.pkl"

try:
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}")


class InputData(BaseModel):
    features: str  

@app.post("/predict")
def predict(data: InputData):
    try:
        new_review = re.sub(r'[^a-zA-Z]', ' ', data.features)
        new_review = new_review.lower().split()

        ps = PorterStemmer()
        all_stopwords = stopwords.words('english')
        if 'not' in all_stopwords:
            all_stopwords.remove('not') 

        new_review = [ps.stem(word) for word in new_review if word not in set(all_stopwords)]
        new_review = ' '.join(new_review)

        new_corpus = [new_review]
        test_vectorized = vectorizer.transform(new_corpus).toarray()

       
        diseases = [
            'ACNE', 'ARTHRITIS', 'BRONCHIAL ASTHMA', 'CERVICAL SPONDYLOSIS', 'CHICKEN POX',
            'COMMON COLD', 'DENGUE', 'DIMORPHIC HEMORRHOIDS', 'FUNGAL INFECTION', 'HYPERTENSION',
            'IMPETIGO', 'JAUNDICE', 'MALARIA', 'MIGRAINE', 'PNEUMONIA', 'PSORIASIS', 'TYPHOID',
            'VARICOSE VEINS', 'ALLERGY', 'DIABETES', 'DRUG REACTION', 'GASTROESOPHAGEAL REFLUX DISEASE',
            'PEPTIC ULCER DISEASE', 'URINARY TRACT INFECTION'
        ]

        
        predicted_index = model.predict(test_vectorized)[0]
        output = diseases[predicted_index]

        return {"prediction": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")


@app.get("/")
def home():
    return {"message": "ML Inference API is running!"}

