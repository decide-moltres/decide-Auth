from django.contrib.auth import backends
from django.contrib.auth.models import User

class EmailAuthBackend(backends.ModelBackend):
    
    """ 
        Backend que usa el par correo electrónico y contraseña para iniciar sesión, si la primera comprobación
        falla, entonces lo comprueba mediante el par nombre de usuario y contraseña.
    """

    def authenticate(self, username=None, password=None):
        """ Autentificación del usuario usando su correo electrócnico como si fuese su nombre de usuario """
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None

    def get_user(self, user_id):
        """ Mediante la id se consigue al User"""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
