from ...views import *
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


class PublicProductsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            product_type = request.GET.get("type", "all").lower()
            base_queryset = Product.objects.filter(is_deleted=False,is_deactive=False)

            if product_type == "popular":
                products = base_queryset.filter(is_popular=True).order_by("-created_at")[:20]
                serializer = ProductListSerializer(products,many=True,context={"request": request})

                response_data = {
                    "status": "success",
                    "message": f"{SUCCESS} - Popular Products Fetched Successfully.",
                    "type": "popular_products",
                    "count": products.count(),
                    "data": serializer.data,
                }
                return Response(response_data,status=status.HTTP_200_OK,)

            elif product_type == "all":
                search = request.GET.get("search")
                category = request.GET.get("category")
                min_price = request.GET.get("min_price")
                max_price = request.GET.get("max_price")
                sort_by = request.GET.get("sort_by", "-created_at")

                products = base_queryset
                if search:
                    products = products.filter(
                        Q(name__icontains=search)
                        | Q(description__icontains=search)
                        | Q(category__icontains=search)
                        | Q(subcategory__icontains=search)
                    )

                # Category Filter
                if category:
                    products = products.filter(
                        category__iexact=category
                    )

                # Price Filter
                if min_price:
                    products = products.filter(
                        price__gte=min_price
                    )

                if max_price:
                    products = products.filter(
                        price__lte=max_price
                    )

                # Sorting
                allowed_sort_fields = [
                    "price",
                    "-price",
                    "name",
                    "-name",
                    "created_at",
                    "-created_at",
                ]

                if sort_by in allowed_sort_fields:
                    products = products.order_by(sort_by)
                else:
                    products = products.order_by("-created_at")

                serializer = ProductListSerializer(
                    products,
                    many=True,
                    context={"request": request}
                )

                return Response(
                    {
                        "status": "success",
                        "message": f"{SUCCESS} - All Products Fetched Successfully.",
                        "type": "all_products",
                        "count": products.count(),
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {
                    "status": "fail",
                    "message": f"{BAD_REQUEST} - Invalid type. Supported values are: all, popular"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "status": "error",
                    "message": f"{INTERNAL_SERVER_ERROR} - {str(e)}"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )