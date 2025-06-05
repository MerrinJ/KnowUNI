import pandas as pd
from education_app.models import Course

def run():
    df = pd.read_csv('Dataset.csv')
    print("Dataset loaded successfully.")
    print("Columns in dataset:", df.columns)

    for index, row in df.iterrows():
        try:
            course = Course(
                name=row['Course Name'],
                university=row['University'],
                location=row['Location'],
                latitude=float(row['latitude']),
                longitude=float(row['longitude']),
                skill=row['Skills']
            )
            course.save()
            print(f"Saved: {course.name}")
        except Exception as e:
            print(f"Error on row {index}: {e}")

    print("Models saved successfully.")
