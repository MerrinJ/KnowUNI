import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel
import difflib

data = pd.read_csv('Dataset.csv')
print("Dataset loaded successfully.")
print("First five rows of the dataset:")
print(data.head())

print("\nDataset Info:")
print(data.info())
print("\nChecking for missing values:")
print(data.isnull().sum())

processed_data = data.copy()
processed_data.drop(['University', 'Difficulty Level', 'Course Rating', 'Course URL', 'Course Description'], axis=1, inplace=True)
print("\nUnnecessary columns dropped. Columns retained:")
print(processed_data.columns)

processed_data['Skills_Cleaned'] = processed_data['Skills'].fillna('')
print("\nSkills column cleaned and NaN values replaced.")

tfidf_vectorizer = TfidfVectorizer(min_df=3, max_features=None, strip_accents='unicode', analyzer='word',
                                   token_pattern=r'\w{1,}', ngram_range=(1, 3), stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(processed_data['Skills_Cleaned'])
print("\nTF-IDF vectorization applied. Shape of TF-IDF matrix:", tfidf_matrix.shape)

similarity_matrix = sigmoid_kernel(tfidf_matrix, tfidf_matrix)
print("\nSigmoid kernel computed. Shape:", similarity_matrix.shape)

course_indices = pd.Series(processed_data.index, index=processed_data['Course Name']).drop_duplicates()
print("\nReverse mapping of indices created.")

def recommend_courses(course_name, similarity_matrix=similarity_matrix):
    try:
        course_idx = course_indices[course_name]
        scores = list(enumerate(similarity_matrix[course_idx]))
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        top_courses = [i[0] for i in sorted_scores[1:11]]
        return data.iloc[top_courses].reset_index(drop=True)
    except KeyError:
        print("Course not found in the dataset.")
        return pd.DataFrame()

def search_and_recommend(keyword):
    try:
        course_list = processed_data['Course Name'].tolist()
        print(course_list)
        matches = difflib.get_close_matches(keyword, course_list)
        
        if matches:
            recommendations = recommend_courses(matches[0])

            if recommendations.empty:
                print("\nSorry! No matching courses found. Try refining your search.")
            else:
                print("\nHere are some recommendations based on your search:")
                print(recommendations)
        else:
            print("\nNo matching courses found for the given keyword.")
    except Exception as e:
        print("\nAn error occurred:", e)

skills = processed_data['Skills_Cleaned'].str.split().explode().value_counts().head(20)
plt.figure(figsize=(10, 6))
skills.plot(kind='bar', color='teal')
plt.title('Top 20 Most Frequent Skills in the Dataset')
plt.xlabel('Skill')
plt.ylabel('Frequency')
plt.xticks(rotation=90)
plt.show()

plt.figure(figsize=(10, 8))
sns.heatmap(similarity_matrix[:20, :20], cmap='viridis', xticklabels=processed_data['Course Name'].head(20), yticklabels=processed_data['Course Name'].head(20), annot=False)
plt.title("Heatmap of Similarity Matrix (Top 20 Courses)")
plt.show()


if 'Course Rating' in data.columns:
    plt.figure(figsize=(10, 6))
    sns.histplot(data['Course Rating'].dropna(), bins=20, kde=True, color='blue')
    plt.title('Distribution of Course Ratings', fontsize=16)
    plt.xlabel('Course Rating')
    plt.ylabel('Frequency')
    plt.show()





print("\nSearching for courses related to 'voices of social change'...")
search_and_recommend('voices of social change')
