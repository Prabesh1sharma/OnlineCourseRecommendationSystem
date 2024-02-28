from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
# from .views import CustomPasswordResetView

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
    # path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
    
    
]