from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Proposal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.TextField(max_length=500, null=False, blank=False)
    item_description = models.TextField(max_length=500, null=False, blank=False)
    quantity_need = models.IntegerField(blank=False, null=False)
    contact_number = models.IntegerField(blank=False, null=False)
    item_image = models.ImageField(upload_to='proposal/', blank=True, null=True)
    ask_price = models.IntegerField(blank=False, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
