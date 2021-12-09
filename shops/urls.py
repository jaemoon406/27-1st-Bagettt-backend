from django.urls        import path
from shops.views        import CartView, OrderView

urlpatterns = [
    path('/cart', CartView.as_view()),
    path('/order', OrderView.as_view())
]