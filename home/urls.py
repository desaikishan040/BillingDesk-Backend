from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView)

urlpatterns = [
    # user
    path('register', views.RegisterUserAPIView.as_view(), name="register"),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name="tokenverify"),
    # company
    path('company', views.CompanyView.as_view(), name="company"),
    # invoice
    path('generate-invoice', views.InvoiceView.as_view(), name="invoice"),
    path('add-item', views.ItemsView.as_view(), name="invoiceitems"),
    path('add-ordered-item', views.InvoiceItemsView.as_view(), name="invoiceitems"),
    # alldata fetching api
    path('getallcompany', views.Getallcompany, name="getallcompany"),
    path('getinboxbill', views.Getinboxbill, name="getinboxbill"),
    path('getsendboxbill', views.Getsendboxbill, name="getsendboxbill"),
    # update
    path('update-item', views.UpdateItem, name="update-item"),
    path('update-company', views.UpdateCompany, name="update-company"),
    # dashboard
    path('dashboard-data', views.Dashboard, name="dashboard-data"),
    # demo
    path('demo', views.demo , name="demo"),

]
