import json

from django.http import JsonResponse
from django.views import View

from users.models import User

class SignInView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
            
            user = User.objects.get(data=['email'])
            if not user:
                return JsonResponse({'message':'INVAILD_USER'},status=401)
            data['password'] == 
        
        except:



'''
로그인 과정
1. 아이디 받기
2. 비번 받기
3. 로그인 하기 
    변수
    - 아이다가 안 맞을 때
    - 비번이 안 맞을 때(암호화)
    
    에러 아이디 공백
        비번 공백
'''