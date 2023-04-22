import json
import os

from django.db.models import Sum, Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import RegisterSerializer, CompanyDataSerializer, InvoiceDataSerializer, \
    ItemsSerializer, InvoiceItemsSerializer, NewInvoiceItemsSerializer, InvoiceFullDataSerializer, \
    ExpanseDataSerializer, ItemOtherfieldSerializer, InventorySerializer, InventorypostSerializer
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Company, Items, InvoiceItems, Invoice, Expanse, ItemOtherfield, InventoryItems
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import get_template
import pdfkit
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@permission_classes([IsAuthenticated])
class CompanyView(APIView):
    def post(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['user'] = request.user.id
        serializer = CompanyDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        company = Company.objects.current(request.user.id).values()
        if company:
            return Response({"status": "success", "data": company}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": "Company not found"}, status=status.HTTP_200_OK)


class BlacklistToken(APIView):
    def post(self, request, *args, **kwargs):
        Refresh_token = request.POST.get("refresh")
        token = RefreshToken(Refresh_token)

        token.blacklist()
        return Response("Successful Logout", status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class ExpanseView(APIView):
    def post(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['user'] = request.user.id
        serializer = ExpanseDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        data = Expanse.objects.filter(user=request.user.id, company=request.GET.get("company_id")).order_by(
            '-created_on').values()
        if data:
            return Response({"status": "success", "data": data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": "data not found"}, status=status.HTTP_400_BAD_REQUEST)


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
                                     created_by_company=request.GET.get("created_by_company")).order_by(
            '-created_on').values()
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

        for x in request.data:
            serializer = InvoiceItemsSerializer(data=x)
            if serializer.is_valid():
                serializer.save()
                data = InventoryItems.objects.filter(item__id=serializer.data["ordered_item"])
                print(data)
                print(serializer.data)
                print(serializer.data["ordered_item"])
                if len(data) > 0:
                    data[0].quantity = data[0].quantity - serializer.data['quantity']
                    data[0].save()

            else:
                return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "success", "data": "bill generated"}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class InventoryView(APIView):
    def get(self, request, *args, **kwargs):
        items = InventoryItems.objects.filter(user=request.user.id,
                                              company=request.GET.get("company")).order_by('-created_on')
        serializer = InventorySerializer(items, many=True)

        if items:
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": "No any Inventory found."},
                            status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['user'] = request.user.id
        serializer = InventorypostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['user'] = request.user.id
        instance = InventoryItems.objects.get(id=request.data['id'], company=request.data['company'])
        instance.quantity = request.data['quantity']
        instance.save()

        return Response({"status": "success", "data": "data is updated"}, status=status.HTTP_200_OK)
        # else:
        #     return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def authenticate_token(request):
    token = request.POST.get("token")

    token = Token.objects.create(user=token)
    return Response(token.key)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Getallcompany(request):
    company = Company.objects.all().values()
    if company:
        return Response({"status": "success", "data": company}, status=status.HTTP_200_OK)
    else:
        return Response({"status": "error", "data": "Company not found"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Getinboxbill(request):
    query = request.GET.get('query')

    if query:
        # inboxdata = Invoice.objects.filter(Q(company_from=request.GET.get("company_id")) &
        #                                    (Q(invoice_no__icontains=query))).select_related(
        #     'company_from').order_by('-created_on')
        inboxdata = Invoice.objects.filter(
            (Q(invoice_no__icontains=query) | Q(company_to__company_name__icontains=query)),
            company_from=request.GET.get("company_id")).select_related(
            'company_from').order_by('-created_on')
    else:
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
    query = request.GET.get("query")
    searchquery = request.GET.get("searchquery")
    some_day_last_week = timezone.now().date() - timedelta(days=7)
    kwargs = {
    }

    if query == "company":
        kwargs = {
            '{0}__{1}'.format('company_from', "isnull"): False
        }
    elif query == "coustomer":
        kwargs = {
            '{0}__{1}'.format('company_from', "isnull"): True
        }
    if searchquery:

        sendboxdata = Invoice.objects.filter((Q(invoice_no__icontains=searchquery) | Q(
            company_from__company_name__icontains=searchquery) | Q(customer_name__icontains=searchquery)),
                                             company_to=request.GET.get("company_id"),
                                             **kwargs, ).select_related(
            'company_from').order_by('-created_on')
    else:
        sendboxdata = Invoice.objects.filter(company_to=request.GET.get("company_id"),
                                             **kwargs, ).select_related(
            'company_from').order_by('-created_on')

    total_sales = Invoice.objects.filter(created_on__gte=some_day_last_week,
                                         company_to=request.GET.get("company_id"), **kwargs).values(
        'created_on__date'
    ).annotate(
        created_date_count=Count('created_on__date')
    ).annotate(
        day_collection=Sum('total')
    ).order_by('-created_on__date')

    total_sendinboxdata_amount = Invoice.objects.filter(company_to=request.GET.get("company_id"), **kwargs).aggregate(
        Sum('total'))

    total_sendinboxdata_count = Invoice.objects.filter(company_to=request.GET.get("company_id"), **kwargs).aggregate(
        Count('invoice_no'))

    paginator = Paginator(sendboxdata, 10)
    page_number = request.GET.get('page')

    if page_number is None:
        page_number = 1

    data = paginator.get_page(page_number)
    serialized_sendbox = NewInvoiceItemsSerializer(data, many=True)

    totalnumpages = data.paginator.num_pages

    card_data = {
        "total_sales": total_sales,
        "total_sendinboxdata_amount": total_sendinboxdata_amount,
        "total_sendinboxdata_count": total_sendinboxdata_count
    }

    if serialized_sendbox.data:
        return Response(
            {"status": "success", "sendboxdata": serialized_sendbox.data, "card_data": card_data, "report_type": query,
             "totalnumpages": totalnumpages},
            status=status.HTTP_200_OK)
    else:
        return Response(
            {"status": "error", "data": "No any bill found"},
            status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class NewItemView(APIView):
    def get(self, request, *args, **kwargs):
        item = Items.objects.filter(id=request.GET.get("item_id")).values()
        if item:
            items = Items.objects.prefetch_related('parent_item').get(id=request.GET.get("item_id"))
            return Response({"status": "success", "otherfields": items.parent_item.all().values(), "itemdata": item},
                            status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": "item not found"},
                            status=status.HTTP_400_BAD_REQUEST00_OK)

    def post(self, request, *args, **kwargs):
        request.data._mutable = True
        company = Company.objects.filter(user=request.user.id, id=request.data["created_by_company"])
        if company:
            parent_item = json.loads(request.data["parent_item"])
            request.data['created_by_user'] = request.user.id
            serializer = ItemsSerializer(data=request.data)

            if serializer.is_valid():
                post = serializer.save()
                if parent_item:
                    for items in parent_item:
                        ItemOtherfield.objects.create(parent_item=post, field_value=items["field_value"],
                                                      field_name=items["field_name"],
                                                      field_type=items["field_type"])

                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:

                return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": "error", "data": "Invalid Company."}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class UpdateItemNew(generics.UpdateAPIView):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Items.objects.get(id=self.request.data['id'])

    def put(self, request, *args, **kwargs):
        request.data._mutable = True
        parent_item = json.loads(request.data["parent_item"])
        request.data['created_by_user'] = request.user.id
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            if parent_item:
                for items in parent_item:
                    if type(items["field_id"]) is int and items["field_id"]:
                        items["parent_item"] = request.data['id']
                        otherfield_instance = ItemOtherfield.objects.get(id=items['field_id'])

                        serializer_otherfield = ItemOtherfieldSerializer(otherfield_instance, data=items)
                        if serializer_otherfield.is_valid():
                            serializer_otherfield.save()
                        else:
                            return Response({"message": serializer_otherfield.errors},
                                            status=status.HTTP_400_BAD_REQUEST)
                    else:
                        ItemOtherfield.objects.create(parent_item=instance, field_value=items["field_value"],
                                                      field_name=items["field_name"],
                                                      field_type=items["field_type"])
                        return Response({"message": "data updated"}, status=status.HTTP_200_OK)
            return Response({"message": serializer.data}, status=status.HTTP_200_OK)

        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def UpdateItem(request):
    request.data._mutable = True
    request.data['created_by_user'] = request.user.id

    itemdata = Items.objects.get(created_by_company=request.data["created_by_company"], id=request.data["id"])

    if not request.data['item_image']:
        request.data['item_image'] = itemdata.item_image

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
    request.data['user'] = request.user.id

    companydata = Company.objects.get(id=request.data["id"], user=request.user.id)

    if not request.data['profile_image']:
        request.data['profile_image'] = companydata.profile_image

    serializer = CompanyDataSerializer(companydata, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Dashboard(request):
    total_inboxdata_amount = Invoice.objects.filter(company_from=request.GET.get("company_id")).aggregate(Sum('total'))
    total_inboxdata_count = Invoice.objects.filter(company_from=request.GET.get("company_id")).aggregate(
        Count('invoice_no'))

    total_expansedata_amount = Expanse.objects.filter(company=request.GET.get("company_id")).aggregate(Sum('amount'))
    total_expansedata_count = Expanse.objects.filter(company=request.GET.get("company_id")).aggregate(
        Count('id'))

    card_data = {
        "total_inboxdata_amount": total_inboxdata_amount,
        "total_inboxdata_count": total_inboxdata_count,
        "total_expansedata_count": total_expansedata_count,
        "total_expansedata_amount": total_expansedata_amount,

    }

    if total_inboxdata_count or total_inboxdata_amount:
        return Response({"status": "success", "card_data": card_data},
                        status=status.HTTP_200_OK)
    else:
        return Response({"status": "error", "data": "No data found for dashboard"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sendmail_to_coustomer(request):
    singleinvoicedata = InvoiceItems.objects.filter(invoice_id=request.GET.get("invoice_id")).select_related(
        'ordered_item').select_related('invoice_id').order_by('created_on')
    serialized_data = InvoiceFullDataSerializer(singleinvoicedata, many=True)

    html = render_to_string('billformet.html', {'data': singleinvoicedata})
    pdfkit.from_string(html, "static/output.pdf")
    # x=pdfkit.from_string(html, "static/output.pdf", options={'page-size':'A4'})

    pdf = open("static/output.pdf")
    # response = HttpResponse(pdf.read(), content_type="application/pdf")
    # response['Content-Disposition'] = 'attachment; filename="static/output.pdf";'
    pdf.close()
    subject = 'Billing system'
    body = 'Email body message'
    from_email = settings.EMAIL_HOST_USER
    to_email = [singleinvoicedata[0].invoice_id.coustomer_mail]
    email = EmailMessage(subject, body, from_email, to_email)
    email.attach_file("static/output.pdf", 'application/pdf')
    # email.attach("output.pdf",response, 'application/pdf')

    email.send()
    os.remove("static/output.pdf")
    return Response({"status": "success", "msg": "sent mail"})


@api_view(['GET'])
def DownloadInvoice(request):
    singleinvoicedata = InvoiceItems.objects.filter(invoice_id=request.GET.get("invoice_id")).select_related(
        'ordered_item').select_related('invoice_id').order_by('created_on')
    serialized_data = InvoiceFullDataSerializer(singleinvoicedata, many=True)
    html = render_to_string('billformet.html', {'data': singleinvoicedata})
    x = pdfkit.from_string(html, False)

    response = HttpResponse(x, content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="static/output.pdf";'

    return response


@api_view(['GET'])
def Demo(request):
    data = InventoryItems.objects.get(item=17)
    d = InventorySerializer(data, many=True)
    return Response({"status": "success", "card_data": d.data},
                    status=status.HTTP_200_OK)
