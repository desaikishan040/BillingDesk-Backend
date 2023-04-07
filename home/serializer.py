from django.contrib.auth.admin import User

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Company, Invoice, Items, InvoiceItems, Expanse


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2',
                  'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CompanyDataSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if Company.objects.filter(GST_number=attrs["GST_number"]):
            raise serializers.ValidationError(
                {"GST_number": "GST number already exist"})
     
        return attrs

    class Meta:
        model = Company
        fields = '__all__'


class ExpanseDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expanse
        fields = '__all__'


class InvoiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'


class InvoiceItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItems
        fields = '__all__'


class NewInvoiceItemsSerializer(serializers.ModelSerializer):
    company_from = CompanyDataSerializer(read_only=True)
    company_to = CompanyDataSerializer(read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'


class InvoiceFullDataSerializer(serializers.ModelSerializer):
    invoice_id = NewInvoiceItemsSerializer(read_only=True)
    ordered_item = ItemsSerializer(read_only=True)

    class Meta:
        model = InvoiceItems
        fields = '__all__'
