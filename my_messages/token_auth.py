from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer


class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        query_string = scope['query_string'].decode()
        if 'token' in query_string:
            try:
                token_key = query_string.split('=')[1]
                data = {'token': token_key}
                token = VerifyJSONWebTokenSerializer().validate(data)
                scope['user'] = token['user']
                print(token)
            except:
                raise ValidationError("No token provided")
        else:
            raise ValidationError("No token provided")
        return self.inner(scope)


def TokenAuthMiddlewareStack(inner): return TokenAuthMiddleware(
    AuthMiddlewareStack(inner))
