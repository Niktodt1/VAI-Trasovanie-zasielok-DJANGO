from django.forms import ModelForm
from .models import DeliveryCompany, Address, Company, Package, UserAccount
from django.contrib.auth.models import User


class DeliveryCompanyForm(ModelForm):
    class Meta:
        model = DeliveryCompany
        fields = ['deliveryCompanyCode', 'deliveryCompanyDescription',
                  'phone', 'email', 'website',
                  'fullCompanyName', 'iconPath']
        labels = {
            'deliveryCompanyCode': 'Kód spoločnosti (skrátený názov alebo skratka):',
            'fullCompanyName': 'Celý názov spoločnosti:',
            'deliveryCompanyDescription': 'Popis spoločnosti:',
            'phone': 'Telefónne číslo spoločnosti:',
            'email': 'Emailová adresa spoločnosti:',
            'website': 'Webstránka spoločnosti:',
            'iconPath': 'Cesta ku obrázku spoločnosti:'
        }


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['city', 'zipCode', 'street', 'streetNumber']
        labels = {
            'city': 'Mesto alebo obec:',
            'zipCode': 'PSČ:',
            'street': 'Ulica:',
            'streetNumber': 'Súpisné číslo:'
        }


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['companyCode', 'companyName', 'companyDescription',
                  'phone', 'email', 'website', 'icon']
        labels = {
            'companyCode': 'Kód obchodu (skrátený názov alebo skratka):',
            'companyName': 'Celý názov obchodu:',
            'companyDescription': 'Popis obchodu:',
            'phone': 'Telefónne číslo obchodu:',
            'email': 'Emailová adresa obchodu:',
            'website': 'Webstránka obchodu:',
            'icon': "Obrázok alebo ikona obchodu:",
        }


class UserAccountForm(ModelForm):
    class Meta:
        model = UserAccount
        fields = ['name', 'surname', 'phone', 'email']
        labels = {
            'name': 'Vaše krstné meno:',
            'surname': 'Vaše priezvisko:',
            'phone': 'Vaše telefónne číslo:',
            'email': 'Vaša Emailová adresa:'
        }

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']
        labels = {
            'username': 'Používateľské meno (login):'
        }

class PackageForm(ModelForm):
    class Meta:
        model = Package
        fields = ['companyId', 'dateOfOrder', 'deliveryCompanyId',
                  'typeOfDelivery']





