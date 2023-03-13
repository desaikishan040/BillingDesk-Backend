from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,TokenVerifyView)

urlpatterns = [
    path('register', views.RegisterUserAPIView.as_view(), name="register"),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name="tokenverify"),
    path('company', views.CompanyView.as_view(), name="company"),
    path('generate-invoice', views.InvoiceView.as_view(), name="invoice"),
    path('add-item', views.ItemsView.as_view(), name="invoiceitems"),
    path('add-ordered-item', views.InvoiceItemsView.as_view(), name="invoiceitems"),
    path('getallcompany', views.Getallcompany, name="getallcompany"),
    path('getallbill', views.Getallbill, name="demo"),
    path('demo', views.Demo, name="demo"),
    path('accounts/', include('django.contrib.auth.urls')),
]
