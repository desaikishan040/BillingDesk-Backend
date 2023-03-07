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
from .models import Company,Items


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

    def get(self, request, *args, **kwargs):
        company = Company.objects.filter(user=request.user.id).values()
        if company:
            return Response({"status": "success", "data": company}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": "Company not found"}, status=status.HTTP_200_OK)
        #     return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        # else:
        #     return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class InvoiceView(APIView):

    def post(self, request, *args, **kwargs):
        request.data._mutable = True
        company = Company.objects.filter(user=request.user.id, id=request.data["company_to"])
        if company:
            serializer = InvoiceDataSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": "error", "data": "Invalid Company."}, status=status.HTTP_401_UNAUTHORIZED)


@permission_classes([IsAuthenticated])
class ItemsView(APIView):
    def get(self, request, *args, **kwargs):
        items = Items.objects.filter(created_by_user=request.user.id, created_by_company=request.GET.get("created_by_company")).values()
        if items:
            return Response({"status": "success", "data":items}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": "No any Item found Please add item or change company"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        request.data._mutable = True
        company = Company.objects.filter(user=request.user.id, id=request.data["created_by_company"])
        if company:
            request.data['created_by_user'] = request.user.id
            serializer = ItemsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": "error", "data": "Invalid Company."}, status=status.HTTP_401_UNAUTHORIZED)


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
    print(token)
    token = Token.objects.create(user=token)
    return Response(token.key)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Demo(request):
    return Response({"token": "key"})
