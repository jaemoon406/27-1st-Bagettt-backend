import re
import jwt
from django.http import JsonResponse
from bagettt.settings.common import ALGORITHM, SECRET_KEY
from users.models import User

from django.core.exceptions import ValidationError

def email_regex_match(email):
    EMAIL_REGEX = '^[a-zA-Z0-9+-_.]+\@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(EMAIL_REGEX, email):
        raise ValidationError('EMAIL_INVALID')

def password_regex_match(password):
    PASSWORD_REGEX = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}'
    if not re.match(PASSWORD_REGEX, password):
        raise ValidationError('PASSWORD_INVALID')


def jwtdecorator(func):
    def wrapper(self, request, *args, **kwarg):
        try:
            token = request.headers.get('Authorization', None)
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            request.user = User.objects.get(id=payload['id'])

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=400)
        return func(self, request, *args, **kwarg)

    return wrapper
