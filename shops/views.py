
from django.views import View
from django.http import JsonResponse

from packages.models import Package
from shops.models import Cart, Order, OrderItem
from users.models import User
from core.decorator import decorator

class OrderView(View):
    @decorator
    def post(self,request): 
        data = json.loads(request.body)
        user_id = request.user # 유저 id
        cart_id = data['cart_id'] # 패키지 Id
        cart_id = Cart.objects.get(id=cart_id)
        package_id = Cart.objects.get(id=cart_id).package_id

        for p in cart_id:
            quantity = cart_id.quantity
            package_price = Package.objects.get(id=package_id).price
            sub_total = package_price * quantity 
            order_number = uuid.uuid4() # 무작위 생성 0
            shipping_option_id = Cart.objects.get(id=)
            Order.objects.create(
                order_number = order_number,
                sub_total = sub_total,
                shipping_option_id = shipping_option_id,
                user_id = user_id
            )
            OrderItem.objects.create(
                quantity = quantity
                order_id = order_
                order_number =
            )

        # 입력 C
        # quantity
        # package_id
        # user_id (토큰)
        # 데이터 저장 패키지당 한줄
        # 수량
        # 주문번호
        # 패키지id
    @decorator
    def get(self,request):
        data = json.loads(request.body)
        user_id = request.user # 유저 id
        user = User.objects.get(user_id=user_id) # 0
        user_name = user.name # 유저이름 0
        quantity = request.get(package_id) # 갯수 공식
        order_number = uuid.uuid4() # 무작위 생성 0
        date = datetime.datetime.date(Order.objects.get(user_id=user_id).created_at) # 0

        order_table = Order.objects.create(
            order_number = order_number,
            sub_total    = quantity * package_price
        )

        # ================================  계산됐을 때
        # 삭제 D
            Cart.objects.filter(user_id=user_id).delete()
            Cart.objects.filter(user_id=1,package_id=5)
        # 주문한 물품 전체(user_id > package_id)
        # =================================   출력 (프론트)
            return JsonResponse({   
                'user_name'    : user_name,
                'address'      : user.address,
                'phone_number' : user.phone_number,
                'email'        : user.email,
                'package_name' : user, # 수정 for list 형식 2 [list]
                'order_number' : order_number,
                'date'         : date,
                'sub_total'    : quantity * sub_price
            })
    
        '''
        DIC 형태로 올 때 받는 방식, 출력 포함
        각 각 다른 table 일 때 필터링 user,package가 각 각 다른 테이블인데 구분 하는 법
        
        acid 방식 order 와 order Item 이 생성 될 때 cart 는 삭제
        order id로 Order와 OrderItem을 연결하는 법
        '''
        # package_id = Cart.objects.filter(user_id=user_id)
        # order_package = Package.objects.get(package_id=data['package_id']) # 패키지 id값