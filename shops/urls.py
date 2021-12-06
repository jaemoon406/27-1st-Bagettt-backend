from django.urls        import path
from shops.views        import CartView

urlpatterns = [
    path('/cart', CartView.as_view())
]