from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .decorators import student_login_required


# from pre_india import display_single_course_graph
# from pre_udacity import visualize_selected_course
# from pre_uiuc import predict_course_prerequisites,plot_knowlegdge
def front_page(request):
    return render(request, "index.html")

def about_page(request):
    return render(request, "about.html")

def contact_page(request):
    return render(request, "contact.html")

def login_page(request):
    return render(request, "login.html")

def home_page(request):
    return render(request, "home.html")

def course_rec(request):
    return render(request, "coruse_recommendation.html")

def course(request):
    return render(request, "course.html")

def booking(request):
    return render(request, "booking.html")

def prerequest(request):
    return render(request, "prerequest.html")

#def profile(request):
#    return render(request, "profile.html", {"user": request.user})

def logout(request):
    return render(request, "index.html")
    
from django.shortcuts import render, redirect, get_object_or_404
from .models import  Course, Student
def profile_view(request):
    # Get saved courses from the database
    saved_courses_db = Course.objects.filter(savedcourse__user=request.user)

    # Get saved course IDs from the session
    session_saved_courses = request.session.get('course_ids', [])

    # Get courses from the session
    session_courses = Course.objects.filter(id__in=session_saved_courses)

    return render(request, "profile.html", {
        'saved_courses_db': saved_courses_db,  # Courses from the database
        'session_courses': session_courses,    # Courses from the session
    })




def profile(request):
    if not request.session.get('user_id'):  # Check if user is logged in
        return redirect('login_page')

    user_id = request.session['user_id']
    student = Student.objects.get(id=user_id)  # Fetch user details

    if request.method == "POST":
        student.name = request.POST.get("full_name")
        student.email = request.POST.get("email")
        student.qualification = request.POST.get("course_selection")
        student.phone = request.POST.get("phone_number")
        student.save()
        return render(request, "profile.html", {"student": student})  # Refresh the page after saving

    return render(request, "profile.html", {"student": student})

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student
from django.contrib.auth.hashers import make_password, check_password

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        qualification = request.POST['qualification']
        interest_areas = request.POST['interest_areas']
        password = request.POST['pass']
        re_password = request.POST['re_pass']

        if password != re_password:
            return HttpResponse("""
                <script>
                    alert("Passwords do not match!");
                    window.location.href = "/login_page/";
                </script>
            """)

        if Student.objects.filter(email=email).exists():
            return HttpResponse("""
                <script>
                    alert("A user with this email already exists!");
                    window.location.href = "/login_page/";
                </script>
            """)

        student = Student(
            name=name,
            email=email,
            phone=phone,
            qualification=qualification,
            interest_areas=interest_areas,
            password=password
        )
        student.save()

        return HttpResponse("""
            <script>
                alert("Student registered successfully!");
                window.location.href = "/login_page/";
            </script>
        """)

    return render(request, 'register.html')


from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User  # Needed for session auth

from django.contrib.auth import login as auth_login
from django.contrib.auth.backends import ModelBackend

from django.shortcuts import render
import pandas as pd
import joblib
from sklearn.metrics.pairwise import sigmoid_kernel

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel
import joblib
from django.shortcuts import render
from django.http import HttpResponse

def login(request):
    if request.method == "POST":
        username = request.POST.get("your_name")
        password = request.POST.get("your_pass")

        try:
            user = Student.objects.get(email=username)
            if password == user.password:
                # Set session manually (no Django login system)
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name

                # ✅ Create a "logged in" user by customizing request.user
                request.user = user  # Only for this request scope

                return HttpResponse(f"""
                    <script>
                        alert("Welcome, {user.name}!");
                        window.location.href = "/home_page/";
                    </script>
                """)
            else:
                return HttpResponse("""
                    <script>
                        alert("Invalid login credentials. Please try again.");
                        window.location.href = "/login_page/";
                    </script>
                """)
        except Student.DoesNotExist:
            return HttpResponse("""
                <script>
                    alert("User does not exist. Please register first.");
                    window.location.href = "/login_page/";
                </script>
            """)

    return HttpResponse("""
        <script>
            alert("Invalid request method. Please use the login form.");
            window.location.href = "/login_page/";
        </script>
    """)





from django.shortcuts import render
import pickle
import pandas as pd

cosine_sim = pickle.load(open('models/cosine_similarity_model.pkl', 'rb'))
recommendation_dict = pickle.load(open('models/course_list.pkl', 'rb'))
recommendation_df = pd.DataFrame.from_dict(recommendation_dict)

def predict_courses(course_name, top_n=5):
    try:
        course_index = recommendation_df[recommendation_df['course_name'] == course_name].index[0]
        course_distances = cosine_sim[course_index]
        recommended_courses = sorted(list(enumerate(course_distances)), reverse=True, key=lambda x: x[1])[1:top_n+1]
        return [recommendation_df.iloc[idx].course_name for idx, _ in recommended_courses]
    except IndexError:
        return [f"Course '{course_name}' not found in the dataset."]
    except Exception as e:
        return [f"An error occurred: {str(e)}"]

def course_recommendation_view(request):
    recommendations = None
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        if course_name:
            recommendations = predict_courses(course_name)

    return render(request, 'coruse_recommendation.html', {'recommendations': recommendations})


data = pd.read_csv('Dataset.csv')
print("Dataset loaded successfully.")
#print("Columns in dataset:", data.columns)

processed_data = data.copy()
processed_data.drop([ 'Difficulty Level', 'Course Rating', 'Course URL', 'Course Description'], axis=1, inplace=True)
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

def predict_new_course(input_skills):
   
    tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
    similarity_matrix = joblib.load('similarity_matrix.pkl')
    
    input_vector = tfidf_vectorizer.transform([input_skills])
    
    scores = sigmoid_kernel(input_vector, tfidf_matrix)
    sorted_scores = sorted(list(enumerate(scores[0])), key=lambda x: x[1], reverse=True)
    
    top_courses = [i[0] for i in sorted_scores[:100]]
    return data.iloc[top_courses].reset_index(drop=True)


from django.shortcuts import render
from .models import Course  

from django.db.models import FloatField
from django.db.models.functions import Cast

from django.shortcuts import render, redirect
from education_app.models import Course

from django.shortcuts import render, redirect
from education_app.models import Course

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Course  
import re

def find_courses_view(request):
    page_number = request.GET.get('page')

    # Detect if it's a fresh GET (not pagination, not redirected POST)
    is_fresh_get = request.method == "GET" and not page_number and not request.session.get("from_post")

    if is_fresh_get:
        # Just reset the specific session keys related to course search
        request.session.pop("course_ids", None)
        request.session.pop("user_interest", None)
        request.session.pop("user_location", None)
        request.session.pop("searched", None)
        request.session.pop("from_post", None)

        return render(request, "course.html", {
            "recommendations": [],
            "user_interest": "",
            "user_location": "",
            "searched": False,
        })

    if request.method == "POST":
        # Get data from form
        user_interest = request.POST.get("user_interest", "")
        user_location = request.POST.get("user_location", "")
        latitude = request.POST.get("latitude", "")
        longitude = request.POST.get("longitude", "")

        # ✅ If user_interest is empty, show error
        if not user_interest:
            return render(request, "course.html", {
                "recommendations": Course.objects.none(),
                "user_interest": user_interest,
                "user_location": user_location,
                "searched": False,
                "form_error": "Please fill this field.",
                "form_submitted": True,  # 🟢 New flag!
            })

        # Basic filtering
        courses = Course.objects.all()

        # Latitude and Longitude filtering
        if latitude and longitude:
            try:
                lat = float(latitude)
                lon = float(longitude)
                courses = courses.filter(
                    latitude__gte=lat - 0.5,
                    latitude__lte=lat + 0.5,
                    longitude__gte=lon - 0.5,
                    longitude__lte=lon + 0.5
                )
            except ValueError:
                pass

        # Location Filtering
        elif user_location and user_location.lower() != "all":
            courses = courses.filter(location__icontains=user_location)

        # User Interest Filtering
        if user_interest:
            safe_keyword = re.escape(user_interest.strip())  # Using regex safely
            # Use a regex to match the keyword exactly as a skill
            courses = courses.filter(skill__iregex=rf"\b{safe_keyword}\b")

        # Save search to session
        request.session["course_ids"] = list(courses.values_list("id", flat=True))
        request.session["user_interest"] = user_interest
        request.session["user_location"] = user_location
        request.session["searched"] = True
        request.session["from_post"] = True  # flag to persist over redirect
        request.session["latitude"] = latitude
        request.session["longitude"] = longitude

        return redirect('find_courses_view')

    # Handle pagination or GET after POST
    course_ids = request.session.get("course_ids", [])
    courses = Course.objects.filter(id__in=course_ids) if course_ids else Course.objects.none()

    paginator = Paginator(courses, 10)
    recommendations = paginator.get_page(page_number)

    context = {
        "recommendations": recommendations,
        "user_interest": request.session.get("user_interest", ""),
        "user_location": request.session.get("user_location", ""),
        "searched": request.session.get("searched", False),
        "form_error": "",
        "form_submitted": False,
        "latitude": request.session.get("latitude", ""),
        "longitude": request.session.get("longitude", ""),
    }

    # Only remove the flag AFTER using it
    request.session.pop("from_post", None)

    return render(request, "course.html", context)









from django.http import JsonResponse
from django.shortcuts import render
with open('knowledge_graph_uiuc.gpickle', 'rb') as f:
    knowledge_graph = pickle.load(f)
data_cleaned = pd.read_pickle('processed_data_with_embeddings.pkl')
with open('knowledge_graph.gpickle', 'rb') as f:
    knowledge_graph = pickle.load(f)

import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

knowledge_graph = {
    "Engineering": ["Physics", "Chemistry", "Mathematics", "Computer Science"],
    "Physics": ["Algebra", "Trigonometry"],
    "Chemistry": ["Basic Science", "Organic Chemistry"],
    "Mathematics": ["Algebra", "Geometry"],
    "Computer Science": ["Programming Basics", "Data Structures"],
    "Algebra": ["Arithmetic"],
    "Organic Chemistry": ["Basic Science"],
    "Medicine":["Physics", "Chemistry", "Biology", "Mathematics"],
    "Astronomy":["Physics", "Mathematics", "Chemistry"],
    "Data Science":["Physics", "Mathematics", "Computer Science"]
}

@csrf_exempt
def find_prerequisites_view(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        course_name = request.POST.get('course_name', "").strip()

        if not course_name or course_name not in knowledge_graph:
            return JsonResponse({"error": "Course not found"}, status=400)

        prerequisites = [{"course": prereq} for prereq in knowledge_graph.get(course_name, [])]

        data = {
            'nodes': [{'id': course_name, 'group': 1}] + [
                {'id': prereq.get('course', 'Unknown'), 'group': 2} for prereq in prerequisites
            ],
            'links': [
                {'source': prereq.get('course', 'Unknown'), 'target': course_name} for prereq in prerequisites
            ],
        }
        return JsonResponse(data)

    return render(request, 'prerequest.html', {'course_name': "Engineering"})



