import joblib
import nltk
import speech_recognition as sr
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

# Function to analyze voice characteristics
def analyze_voice(audio):
    # Get the duration of the audio in seconds
    duration_seconds = len(audio.frame_data) / audio.sample_rate
    return duration_seconds

# Function to get spoken response
def get_response(question):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(question)
        audio = recognizer.listen(source)
    try:
        response = recognizer.recognize_google(audio)
        print("You said:", response)
        return response, audio
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return "", audio
    except sr.RequestError:
        print("Sorry, speech recognition service is unavailable.")
        return "", audio

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
audios = []
for question in questions:
    response, audio = get_response(question)
    responses.append(response)
    audios.append(audio)

# Preprocess responses
processed_responses = [preprocess_text(response) for response in responses]

# Analyze voice characteristics
voice_characteristics = []
for audio in audios:
    characteristics = analyze_voice(audio)
    voice_characteristics.append(characteristics)

# Calculate average voice characteristics
avg_duration = sum(voice_characteristics) / len(voice_characteristics)

# Print average voice characteristics
print("Speech Characteristics:")
print("Average Duration (seconds):", avg_duration)

# Content analysis based on keywords
content_analysis = {}

# Analyze each response for keywords related to mental health conditions
for response in responses:
    # Check for keywords related to Eating Disorders
    if 'food' in response.lower() or 'weight' in response.lower() or 'body image' in response.lower():
        content_analysis[response] = 'Eating Disorders'
    # Check for keywords related to Borderline Personality Disorder
    elif 'personality' in response.lower() or 'identity' in response.lower():
        content_analysis[response] = 'Borderline Personality Disorder'
    # Check for keywords related to ADHD
    elif 'attention deficit hyperactivity disorder' in response.lower() or 'adhd' in response.lower():
        content_analysis[response] = 'ADHD'
    # Check for keywords related to Substance Use Disorder
    elif 'substance' in response.lower() or 'drug' in response.lower() or 'alcohol' in response.lower():
        content_analysis[response] = 'Substance Use Disorder'
    # Check for keywords related to PTSD
    elif 'flashbacks' in response.lower() or 'nightmares' in response.lower() or 'traumatic event' in response.lower():
        content_analysis[response] = 'PTSD'
    # Check for keywords related to Schizophrenia
    elif 'hallucinations' in response.lower() or 'delusions' in response.lower() or 'psychosis' in response.lower():
        content_analysis[response] = 'Schizophrenia'
    # Check for keywords related to Depression
    elif 'depressed' in response.lower() or 'hopeless' in response.lower() or 'worthless' in response.lower():
        content_analysis[response] = 'Depression'
    # Check for keywords related to Anxiety
    elif 'nervous' in response.lower() or 'anxious' in response.lower() or 'panic' in response.lower():
        content_analysis[response] = 'Anxiety'
    # Check for keywords related to Bipolar Disorder
    elif 'manic' in response.lower() or 'depressed' in response.lower() or 'mood swings' in response.lower():
        content_analysis[response] = 'Bipolar Disorder'
    # Add more conditions for other disorders

# Classify mental health condition based on speech characteristics
if avg_duration < 2:
    predicted_condition_voice = 'Depression'
elif avg_duration > 3:
    predicted_condition_voice = 'Anxiety'
elif avg_duration > 2.5:
    predicted_condition_voice = 'PTSD'
elif 1.5 < avg_duration < 3:
    predicted_condition_voice = 'Bipolar Disorder'
elif avg_duration < 2.5:
    predicted_condition_voice = 'Schizophrenia'
elif avg_duration < 3:
    predicted_condition_voice = 'Borderline Personality Disorder'
elif 2 < avg_duration < 3.5:
    predicted_condition_voice = 'Eating Disorders'
elif avg_duration > 3.5:
    predicted_condition_voice = 'ADHD'
elif avg_duration > 2:
    predicted_condition_voice = 'Substance Use Disorders'
else:
    predicted_condition_voice = None

# Combine both voice analysis and content analysis predictions
print("\nCombined Predictions:")

# If the model predicts a mental health condition, use that; otherwise, use content analysis
if predicted_condition_voice:
    print("Predicted mental health condition (based on voice characteristics):", predicted_condition_voice)
else:
    print("No mental health condition identified based on voice characteristics.")

# If content analysis predicts a mental health condition, use that; otherwise, use voice analysis
if content_analysis:
    print("Predicted mental health condition (based on content analysis):", list(content_analysis.values())[0])
else:
    print("No mental health condition identified based on content analysis.")
