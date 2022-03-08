import uuid, datetime, json

from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.http import JsonResponse
from django.views import View
from django.db import transaction

from shops.models import Cart, Option, Order, OrderItem
from utils.decorator import jwtdecorator


class CartView(View):
    @jwtdecorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user
            quantity = data["quantity"]
            price = data["price"]
            package_id = data["package_id"]
            shipping_option = data["shipping_option"]
            option = Option.objects.get(shipping_option=shipping_option).id

            if int(quantity) < 1:
                return JsonResponse({'message': 'DESELECTED_QUANTITY'}, status=400)

            cart, created = Cart.objects.get_or_create(
                user=user,
                package_id=package_id,
                defaults={
                    'shipping_option_id': option
                }
            )
            cart.quantity += quantity
            cart.price += price
            cart.save()

            return JsonResponse({'result': 'ADD_CART'}, status=201)

        except ValidationError as e:
            return JsonResponse({'message': e.message}, status=400)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    @jwtdecorator
    def get(self, request):
        try:
            user = request.user
            carts = Cart.objects.filter(user=user.id)
            total_price = carts.values('price').aggregate(total_price=Sum('price'))

            result = [{
                'total_price': total_price,
                'cart': [{
                    'id': cart.id,
                    'image': cart.package.thumbnail_image,
                    'name': cart.package.name,
                    'price': cart.price,
                    'quantity': cart.quantity,
                    'option': cart.shipping_option.shipping_option
                } for cart in carts]
            }]

            return JsonResponse({'result': result}, status=200)

        except ValidationError as e:
            return JsonResponse({'message': e.message}, status=401)

    @jwtdecorator
    def delete(self, request):
        try:
            data = json.loads(request.body)
            cart_list = data['id']
            carts = Cart.objects.filter(id__in=cart_list)

            carts.delete()

            return JsonResponse({'result': 'DELETE_CART'}, status=200)

        except ValidationError as e:
            return JsonResponse({'message': e.message}, status=401)

    @jwtdecorator
    def patch(self, request):
        try:
            data = json.loads(request.body)
            quantity = data['quantity']
            id = data['id']

            if int(quantity) < 1:
                return JsonResponse({'messages': 'DESELECTED_QUANTITY'}, status=400)

            cart = Cart.objects.get(id=id)
            price = cart.package.price

            cart.quantity = quantity
            cart.price = Decimal(int(cart.quantity) * int(price))
            cart.save()

            return JsonResponse({'result': 'QUANTITY_IN_CART'}, status=200)

        except ValidationError as e:
            return JsonResponse({'message': e.message}, status=401)


class OrderView(View):
    @jwtdecorator
    def post(self, request):
        data = json.loads(request.body)
        user = request.user
        cart_ids = data['cart_id']

        with transaction.atomic():
            order = Order.objects.create(order_number=uuid.uuid4(), user_id=user.id)

            OrderItem.objects.bulk_create([
                OrderItem(
                    quantity=cart.quantity,
                    order_id=order.id,
                    shipping_option_id=cart.shipping_option_id,
                    package_id=cart.package.id
                ) for cart in Cart.objects.filter(id__in=cart_ids, user_id=user.id)
            ])

            order.sub_total = Cart.objects.filter(id__in=cart_ids).aggregate(sub_total=Sum('price'))['sub_total']
            order.save()
            Cart.objects.filter(id__in=cart_ids, user_id=user.id).delete()

        new_order = Order.objects.all().order_by('-created_at').first()

        result = {
            'user_name': user.name,
            'address': user.address,
            'phone_number': user.phone_number,
            'email': user.email,
            'order_number': order.order_number,
            'date': datetime.datetime.date(order.created_at),
            'total_price': order.sub_total,
            'package': [{
                'option': order_item.shipping_option_id,
                'package_name': order_item.package.name,
                'package_price': order_item.package.price * order_item.quantity,
                'quantity': order_item.quantity,
                'package_image': order_item.package.thumbnail_image
            } for order_item in OrderItem.objects.filter(order_id=new_order.id)]
        }

        return JsonResponse({'result': result})
