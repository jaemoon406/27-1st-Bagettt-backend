import uuid, datetime, json

from django.views    import View
from django.http     import JsonResponse
from django.db       import transaction

from packages.models import Package
from shops.models    import Cart, Order, OrderItem
from users.models    import User
from core.decorator  import decorator

class OrderView(View):
    @decorator
    def post(self,request): 
        try:
            data = json.loads(request.body)
            user = request.user # 유저 id
    # 유저의 카드 번호
            for package in data['package_id']: # cart로
                package            = Cart.objects.get(package_id=package)
                cart               = Cart.objects.get(package_id=package,user_id=user)
                quantity           = cart.quantity
                package_id         = cart.package_id
                shipping_option_id = cart.shippting_option_id
                package_price      = Package.objects.get(id=package_id).price
                sub_total          = package_price * quantity 
                order_number       = uuid.uuid4() # 무작위 생성 0

                with transaction.atomic():
                    Order.objects.create(
                        order_number       = order_number,
                        sub_total          = sub_total,
                        shipping_option_id = shipping_option_id,
                        user_id            = user
                    )
                    OrderItem.objects.create(
                        quantity     = quantity,
                        order_id     = order_,
                        # order_item Table 에 중복으로 쌓이는가? Order 와 Order 아이템 사이에 order_id 가 어떻게 엮이는가
                        order_number = , 
                        # order_number를 가져오기 위한 유일한 컬럼이 없다
                    )
                    Cart.objects.filter(user_id=user).delete()
                    Cart.objects.filter(user_id=1,package_id=5)
                    return JsonResponse({'message':'SUCCES'})
        
        
        except KeyError:
            return JsonResponse()
            # 입력 
            # package_id
            # user_id (토큰)

            # Create 
            # user에 해당하는 Cart에 있는 항목 Order,OrderItem
            
            # Delete
            # Cart에서 받아온 package 전체


                order_number = uuid.uuid4() # 무작위 생성 0
                


        @decorator
        def get(self,request):
            user      = request.user # 유저 id
            user      = User.objects.get(user_id=user) # 0
            quantity  = Cart.objects.get(package_id=package).package_id # 갯수 공식
            date      = datetime.datetime.date(Order.objects.get(user_id=user).created_at) # 0
            order_number = Order.objects.get()
            order_table = Order.objects.create
                order_number = order_number,
                sub_total    = quantity * package_price

            # ================================  계산됐을 때
            # 삭제 D
            # 주문한 물품 전체(user_id > package_id)
            # =================================   출력 (프론트)
            return JsonResponse({   
                'user_name'    : user.name,
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