import json, bcrypt

from json.decoder           import JSONDecodeError
from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import  ValidationError

from users.models           import User
from .validaitor            import email_regex_match, password_regex_match

class SignUpView(View):
    def post(self, request):
        try:
            data          = json.loads(request.body)
            name          = data['name']
            address       = data['address']
            email         = data['email']
            password      = data['password']
            phone_number  = data['phone_number']
            
            email_regex_match(email)
            password_regex_match(password)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message':'EMAIL_ALREADY_EXISTS'}, status = 400)
            
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            User.objects.create(
                name          = name,
                address       = address,
                email         = email,
                password      = hashed_password,
                phone_number  = phone_number
            )

            return JsonResponse({'message':'SUCCESS'}, status=201) 
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        except ValidationError as e:
            return JsonResponse({'message':e.message}, status=401)

        except JSONDecodeError:
            return JsonResponse({'message':'JSON_INVALID'})
