import json, re

from django.http  import JsonResponse
from django.views import View

from users.models import User

class SignupView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
            email_regex    = r'^[a-zA-Z0-9.-_]+\@[a-zA-Z0-9.-]+\.[a-zA-Z]+$'
            password_regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}'

            if not re.match(email_regex,data['email']):
                return JsonResponse({'message':'INVALID_EMAIL'}, status=201)
            if not re.match(password_regex,data['password']):
                return JsonResponse({'message':'INVALID_PASSWORD'}, status=201)
            User.objects.create(
                email     = data['email'],
                password  = data['password'],
                name      = data['name'],
                address   = data['address'],
                phone_number = data['phone_number']
                    )
            return JsonResponse({'message':'Congratulation'}, status=201)
        except: 
            return JsonResponse({'message':'ACCOUNT_EXISTS'})
