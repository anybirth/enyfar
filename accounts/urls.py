from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.SignupView.as_view(traveller=False), name='signup'),
    path('signup/traveller/', views.SignupView.as_view(traveller=True), name='signup_traveller'),
    path('email-signup/', views.EmailSignupView.as_view(traveller=False), name='email_signup'),
    path('email-signup/traveller/', views.EmailSignupView.as_view(traveller=True), name='email_signup_traveller'),
    path('social-confirm/', views.SocialConfirmView.as_view(traveller=False), name='social_confirm'),
    path('social-confirm/traveller/', views.SocialConfirmView.as_view(traveller=True), name='social_confirm_traveller'),
    path('complete/', views.CompleteView.as_view(), name='complete'),
    path('activate/<uuid:uuid>', views.ActivateView.as_view(), name='activate'),
    path('activate/error', views.ActivateErrorView.as_view(), name='activate_error'),
    path('activate/again', views.ActivateAgainView.as_view(), name='activate_again'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/traveller/', views.ProfileTravellerView.as_view(), name='profile_traveller'),
]
