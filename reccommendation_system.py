import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel
import difflib
import joblib  

data = pd.read_csv('Dataset.csv')
print("Dataset loaded successfully.")

processed_data = data.copy()
processed_data.drop(['University', 'Difficulty Level', 'Course Rating', 'Course URL', 'Course Description'], axis=1, inplace=True)
processed_data['Skills_Cleaned'] = processed_data['Skills'].fillna('')

tfidf_vectorizer = TfidfVectorizer(
    min_df=3, max_features=None, strip_accents='unicode', analyzer='word',
    token_pattern=r'\w{1,}', ngram_range=(1, 3), stop_words='english'
)
tfidf_matrix = tfidf_vectorizer.fit_transform(processed_data['Skills_Cleaned'])

similarity_matrix = sigmoid_kernel(tfidf_matrix, tfidf_matrix)

course_indices = pd.Series(processed_data.index, index=processed_data['Course Name']).drop_duplicates()

joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer.pkl')
joblib.dump(similarity_matrix, 'similarity_matrix.pkl')
print("Models saved successfully.")

def recommend_courses(course_name, similarity_matrix, course_indices):
    try:
        course_idx = course_indices[course_name]
        scores = list(enumerate(similarity_matrix[course_idx]))
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        top_courses = [i[0] for i in sorted_scores[1:11]]
        return data.iloc[top_courses].reset_index(drop=True)
    except KeyError:
        print("Course not found in the dataset.")
        return pd.DataFrame()

# Predict on new input
def predict_new_course(input_skills):
    # Load saved models
    tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
    similarity_matrix = joblib.load('similarity_matrix.pkl')
    
    # Transform new input
    input_vector = tfidf_vectorizer.transform([input_skills])
    
    # Compute similarity with existing courses
    scores = sigmoid_kernel(input_vector, tfidf_matrix)
    sorted_scores = sorted(list(enumerate(scores[0])), key=lambda x: x[1], reverse=True)
    
    # Get top recommendations
    top_courses = [i[0] for i in sorted_scores[:10]]
    return data.iloc[top_courses].reset_index(drop=True)

# Example search and recommend
print("\nSearching for courses related to 'voices of social change'...")
recommendations = predict_new_course('voices of social change')
if not recommendations.empty:
    print("\nRecommended Courses:")
    print(recommendations[['Course Name', 'Skills']])
else:
    print("\nNo recommendations found.")
