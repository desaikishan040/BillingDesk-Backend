from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView)


urlpatterns = [
    # user
    path('register', views.RegisterUserAPIView.as_view(), name="register"),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout', views.BlacklistToken.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name="tokenverify"),
    # company
    path('company', views.CompanyView.as_view(), name="company"),
    # expanse
    path('expanse', views.ExpanseView.as_view(), name="company"),
    # invoice
    path('generate-invoice', views.InvoiceView.as_view(), name="invoice"),
    path('add-item', views.ItemsView.as_view(), name="invoiceitems"),
    path('add-ordered-item', views.InvoiceItemsView.as_view(), name="invoiceitems"),
    path('inventory', views.InventoryView.as_view(), name="inventory"),
    # alldata fetching api
    path('getallcompany', views.Getallcompany, name="getallcompany"),
    path('getinboxbill', views.Getinboxbill, name="getinboxbill"),
    path('getsendboxbill', views.Getsendboxbill, name="getsendboxbill"),
    # update
    path('update-item', views.UpdateItem, name="update-item"),
    path('update-item-new', views.UpdateItemNew.as_view(), name="update-item-new"),
    path('update-company', views.UpdateCompany, name="update-company"),
    # dashboard
    path('dashboard-data', views.Dashboard, name="dashboard-data"),
    # demo
    path('sendmail', views.sendmail_to_coustomer, name="sendmail"),
    path('download-invoice', views.DownloadInvoice, name="downloadinvoice"),
    path('add-item-new', views.NewItemView.as_view(), name="demo"),
    path('demo', views.Demo, name="demo"),
]
