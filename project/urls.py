"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from .views import GoogleLogin, callback, protected

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('auth/', include('dj_rest_auth.urls')),
    # path('accounts/', include('allauth.urls'), name='socialaccount_signup'),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),

    path('auth/google/callback/', callback),
    path('protected/', protected),
]

# https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=http://127.0.0.1:8000/auth/google/callback/&prompt=consent&response_type=code&client_id=594963492296-c15nipesdhrshqmr88obgen79ebar1d5.apps.googleusercontent.com&scope=openid%20email%20profile&access_type=offline

# https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=http://127.0.0.1:8000/authentication/google/callback/&prompt=consent&response_type=code&client_id=594963492296-c15nipesdhrshqmr88obgen79ebar1d5.apps.googleusercontent.com&scope=openid%20email%20profile&access_type=offline

# https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=https://labrary-staging.herokuapp.com/authentication/google/callback/&prompt=consent&response_type=code&client_id=421768511888-ni3eago41fhlq98v5o76ibnj234risl4.apps.googleusercontent.com&scope=openid%20email%20profile&access_type=offline
