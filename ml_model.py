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
def analyze_sentiment(text: str) -> str:
    positive_words = ["complete", "finish", "done", "success", "great", "excellent", "good", "happy", "achieve"]
    negative_words = ["bug", "error", "fail", "broken", "crash", "urgent", "critical", "problem", "fix"]
    
    text_lower = text.lower()
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    
    if pos_count > neg_count:
        return "positive"
    elif neg_count > pos_count:
        return "negative"
    else:
        return "neutral"