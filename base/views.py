from django.shortcuts import render, redirect
import pickle
from pickle import load
import pandas as pd
import numpy as np
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from base.models import Watchlater
from django.db.models import Case, When
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
import json
from django.http import JsonResponse, HttpResponseBadRequest


# Create your views here.
def top50(request):
    # Load the DataFrame from the pickle file
    with open('./savedmodels/popular_df_review.pkl', 'rb') as f:
        popular_df = load(f)

    # Extract the columns from the DataFrame
    ID = list(popular_df['ID'].values)
    course_title = list(popular_df['course name'].values)
    source = list(popular_df['source'].values)
    Url = list(popular_df['Url'].values)
    is_paid = list(popular_df['is-paid'].values)
    Instructor = list(popular_df['Instructor'].values)
    level = list(popular_df['level'].values)
    no_of_enrollment = list(popular_df['no of enrollments'].values)
    duration = list(popular_df['duration(hr)'].values)
    rating = list(popular_df['rating'].values)
    review = list(popular_df['review'].values)
    published_year = list(popular_df['published year'].values)
    genre = list(popular_df['genre'].values)


    # Zip the lists
    courses_data = zip(ID, course_title, source, Url, is_paid, Instructor, level, no_of_enrollment, duration, rating, review, published_year, genre)

    # Pass the zipped list as context to the template
    context = {
        'courses_data': courses_data,
    }

    return render(request, 'index.html',context)

def top50_reviews(request):
    # Load the DataFrame from the pickle file
    with open('./savedmodels/popular_df_review.pkl', 'rb') as f:
        popular_df = load(f)

    # Extract the columns from the DataFrame
    ID = list(popular_df['ID'].values)
    course_title = list(popular_df['course name'].values)
    source = list(popular_df['source'].values)
    Url = list(popular_df['Url'].values)
    is_paid = list(popular_df['is-paid'].values)
    Instructor = list(popular_df['Instructor'].values)
    level = list(popular_df['level'].values)
    no_of_enrollment = list(popular_df['no of enrollments'].values)
    duration = list(popular_df['duration(hr)'].values)
    rating = list(popular_df['rating'].values)
    review = list(popular_df['review'].values)
    published_year = list(popular_df['published year'].values)
    genre = list(popular_df['genre'].values)


    # Zip the lists
    courses_data = zip(ID, course_title, source, Url, is_paid, Instructor, level, no_of_enrollment, duration, rating, review, published_year, genre)

    # Pass the zipped list as context to the template
    context = {
        'courses_data': courses_data,
    }

    return render(request, 'index.html',context)

def top50_enrollment(request):
    # Load the DataFrame from the pickle file
    with open('./savedmodels/popular_df_enrollment.pkl', 'rb') as f:
        popular_df = load(f)

    # Extract the columns from the DataFrame
    ID = list(popular_df['ID'].values)
    course_title = list(popular_df['course name'].values)
    source = list(popular_df['source'].values)
    Url = list(popular_df['Url'].values)
    is_paid = list(popular_df['is-paid'].values)
    Instructor = list(popular_df['Instructor'].values)
    level = list(popular_df['level'].values)
    no_of_enrollment = list(popular_df['no of enrollments'].values)
    duration = list(popular_df['duration(hr)'].values)
    rating = list(popular_df['rating'].values)
    review = list(popular_df['review'].values)
    published_year = list(popular_df['published year'].values)
    genre = list(popular_df['genre'].values)


    # Zip the lists
    courses_data = zip(ID, course_title, source, Url, is_paid, Instructor, level, no_of_enrollment, duration, rating, review, published_year, genre)

    # Pass the zipped list as context to the template
    context = {
        'courses_data': courses_data,
    }

    return render(request, 'index.html',context)

def recommend_course(title, numrec):
    with open('./savedmodels/df.pkl', 'rb') as g:
        df = load(g)
    with open('./savedmodels/cosine_sim_mat.pkl', 'rb') as h:
        cosine_mat = load(h)

    course_index = pd.Series(df.index, index=df['course name']).drop_duplicates() #df
    index = course_index[title]

    scores = list(enumerate(cosine_mat[index]))  #cosine_sim_mat
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

    selected_course_index = [i[0] for i in sorted_scores[1:numrec+1]]
    selected_course_score = [i[1] for i in sorted_scores[1:numrec+1]]

    rec_df = df.iloc[selected_course_index]
    rec_df['Similarity_Score'] = selected_course_score

    final_recommended_courses = rec_df[['ID', 'course name', 'source', 'Url','is-paid','Instructor','level','no of enrollments','duration(hr)','rating','review','published year','genre']]

    return final_recommended_courses.head(numrec)

def search_term(term):
    with open('./savedmodels/df.pkl', 'rb') as g:
        df = load(g)
    result_df = df[df['course name'].str.contains(term, case=False)]
    top_6 = result_df.sort_values(by='review', ascending=False).head(7)
    return top_6

def extract_features(rec_df):
    ID = list(rec_df['ID'].values)
    course_title = list(rec_df['course name'].values)
    source = list(rec_df['source'].values)
    Url = list(rec_df['Url'].values)
    is_paid = list(rec_df['is-paid'].values)
    Instructor = list(rec_df['Instructor'].values)
    level = list(rec_df['level'].values)
    no_of_enrollment = list(rec_df['no of enrollments'].values)
    duration = list(rec_df['duration(hr)'].values)
    rating = list(rec_df['rating'].values)
    review = list(rec_df['review'].values)
    published_year = list(rec_df['published year'].values)
    genre = list(rec_df['genre'].values)

    return ID, course_title, source, Url, is_paid, Instructor, level, no_of_enrollment, duration, rating, review, published_year, genre

def SearchRecommend(request):
    return render (request, 'search.html')


def SearchRecommendAfterSearch(request):
    
    if request.method == 'POST':
        try:
            my_dict = request.POST
            title_name = my_dict['course'].strip()
            if not title_name:
                error_message = "Please enter something before searching."
                return render(request, 'aftersearch.html', {'error_message': error_message})
            

            num_rec = 7

            rec_df = recommend_course(title_name, num_rec)
            ID, course_title, source, Url, is_paid, Instructor, level, no_of_enrollment, duration, rating, review, published_year, genre = extract_features(rec_df)

            dict_map = zip(ID, course_title, source, Url, is_paid, Instructor, level, no_of_enrollment, duration, rating, review, published_year, genre)

            if any(dict_map):
                return render(request, 'aftersearch.html', {'coursemap': dict_map, 'coursename': title_name, 'showtitle': True, 'source': 'recommendations'})
            else:
                return render(request, 'aftersearch.html', {'showerror': True, 'coursename': title_name})
        except Exception as e:
            print(e)
            
            result_df = search_term(title_name)
            if result_df.shape[0] > 7:
                result_df = result_df.head(7)
            ID, course_title, source, Url, is_paid, Instructor, level, no_of_enrollment, duration, rating, review, published_year, genre = extract_features(result_df)
            course_map = zip(ID, course_title, source, Url, is_paid, Instructor, level, no_of_enrollment, duration, rating, review, published_year, genre)
            if any(course_map):
                return render(request, 'aftersearch.html', {'coursemap': course_map, 'coursename': title_name, 'showtitle': True, 'source': 'search_results'})
            else:
                return render(request, 'aftersearch.html', {'showerror': True, 'coursename': title_name})

    return render(request, 'aftersearch.html')

def categories(request):
    with open('./savedmodels/df.pkl', 'rb') as g:
        df = pickle.load(g)

    q = request.GET.get('q', '')
    topics = df[df['genre'].str.contains(q, case=False)]['genre'].unique()
    return render(request, 'categories.html',{'topics': topics, 'query': q})

def categoriesCourseName(request):
    with open('./savedmodels/df.pkl', 'rb') as g:
        df = pickle.load(g)

    q = request.GET.get('genre', '')
    rec_df = df[df['genre'].str.contains(q, case=False)]
    ID, course_title, source, Url, is_paid, Instructor, level, no_of_enrollment, duration, rating, review, published_year, genre = extract_features(rec_df)
    course_map = zip(ID, course_title, source, Url, is_paid, Instructor, level, no_of_enrollment, duration, rating, review, published_year, genre)

    return render(request,'insidecategory.html',{'course_map': course_map, 'showerror': len(rec_df) == 0,'q':q})


def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('/signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('/signup')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('/signup')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('/signup')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('/signup')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = True
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!!")
        return redirect('login')

    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        if user is not None:
            auth_login(request, user)
            
            # messages.success(request, "Logged In Sucessfully!!")
            return redirect("/")
        else:
            messages.error(request, "Password or username Incorrect Try again!!")
            return redirect('login')

    return render(request, 'login.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('/login')

@login_required(login_url= 'login')
def saved_courses(request):
    with open('./savedmodels/df.pkl', 'rb') as g:
        df = pickle.load(g)
    
    if request.method == "POST":
        try:
            user = request.user
            course_id = request.POST['course_id']
            watch = Watchlater.objects.filter(user=user)
            
            for i in watch:
                if course_id == i.course_id:
                    messages.error(request, "This course is already Saved")
                    
                    
                    break
            else:
                saved_courses = Watchlater(user=user, course_id=course_id)
                saved_courses.save()
                messages.success(request, "Course is Saved Successfully")
                
            
            return redirect("/saved_courses")
        except MultiValueDictKeyError:
            messages.error(request, "Invalid request. Please provide a course_id.")
            return redirect("/saved_courses")  # Redirect to the saved_courses page

    wl = Watchlater.objects.filter(user=request.user)
    ids = [i.course_id for i in wl]
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    courses = Watchlater.objects.filter(course_id__in=ids).order_by(preserved)

    # Assuming df is a pandas DataFrame
    course_map = []
    for course_id in ids:
        ID = int(course_id)
        course_title = df.loc[df['ID'] == ID, 'course name'].values[0]
        source = df.loc[df['ID'] == ID, 'source'].values[0]
        Url = df.loc[df['ID'] == ID, 'Url'].values[0]
        is_paid = df.loc[df['ID'] == ID, 'is-paid'].values[0]
        Instructor = df.loc[df['ID'] == ID, 'Instructor'].values[0]
        level = df.loc[df['ID'] == ID, 'level'].values[0]
        no_of_enrollment = df.loc[df['ID'] == ID, 'no of enrollments'].values[0]
        duration = df.loc[df['ID'] == ID, 'duration(hr)'].values[0]
        rating = df.loc[df['ID'] == ID, 'rating'].values[0]
        review = df.loc[df['ID'] == ID, 'review'].values[0]
        published_year = df.loc[df['ID'] == ID, 'published year'].values[0]
        genre = df.loc[df['ID'] == ID, 'genre'].values[0]

        course_map.append((ID, course_title, source, Url, is_paid, Instructor, level, no_of_enrollment, duration, rating, review, published_year, genre))

    return render(request, 'saved.html', {'course': courses, 'course_map': course_map})


@login_required(login_url= 'login')
def sc_delete(request):
    with open('./savedmodels/df.pkl', 'rb') as g:
        df = pickle.load(g)
    id = request.POST['course_id']
    course = get_object_or_404(Watchlater, course_id=id, user=request.user)
    course_name = df.loc[df['ID'] == int(id), 'course name'].values[0]

    
    if request.user != course.user:
        messages.error(request, "Invalid user")
    if request.method == 'POST':
        course.delete()
        messages.success(request, f"'{course_name}' is unsaved Successfully from Saved Sourses")
        return redirect('/saved_courses')
    return render(request, 'saved.html', {'obj':course_name})


# from django.contrib.auth.views import PasswordResetView

# class CustomPasswordResetView(PasswordResetView):
#     template_name = 'password_reset_form.html'
#     html_email_template_name = 'password_reset_email.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Add uidb64 and token to the context
#         uidb64 = self.get_context_data().get('uidb64', '')
#         token = self.get_context_data().get('token', '')
#         success_url = self.success_url + f'?uidb64={uidb64}&token={token}'

#         return HttpResponseRedirect(success_url)

# def coursedetails(request):
#     with open('./savedmodels/df.pkl', 'rb') as g:
#         df = pickle.load(g)
#     ID = request.GET.get('ID')
    
#     course_title = df.loc[df['ID'] == int(ID), 'course name'].values[0]
#     source = df.loc[df['ID'] == int(ID), 'source'].values[0]
#     Url = df.loc[df['ID'] == int(ID), 'Url'].values[0]
#     is_paid = df.loc[df['ID'] == int(ID), 'is-paid'].values[0]
#     Instructor = df.loc[df['ID'] == int(ID), 'Instructor'].values[0]
#     level = df.loc[df['ID'] == int(ID), 'level'].values[0]
#     no_of_enrollment = df.loc[df['ID'] == int(ID), 'no of enrollments'].values[0]
#     duration = df.loc[df['ID'] == int(ID), 'duration(hr)'].values[0]
#     rating = df.loc[df['ID'] == int(ID), 'rating'].values[0]
#     review = df.loc[df['ID'] == int(ID), 'review'].values[0]
#     published_year = df.loc[df['ID'] == int(ID), 'published year'].values[0]
#     genre = df.loc[df['ID'] == int(ID), 'genre'].values[0]
#     is_paid_str = str(is_paid)
#     no_of_enrollment_int = int(no_of_enrollment)
#     duration_int = int(duration)
#     rating_int = int(rating)
#     review_int = int(review)
#     course_details = {
#         'course_title': course_title,
#         'source': source,
#         'Url': Url,
#         'is_paid': bool(is_paid),
#         'Instructor': Instructor,
#         'level': level,
#         'no_of_enrollment': no_of_enrollment,
#         'duration': duration,
#         'rating': rating,
#         'review': review,
#         'published_year': published_year,
#         'genre': genre,
#     }

#     return JsonResponse(course_details)
    

def coursedetails(request):
    if request.method == 'GET':
        # Get the course ID from the query parameters
        ID = request.GET.get('ID')

        # Assuming you have a DataFrame named 'df'
        with open('./savedmodels/df.pkl', 'rb') as g:
            df = pickle.load(g)

        # Retrieve course details based on the ID
        course_details = df[df['ID'] == int(ID)].to_dict(orient='records')[0]

        # Return course details as JSON response
        return JsonResponse(course_details)
    else:
        # Handle other HTTP methods if needed
        return HttpResponseBadRequest("Invalid HTTP method")
    