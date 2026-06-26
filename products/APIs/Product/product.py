from ...views import *

class PublicProductsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            product_type = request.GET.get("type", "all").lower()
            base_queryset = Product.objects.all()

            if product_type == "popular":
                products = base_queryset.filter(is_popular=True).order_by("-id")[:20]
                serializer = ProductListSerializer(products,many=True,context={"request": request})

                response_data = {
                    "status": "success",
                    "message": f"{SUCCESS} - Popular Products Fetched Successfully.",
                    "type": "popular_products",
                    "count": products.count(),
                    "data": serializer.data
                }
                return Response(response_data,status=status.HTTP_200_OK)

            elif product_type == "all":
                products = base_queryset
                search = request.GET.get("search")
                category = request.GET.get("category")
                min_price = request.GET.get("min_price")
                max_price = request.GET.get("max_price")
                sort_by = request.GET.get("sort_by", "-id")

                if search:
                    products = products.filter(Q(name__icontains=search))

                if category:
                    products = products.filter(category__iexact=category)

                if min_price:
                    products = products.filter(price__gte=min_price)

                if max_price:
                    products = products.filter(price__lte=max_price)

                allowed_sort_fields = ["price","-price","name","-name","rating","-rating","id","-id",]

                if sort_by in allowed_sort_fields:
                    products = products.order_by(sort_by)
                else:
                    products = products.order_by("-id")

                serializer = ProductListSerializer(products,many=True,context={"request": request})

                response_data = {
                    "status": "success",
                    "message": f"{SUCCESS} - All Products Fetched Successfully.",
                    "type": "all_products",
                    "count": products.count(),
                    "data": serializer.data,
                }
                return Response(response_data,status=status.HTTP_200_OK,)

            return Response({"status": "fail","message": f"{BAD_REQUEST} - Invalid type. Supported values are: all, popular products."},
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"status": "error","message": f"{INTERNAL_SERVER_ERROR} - Internal Server Error - {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,)