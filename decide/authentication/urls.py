from django.urls import include, path
from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token


from .views import GetUserView, LogoutView, RegisterView, home
from authentication import views #<--


urlpatterns = [
    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view()),
    path('getuser/', GetUserView.as_view()),
    path('register/', RegisterView.as_view()),

    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),	
    url(r'^oauth/', include('social_django.urls', namespace="social")),
    path('registration/login', views.login),
    path('policy/', views.policy), 

]

LOGIN_URL = 'registration/login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'

