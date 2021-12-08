from django.urls        import path
from packages.views     import PackagesListView, ProductsView

urlpatterns = [
    path('', PackagesListView.as_view()),
    path('/details/<int:package_id>', ProductsView.as_view())
]