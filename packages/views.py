
import json

from django.http                import JsonResponse
from django.views               import View
from django.db.models           import Q

from packages.models            import Package, Product


class PackagesListView(View):
    def get(self, request):   
        
        result   = []
        #print(request)
        
        brand_name = request.GET.get('brand_name', None)
        ordering   = request.GET.get('order', None)
        #category  = request.GET.get('category', None)

        packages   = Package.objects.all()
        products   = Product.objects.filter(Q(brand_name=brand_name)|Q())
        packages   = packages.order_by(ordering) if ordering else packages

        if brand_name:
            for product in products:
                result.append(
                    [{
                        "id"   : package.id,
                        "name" : package.name,
                        "image": package.thumbnail_image,
                        "price": package.price,
                    } for package in product.packages.all()
                ]
            )
        elif ordering:
                result.append(
                    [{
                        "id"   : package.id,
                        "name" : package.name,
                        "image": package.thumbnail_image,
                        "price": package.price
                    } for package in packages
                ]
            )

        else:
            for package in packages:
                result.append(
                    {
                        "id"    : package.id,
                        "name"  : package.name,
                        "image" : package.thumbnail_image,
                        "price" : package.price,
                        "brands": [product.brand_name for product in package.products.all()],
                    }
                )

        return JsonResponse({'result' : result}, status=200)    
        
        # for package in packages.order_by(ordering):
        #     result.append(
        #         {
        #             "id"   : package.id,
        #             "name" : package.name,
        #             "image": package.thumbnail_image,
        #             "price": package.price
        #         }
        #     )
      
        # packages = Package.objects.all()
        # for package in packages:
        #     result.append(
        #         {
        #             "id"    : package.id,
        #             "name"  : package.name,
        #             "image" : package.thumbnail_image,
        #             "price" : package.price,
        #             "brands": [product.brand_name for product in package.products.all()],
                    
        #         }
        #     )
        

# class PackagesView(View):
#     #상세페이지 : 리스트페이지 > 상세페이지
#     def get(self, request, ):
    
#         #3.수량, 옵션 선택
        
        
#         data     = json.loads(request.body)
#         products = Product.objects.filter(packages__id=data["id"])
        
#         #대표이미지 어떻게???
#         #{"image_url" : Package.objects.get(id=data["id"]).thumbnail_image}????
#         result = []
#         for product in products:
#             result.append(
#                 {
#                     "id"    : product.id,
#                     "image" : product.image_url
#                 }                
#             )
#         return JsonResponse({'result': result}, status=200)

    # def update(self, request):
        #수량변경 : 수량 변경 요청이 있을시 cart의 quantity += 1 > update
        
        #option 선택시 

        #def post():
        #장바구니 클릭시 장바구니 테이블 create


class ProductsView(View):
    def get(self, request, package_id):
        try:
            products = Product.objects.filter(packages__id=package_id)
            package = Package.objects.get(id = package_id)
            
            result = [{
                "package_id"           : package_id,
                "package_name"         : package.name,
                "packgae_description"  : package.description,
                "price"                : package.price,
                "product_details"      : [
                        {    "name"      : product.name,
                            "brand_name": product.brand_name,
                            "image"     : product.image_url,
                            "kcal"      : product.kcal,
                            "nutrition" : product.nutrition
                    } for product in products],
                }
            ]
        
            return JsonResponse({'result':result}, status=200)
        
        except Package.DoesNotExist:
            return JsonResponse({'messages':'NOT_FOUND'}, status=401)


        

