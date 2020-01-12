from rest_framework.response import Response
from rest_framework.status import (
        HTTP_201_CREATED,
        HTTP_400_BAD_REQUEST,
        HTTP_401_UNAUTHORIZED
)
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import update_session_auth_hash, authenticate, login

from django.contrib.auth.decorators import login_required #<--
from django.shortcuts import render #<--

from .serializers import UserSerializer

from django.contrib.auth.forms import AdminPasswordChangeForm, UserCreationForm, UserChangeForm, PasswordChangeForm

from authentication.forms import (
    RegistrationForm,
    EditProfileForm
)

from django.urls import reverse
from social_django.models import UserSocialAuth
from django.contrib.auth.decorators import login_required
from django.contrib import messages





class GetUserView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        return Response(UserSerializer(tk.user, many=False).data)


class LogoutView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        try:
            tk = Token.objects.get(key=key)
            tk.delete()
        except ObjectDoesNotExist:
            pass

        return Response({})


class RegisterView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        if not tk.user.is_superuser:
            return Response({}, status=HTTP_401_UNAUTHORIZED)

        username = request.data.get('username', '')
        pwd = request.data.get('password', '')
        if not username or not pwd:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        try:
            user = User(username=username)
            user.set_password(pwd)
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
        except IntegrityError:
            return Response({}, status=HTTP_400_BAD_REQUEST)
        return Response({'user_pk': user.pk, 'token': token.key}, HTTP_201_CREATED)

		
def home(request):
	count = User.objects.count()	
	return render(request, 'home.html', {'count': count} 
	)

def policy(request): 
        return render(request, 'privacy_policy.html')
		
		
def register(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('home'))
        else:
            form = RegistrationForm()
            args = {'form': form}
            return render(request, 'registration/signup.html', args)	
    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'registration/signup.html', args)
	
def view_profile(request):
	args = {'user': request.user}
	return render(request, 'registration/profile.html', args)
	
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('view_profile'))
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'registration/edit_profile.html', args)

		
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('view_profile'))
        else:
            return redirect(reverse('change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'registration/change_password.html', args)

	
@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'social/password.html', {'form': form})		
	
def user_login(request):
    '''
    Login
    '''
    if request.method == 'POST':
            user = authenticate(
                username=request.POST['email'],
                password=request.POST['password']
            )
            if user is not None:
                login(request, user)
                return redirect(dashboard)
	


