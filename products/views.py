from rest_framework.views import APIView
from .models import Product, ProductImage
from .serializers import ProductSerializer, ProductImageSerializer
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK,HTTP_404_NOT_FOUND,HTTP_400_BAD_REQUEST)
# Create your views here.

class ProductView(APIView):

    def get(self, request, *args, **kwargs):

        try:
            product_id = kwargs.get("id", None)
    
            if product_id:
                product = Product.objects.get(id=product_id)
                serializer = ProductSerializer(product)
                return Response(serializer.data, status=HTTP_200_OK)
            
            else:
                products = Product.objects.all()
                serializer = ProductSerializer(products, many=True)
                return Response(serializer.data, status=HTTP_200_OK)
            
        except Product.DoesNotExist:
            return Response({'error':'Product not found'}, status=HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)
       
