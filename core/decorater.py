import jwt

from django.http  import JsonResponse

from my_settings  import ALGORITHM, SECRET_KEY
from users.models import User

class TokenDecorator:
    def __init__(self,func):
        self.func = func
    def __call__(self,request,*args,**kargs):
        token = request.header.get('Authorization',None)
        try:
            if token:
                payload      = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
                user         = User.objects.get(id=payload['id'])
                request.user = user

            return self.func(self,request,*args,**kargs)

        except KeyError:
            return JsonResponse({'':''})