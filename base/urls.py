from django.urls import path
from . import views

urlpatterns = [
    path('',views.top50),
    path('search', views.SearchRecommend, name="search"),
    path('searchResult', views.SearchRecommendAfterSearch, name="searchResult"),
    path('categories', views.categories, name="categories"),
    path('categoriesCourseName', views.categoriesCourseName, name="categoriesCourseName"),
    path('signup',views.signup, name = "signup"),
    path('login',views.login, name = "login"),
    path('signout',views.signout, name = "signout"),
    path('saved_courses',views.saved_courses, name = "saved_courses"),
    path('sc_delete', views.sc_delete, name='sc_delete'),
    
]