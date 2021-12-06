
import jwt

from django.http                import JsonResponse

from users.models               import User

from bagettt.settings         import SECRET_KEY, ALGORITHM

def sign_in_decorator(func):
    def access_token(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get("Authorization", None)   
                                                  
            payload = jwt.decode(access_token, SECRET_KEY, algorithms = ALGORITHM)
            user  = User.objects.get(id = payload['id'])
            request.user = user
           
            return func(self, request, *args, **kwargs)
            
        except jwt.exceptions.DecodeError:                                                 
            return JsonResponse({'MESSAGE':'INVALID_TOKEN'}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'INVALID_USER'}, status = 401)       
                                                                                                                                       
    return access_token