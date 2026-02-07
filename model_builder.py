import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# Load data
df = pd.read_csv('spam.csv')

# Convert text to numbers
tfidf = TfidfVectorizer()
X = tfidf.fit_transform(df['message'])
y = df['label']

# Train Model
model = MultinomialNB()
model.fit(X, y)

# Save the brain
pickle.dump(model, open('phishing_model.pkl', 'wb'))
pickle.dump(tfidf, open('tfidf_vectorizer.pkl', 'wb'))
print("AI Brain Ready!")