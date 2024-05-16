import joblib
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Load the pre-trained model
model_filename = 'mental_health_classifier_model.sav'
model = joblib.load(model_filename)

# Function to preprocess text
def preprocess_text(text):
    # Tokenization
    tokens = word_tokenize(text.lower())
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    return " ".join(lemmatized_tokens)

# Questions to ask
questions = [
    "How have you been feeling lately?",
    "Have you been sleeping well?",
    "Do you find it hard to concentrate?",
    "Have you lost interest in activities you used to enjoy?",
    "Do you feel tired or fatigued most of the time?",
    "Do you feel nervous, anxious, or on edge frequently?",
    "Have you experienced sudden panic attacks?",
    "Do you avoid social situations or activities you used to enjoy?",
    "Have you experienced flashbacks or nightmares about a traumatic event?",
    "Do you feel detached from reality or your surroundings?"
]

# Collect responses from the user
responses = []
for question in questions:
    response = input(question + " ")
    responses.append(response)

# Preprocess responses
processed_responses = [preprocess_text(response) for response in responses]

# Make prediction
predicted_condition = model.predict(processed_responses)
print("Predicted mental health condition:", predicted_condition[0])
