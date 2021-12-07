from django.http                import JsonResponse
from django.views               import View
from django.db.models           import Q

from packages.models            import Package, Product


class PackagesListView(View):
    def get(self, request):   
        
        brand     = request.GET.getlist('brand', None) 
        ordering  = request.GET.get('order', 'id')

        q = Q()

        if brand:
            q &= Q(products__brand_name__in=brand)
            
        packages = Package.objects.filter(q).order_by(ordering).distinct()
        
        results = [{
            "id"    : package.id,
            "name"  : package.name,
            "image" : package.thumbnail_image,
            "price" : package.price,
            "brand" : [product.brand_name for product in package.products.all()],
        } for package in packages]

        return JsonResponse({'result':results}, status=200)    
        
class ProductsView(View):
    def get(self, request, package_id):
        try:
            products = Product.objects.filter(packages__id=package_id)
            package = Package.objects.get(id = package_id)
            
            result = [{
                "package_id"           : package_id,
                "package_name"         : package.name,
                "package_description"  : package.description,
                "package_thumbnail"    : package.thumbnail_image,
                "price"                : package.price,
                "product_details"      : [{   
                            "name"      : product.name,
                            "brand_name": product.brand_name,
                            "image"     : product.image_url,
                            "kcal"      : product.kcal,
                            "nutrition" : product.nutrition
                    } for product in products],
                }]
        
            return JsonResponse({'result':result}, status=200)
        
        except Package.DoesNotExist:
            return JsonResponse({'messages':'NOT_FOUND'}, status=404) 
