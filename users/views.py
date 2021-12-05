import json, bcrypt, jwt
from json.decoder import JSONDecodeError

from django.http  import JsonResponse
from django.views import View

from my_settings  import ALGORITHM, SECRET_KEY
from users.models import User

class SignInView(View):
    def post(self,request):
        try:
            data  = json.loads(request.body)
            user  = User.objects.get(email=data['email'])

            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                token = jwt.encode({'id':user.id},SECRET_KEY,ALGORITHM)
                return JsonResponse({'message':'SUCCESS', 'token':token}, status=201)
            return JsonResponse({'message':'PASSWORD_ERROR'},status=401)
        
        except User.DoesNotExist:
            return JsonResponse({'message':'EMAIL_ERROR'},status=401)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=401)

        except JSONDecodeError:
            return JsonResponse({'message':'INVAILD_ERROR'},status=404)