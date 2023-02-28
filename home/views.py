from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import RegisterSerializer, CompanyDataSerializer, InvoiceDataSerializer, \
    ItemsSerializer, InvoiceItemsSerializer
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Company

class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@permission_classes([IsAuthenticated])
class CompanyView(APIView):

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = CompanyDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class InvoiceView(APIView):

    def post(self, request, *args, **kwargs):
        request.data._mutable = True
        # company = Company.objects.filter(user = request.user.id ).values
        # print(request.data['company_to'])
        # if request.data['company_to'] in company:
        #     print("------------------------>")
        serializer = InvoiceDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class ItemsView(APIView):

    def post(self, request, *args, **kwargs):
        request.data._mutable = True

        request.data['created_by_user'] = request.user.id
        serializer = ItemsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class InvoiceItemsView(APIView):

    def post(self, request, *args, **kwargs):
        request.data._mutable = True

        request.data['created_by_user'] = request.user.id
        serializer = InvoiceItemsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def authenticate_token(request):
    token = request.POST.get("token")
    token = Token.objects.create(user=token)
    return Response(token.key)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Demo(request):
    return Response({"token": "key"})
