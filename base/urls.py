from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name="home"),
    path('login/', views.login_page, name ="login"),
    path('logout/', views.logout_user, name ="logout"),
    path('register/', views.register_page, name ="register"),
    path('event/<str:pk>/', views.event_Page, name="event"),
    path('user/<str:pk>/', views.user_page, name="profile"),
    path('registration-confirmation/<str:pk>/', views.registration_confirmation, name="registration"),

    path('account/', views.account_page, name = "account"),

    path('project-submission<str:pk>', views.project_submission, name="project-submission"),

    path('update-submission<str:pk>', views.update_submission, name="update-submission"),

]
