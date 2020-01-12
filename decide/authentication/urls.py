from django.urls import include, path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

from .views import GetUserView, LogoutView, RegisterView, home
from authentication import views #<--

from django.contrib.auth.views import (
login, logout)


urlpatterns = [

    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view()),
    path('getuser/', GetUserView.as_view()),
    path('register/', RegisterView.as_view()),

    path('', views.home, name='home'),	

	url(r'^login/$', login, {'template_name': 'registration/login.html'}, name='login'),
    path('signup/', views.register, name='signup'),		   
    path('accounts/', include('django.contrib.auth.urls')),	
    url(r'^oauth/', include('social_django.urls', namespace="social")),
	url(r'^profile/$', views.view_profile, name="view_profile"),
	url(r'^profile/edit/$', views.edit_profile, name="edit_profile"),
	url(r'^profile/password/$', views.change_password, name='change_password'),	
    url(r'^settings/password/$', views.password, name='password'),
    path('policy/', views.policy, name='policy'), 

	


]

LOGIN_URL = 'registration/login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'

