from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

class StaticTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Retrieve the 'Authorization' header from the request's META data.
        auth_token = request.META.get('HTTP_AUTHORIZATION')

        if auth_token == f'Token SafarBazi':
            # Return a tuple of (user, auth) where user can be None.
            return (None, None)
        else:
            pass

        # Raise an AuthenticationFailed exception with a 403 status code (Forbidden) by default.
        raise AuthenticationFailed('Invalid token')
