# Importing Dependencies
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem.porter import PorterStemmer
import pickle

# Load the dataset
dataset = pd.read_csv("Data.csv")
print("Dataset loaded successfully.")

# Basic Data Analysis
print(f"Shape of dataset: {dataset.shape}")
print(f"Dataset Info: \n{dataset.info()}")
print(f"Missing values: \n{dataset.isnull().sum()}")

# Visualizing Distribution of Course Difficulty Levels
plt.figure(figsize=(8,6))
sns.countplot(x='Difficulty Level', data=dataset)
plt.title("Distribution of Course Difficulty Levels")
plt.xlabel('Difficulty Level')
plt.ylabel('Count')
plt.show()

# Visualizing Distribution of Course Ratings
plt.figure(figsize=(8,6))
sns.countplot(x='Course Rating', data=dataset)
plt.title("Distribution of Course Ratings")
plt.xlabel('Course Rating')
plt.ylabel('Count')
plt.show()

# Selecting Required Columns
dataset = dataset[['Course Name', 'Difficulty Level', 'Course Description', 'Skills']]

# Pre-Processing Data (Cleaning)
dataset['Course Name'] = dataset['Course Name'].str.replace(' ', ',').str.replace(',,', ',').str.replace(':', '')
dataset['Course Description'] = dataset['Course Description'].str.replace(' ', ',').str.replace(',,', ',').str.replace('_', '').str.replace(':', '').str.replace('(', '').str.replace(')', '')
dataset['Skills'] = dataset['Skills'].str.replace('(', '').str.replace(')', '')

# Creating Tags Column by Combining Relevant Text Columns
dataset['tags'] = dataset['Course Name'] + dataset['Difficulty Level'] + dataset['Course Description'] + dataset['Skills']
print("Tags column created successfully.")

# Creating a New DataFrame for Recommendations
recommendation_df = dataset[['Course Name', 'tags']]
recommendation_df['tags'] = recommendation_df['tags'].str.replace(',', ' ').apply(lambda x: x.lower())
recommendation_df['Course Name'] = recommendation_df['Course Name'].str.replace(',', ' ')
recommendation_df.rename(columns={'Course Name': 'course_name'}, inplace=True)
print(f"New DataFrame for recommendations created with shape: {recommendation_df.shape}")

# Text Vectorization using CountVectorizer
cv = CountVectorizer(max_features=5000, stop_words='english')
vectorized_text = cv.fit_transform(recommendation_df['tags']).toarray()
print("Text vectorization completed.")

# Stemming the Tags Column to Enhance Similarity Measurement
ps = PorterStemmer()
def stem_text(text):
    return " ".join([ps.stem(word) for word in text.split()])

recommendation_df['tags'] = recommendation_df['tags'].apply(stem_text)
print("Stemming process completed on tags.")

# Calculating Cosine Similarity between Courses
cosine_sim = cosine_similarity(vectorized_text)
print("Cosine similarity matrix created.")

# Function to Recommend Courses Based on Similarity
def recommend_courses(course_name):
    try:
        course_index = recommendation_df[recommendation_df['course_name'] == course_name].index[0]
        course_distances = cosine_sim[course_index]
        recommended_courses = sorted(list(enumerate(course_distances)), reverse=True, key=lambda x: x[1])[1:7]

        print(f"Recommended courses similar to '{course_name}':")
        for i in recommended_courses:
            print(recommendation_df.iloc[i[0]].course_name)
    except IndexError:
        print(f"Course '{course_name}' not found in the dataset.")

# Test the Recommendation Function
recommend_courses('Business Strategy Business Model Canvas Analysis with Miro')

# Saving the Model and Data
os.makedirs('models', exist_ok=True)
pickle.dump(cosine_sim, open('models/cosine_similarity_model.pkl', 'wb'))
pickle.dump(recommendation_df.to_dict(), open('models/course_list.pkl', 'wb'))
pickle.dump(recommendation_df, open('models/courses.pkl', 'wb'))

print("Model and Data exported successfully.")

