from django.urls import path, include
from . import views

urlpatterns = [
    path('require-item', views.RequireItem.as_view(), name="requireItem"),
    path('require-item-all', views.RequireItemAll, name="requireiItemAll"),
]
