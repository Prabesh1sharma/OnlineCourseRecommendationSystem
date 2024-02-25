from django.urls import path
from . import views

urlpatterns = [
    path('',views.top50),
    path('search', views.SearchRecommend, name="search"),
    path('aftersearch', views.SearchRecommendAfterSearch, name="aftersearch"),
    path('categories', views.categories, name="categories"),
    path('categoriesCourseName', views.categoriesCourseName, name="categoriesCourseName"),
    
]