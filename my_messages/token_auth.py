from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer


class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        headers = dict(scope['headers'])
        scope['user'] = AnonymousUser()
        if b'authorization' in headers:
            try:
                token_name, token_key = headers[b'authorization'].decode(
                ).split()

                if token_name == 'jwt':
                    data = {'token': token_key}
                    token = VerifyJSONWebTokenSerializer().validate(data)
                    scope['user'] = token['user']
                    print(token)
            except:
                scope['user'] = AnonymousUser()
        return self.inner(scope)


def TokenAuthMiddlewareStack(inner): return TokenAuthMiddleware(
    AuthMiddlewareStack(inner))
