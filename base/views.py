from django.shortcuts import render
import pickle
from pickle import load
import pandas as pd
import numpy as np

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
    top_6 = result_df.sort_values(by='review', ascending=False).head(6)
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
            title_name = my_dict['course']
            

            num_rec = 6

            rec_df = recommend_course(title_name, num_rec)
            ID, course_title, source, Url, is_paid, Instructor, level, no_of_enrollment, duration, rating, review, published_year, genre = extract_features(rec_df)

            dict_map = zip(ID, course_title, source, Url, is_paid, Instructor, level, no_of_enrollment, duration, rating, review, published_year, genre)

            if any(dict_map):
                return render(request, 'aftersearch.html', {'coursemap': dict_map, 'coursename': title_name, 'showtitle': True})
            else:
                return render(request, 'aftersearch.html', {'showerror': True, 'coursename': title_name})
        except Exception as e:
            print(e)
            result_df = search_term(title_name)
            if result_df.shape[0] > 6:
                result_df = result_df.head(6)
            ID, course_title, source, Url, is_paid, Instructor, level, no_of_enrollment, duration, rating, review, published_year, genre = extract_features(result_df)
            course_map = zip(ID, course_title, source, Url, is_paid, Instructor, level, no_of_enrollment, duration, rating, review, published_year, genre)
            if any(course_map):
                return render(request, 'aftersearch.html', {'coursemap': course_map, 'coursename': title_name, 'showtitle': True})
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

    return render(request,'insidecategory.html',{'course_map': course_map, 'showerror': len(rec_df) == 0})