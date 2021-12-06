import json

from decimal                        import Decimal
from django.core.checks             import messages
from django.core.exceptions         import ValidationError
from django.db.models               import Sum, Q
from django.http                    import JsonResponse
from django.views                   import View

from shops.models                   import Cart, Option
from packages.models                import Package
from users.models                   import User
from core.utils.decorator_sign_in   import sign_in_decorator


class CartView(View):
    @sign_in_decorator
    def post(self, request):
        try:
            data            = json.loads(request.body)
            user            = request.user
            quantity        = data["quantity"]
            price           = data["price"]
            package_id      = data["package_id"] 
            shipping_option = data["shipping_option"]   
            cart            = Cart.objects.filter(Q(package = package_id)&Q(user = user.id))

            if int(quantity) < 1 :
                return JsonResponse({'message':'DESELECTED_QUANTITY'})
            
            if not cart.exists():
                Cart.objects.create(
                    user            = User.objects.get(id = user.id),
                    price           = price,
                    quantity        = quantity,
                    shipping_option = Option.objects.get(id=shipping_option),
                    package         = Package.objects.get(id=package_id)
                )
                
            else:
                cart = Cart.objects.filter(user=user.id).get(package=package_id)
                cart.quantity += int(quantity)
                cart.price    += int(price)
                cart.save()
                
            return JsonResponse({'result':'ADD_CART'}, status = 200)
        
        except ValidationError as e:
            return JsonResponse({'message':e.message}, status = 400)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

    @sign_in_decorator
    def get(self, request):
        try:
            user        = request.user
            carts       = Cart.objects.filter(user = user.id)
            
            total       = carts.values('price')
            total_price = total.aggregate(total_price=Sum('price'))
            
            result=[{
            
                "total_price" : total_price,
                "cart"        :
                [{
                'id'          : cart.id,
                'image'       : cart.package.thumbnail_image, 
                'name'        : cart.package.name, 
                'price'       : cart.price,
                'quantity'    : cart.quantity,
                'option'      : cart.shipping_option.shipping_option
                    } for cart in carts],
                }
            ]
            return JsonResponse({'result':result}, status = 200)

        except ValidationError as e:
            return JsonResponse({'message':e.message}, status = 400 )

    @sign_in_decorator
    def delete(self, request):
        try:
            user = request.user
            cart_id = request.GET.get('id')
            cart = Cart.objects.filter(Q(id = cart_id)&Q(user=user.id))
            
            if cart.exists():
                cart.delete()

            return JsonResponse({'result':'DELETE_CART'}, status = 200)
        
        except ValidationError as e:
            return JsonResponse({'message':e.message}, status = 400 )

    @sign_in_decorator
    def patch(self, request):
        try:
            
            data            = json.loads(request.body)
            quantity        = data['quantity']
            user            = request.user
            cart_id         = request.GET.get('id')
            
            if int(quantity) < 1:
                return JsonResponse({'messages':'DESELECTED_QUANTITY'}, status = 400)

            cart = Cart.objects.get(id=cart_id)
            cart.quantity = quantity
            price = cart.package.price
            cart.price = Decimal(int(cart.quantity) * int(price))
            cart.save()    
                
            return JsonResponse({'result':'QUANTITY_IN_CART'}, status = 200)
        
        except ValidationError as e:
            return JsonResponse({'message':e.message}, status = 400 )