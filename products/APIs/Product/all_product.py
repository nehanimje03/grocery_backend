from ...views import *


class AllProductsAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        response_data = {
            "status": True,
            "message": "All Products",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    

class PopularProductsAPIView(APIView):
    def get(self, request):
        products = Product.objects.filter(is_popular=True)
        serializer = ProductSerializer(products, many=True)
        
        response_data = {
            "status": True,
            "message": "Popular Products",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)