from django.db.models import Sum, Count
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import RegisterSerializer, CompanyDataSerializer, InvoiceDataSerializer, \
    ItemsSerializer, InvoiceItemsSerializer, NewInvoiceItemsSerializer, InvoiceFullDataSerializer
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Company, Items, InvoiceItems, Invoice
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator


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


@permission_classes([IsAuthenticated])
class InvoiceView(APIView):
    def get(self, request, *args, **kwargs):
        singleinvoicedata = InvoiceItems.objects.filter(invoice_id=request.GET.get("invoice_no")).select_related(
            'ordered_item').select_related('invoice_id').order_by('created_on')
        serialized_data = InvoiceFullDataSerializer(singleinvoicedata, many=True)
        return Response({"status": "success", "data": serialized_data.data}, status=status.HTTP_200_OK)

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
        items = Items.objects.filter(created_by_user=request.user.id,
                                     created_by_company=request.GET.get("created_by_company")).values()
        if items:
            return Response({"status": "success", "data": items}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": "No any Item found Please add item or change company"},
                            status=status.HTTP_400_BAD_REQUEST)

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
        print(request.data)
        for x in request.data:
            serializer = InvoiceItemsSerializer(data=x)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "success", "data": "bill generated"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def authenticate_token(request):
    token = request.POST.get("token")
    print(token)
    token = Token.objects.create(user=token)
    return Response(token.key)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Getallcompany(request):
    company = Company.objects.all().values()
    if company:
        return Response({"status": "success", "data": company}, status=status.HTTP_200_OK)
    else:
        return Response({"status": "error", "data": "Company not found"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Getinboxbill(request):
    inboxdata = Invoice.objects.filter(company_from=request.GET.get("company_id")).select_related(
        'company_from').order_by('-created_on')

    paginator = Paginator(inboxdata, 10)
    page_number = request.GET.get('page')
    if page_number is None:
        page_number = 1
    data = paginator.get_page(page_number)
    serialized_inbox = NewInvoiceItemsSerializer(data, many=True)
    totalnumpages = data.paginator.num_pages
    if serialized_inbox.data:
        return Response(
            {"status": "success", "totalnumpages": totalnumpages, "inboxdata": serialized_inbox.data},
            status=status.HTTP_200_OK)
    else:
        return Response({"status": "error", "data": "No any bill found"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Getsendboxbill(request):
    sendboxdata = Invoice.objects.filter(company_to=request.GET.get("company_id")).select_related(
        'company_from').order_by('-created_on')
    paginator = Paginator(sendboxdata, 10)
    page_number = request.GET.get('page')
    if page_number is None:
        page_number = 1
    data = paginator.get_page(page_number)
    serialized_sendbox = NewInvoiceItemsSerializer(data, many=True)

    totalnumpages = data.paginator.num_pages
    if serialized_sendbox.data:
        return Response(
            {"status": "success", "totalnumpages": totalnumpages, "sendboxdata": serialized_sendbox.data},
            status=status.HTTP_200_OK)
    else:
        return Response({"status": "error", "data": "No any bill found"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def UpdateItem(request):
    request.data._mutable = True
    request.data['created_by_user'] = request.user.id
    itemdata = Items.objects.get(created_by_company=request.data["created_by_company"], id=request.data["id"])
    serializer = ItemsSerializer(itemdata, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def UpdateCompany(request):
    request.data._mutable = True
    print(request.data)
    request.data['user'] = request.user.id
    companydata = Company.objects.get(id=request.data["id"], user=request.user.id)
    serializer = CompanyDataSerializer(companydata, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Dashboard(request):
    some_day_last_week = timezone.now().date() - timedelta(days=7)
    total_sales = Invoice.objects.filter(created_on__gte=some_day_last_week,
                                         company_to=request.GET.get("company_id")).values(
        'created_on__date'
    ).annotate(
        created_date_count=Count('created_on__date')
    ).annotate(
        day_collection=Sum('total')
    ).order_by('-created_on__date')
    total_inboxdata_amount = Invoice.objects.filter(company_to=request.GET.get("company_id")).aggregate(Sum('total'))
    total_inboxdata_count = Invoice.objects.filter(company_to=request.GET.get("company_id")).aggregate(
        Count('invoice_no'))
    total_sendinboxdata_amount = Invoice.objects.filter(company_from=request.GET.get("company_id")).aggregate(
        Sum('total'))
    total_sendinboxdata_count = Invoice.objects.filter(company_from=request.GET.get("company_id")).aggregate(
        Count('invoice_no'))
    card_data = {
        "total_inboxdata_amount": total_inboxdata_amount,
        "total_inboxdata_count": total_inboxdata_count,
        "total_sendinboxdata_amount": total_sendinboxdata_amount,
        "total_sendinboxdata_count": total_sendinboxdata_count
    }
    if total_sales:
        return Response({"status": "success", "data": total_sales, "card_data": card_data},
                        status=status.HTTP_200_OK)
    else:
        return Response({"status": "error", "data": "No data found for dashboard"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def demo(request):
    some_day_last_week = timezone.now().date() - timedelta(days=7)

    total_sales = Invoice.objects.filter(created_on__gte=some_day_last_week, ).values(
        'created_on__date'
    ).annotate(
        created_date_count=Count('created_on__date')
    ).annotate(
        day_collection=Sum('total')
    )
    return Response({"status": "success", "data": total_sales}, status=status.HTTP_200_OK)
