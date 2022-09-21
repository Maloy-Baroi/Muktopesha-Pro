from django.urls import path
from App_auth.views import *

app_name = 'App_auth'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('registration/', registration_view, name='registration'),
    path('logout/', logout_view, name='logout'),
    path('profile-setup-view/', profile_setup_view, name='profile-setup-view'),
    path('freelancer-profile-view/', freelancer_profile_view, name='freelancer-profile-view'),
    path('buyer-profile-view/', buyer_profile_view, name='buyer-profile-view'),
    path('add-new-skill/', add_new_skill, name='add-new-skill'),
    path('add-new-language/', add_new_language, name='add-new-language'),
]

