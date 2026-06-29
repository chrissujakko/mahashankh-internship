from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

# Training data - sample tasks with priority labels
training_texts = [
    "fix critical bug in production server",
    "urgent meeting with client today",
    "server is down need immediate fix",
    "deploy hotfix to production now",
    "read a book this weekend",
    "buy groceries sometime this week",
    "organize desk when free",
    "watch tutorial video later",
    "write weekly report by friday",
    "review code before end of day",
]

training_labels = [
    "high", "high", "high", "high",
    "low", "low", "low", "low",
    "medium", "medium"
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(training_texts)

model = MultinomialNB()
model.fit(X, training_labels)

def predict_priority(task_title: str) -> str:
    X_new = vectorizer.transform([task_title])
    prediction = model.predict(X_new)
    return prediction[0]