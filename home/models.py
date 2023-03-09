from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="company_owner")
    company_name = models.CharField(max_length=150, null=True, blank=True)
    GST_number = models.CharField(max_length=15)
    Phone_number = models.CharField(blank=True, max_length=13)
    company_mail = models.EmailField(blank=True)
    state = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(max_length=15, null=True, blank=True)
    currency = models.CharField(max_length=15, null=False)
    Company_address = models.TextField(max_length=500, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    profile_image = models.ImageField(upload_to='images/', null=True, blank=True)


PAYMENT_CHOICES = (
    ('online', 'ONLINE'),
    ('cash', 'CASH'),
    ('check', 'CHECK'),
    ('upi', 'UPI'),
    ('card', 'CARD'),
)


class Invoice(models.Model):
    company_to = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company_to")
    company_from = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name="company_from")
    invoice_no = models.AutoField(primary_key=True, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cash')
    customer_name = models.CharField(max_length=50, blank=True)
    Phone_number =  models.CharField(blank=True, max_length=13)
    coustomer_mail = models.EmailField(blank=True)

    def save(self, *args, **kwargs):
        today = datetime.today()
        today_string = today.strftime('%y%m%d')
        next_invoice_number = '01'
        last_invoice = Invoice.objects.filter(invoice_no__startswith=today_string).order_by('invoice_no').last()
        if last_invoice:
            last_invoice_number = int(str(last_invoice.invoice_no)[-2:])
            next_invoice_number = '{0:02d}'.format(last_invoice_number + 1)
        self.invoice_no = today_string + next_invoice_number
        super(Invoice, self).save(*args, **kwargs)


class Items(models.Model):
    created_by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_by_company = models.ForeignKey(Company, on_delete=models.CASCADE)
    item_description = models.TextField(max_length=500, null=True, blank=True)
    MRP_price_per_unit = models.IntegerField(blank=False, null=False)
    GST_percentage = models.IntegerField(blank=False, null=False)
    purchase_price = models.IntegerField(blank=False, null=False)
    profit_amount = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    item_image = models.ImageField(upload_to='items/')

    def save(self, *args, **kwargs):
        self.profit_amount = (self.MRP_price_per_unit - self.purchase_price - (
                self.MRP_price_per_unit * self.GST_percentage) / 100)
        super(Items, self).save(*args, **kwargs)


class InvoiceItems(models.Model):
    quantity = models.IntegerField(blank=True, null=True)
    invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    ordered_item = models.ForeignKey(Items, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
