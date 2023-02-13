from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.


class Address(models.Model):
    city = models.CharField(max_length=100, default="neznáme mesto")
    zipCode = models.CharField(max_length=5, default="## ###")
    street = models.CharField(max_length=100, default="neznáma ulica")
    streetNumber = models.CharField(max_length=50, default="#")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s %s' % (self.city, self.street, self.streetNumber)


class Company(models.Model):
    companyCode = models.CharField(max_length=100, default="nezmáma spoločnosť")
    companyName = models.CharField(max_length=100, default="nezmáma spoločnosť")
    companyDescription = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=13, default="+421##########")
    email = models.CharField(max_length=100, default="###@email")
    website = models.CharField(max_length=100, default="obchod nemá web")
    addressId = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    iconPath = models.TextField(null=True, blank=True)
    icon = models.ImageField(null=True, default="shop_default.svg")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['companyCode', 'companyName']

    def __str__(self):
        return self.companyCode


class DeliveryCode(models.Model):
    deliveryText = models.TextField(default="neznámy spôsob dopravy")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.deliveryText


class DeliveryCompany(models.Model):
    deliveryCompanyCode = models.CharField(max_length=100, default="Neznámy doparvca")
    deliveryCompanyDescription = models.TextField(null=True, blank=True)
    addressId = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=13, default="+421##########")
    email = models.CharField(max_length=100, default="###@email")
    website = models.CharField(max_length=100, null=True, blank=True)
    fullCompanyName = models.CharField(max_length=100, default="###")
    iconPath = models.TextField(null=True, blank=True)
    icon = models.ImageField(null=True, default="deliveryCompany_default.svg")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['deliveryCompanyCode', 'fullCompanyName']

    def __str__(self):
        return self.deliveryCompanyCode


class Courier(models.Model):
    name = models.CharField(max_length=100, default="neznáme meno")
    surname = models.CharField(max_length=100, default="neznáme priezvisko")
    deliveryCompanyId = models.ForeignKey(DeliveryCompany, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    picturePath = models.TextField(null=True, blank=True)
    picture = models.ImageField(null=True, default="id_default")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s company:%s' % (self.name, self.surname, self.deliveryCompanyId)


class StageCode(models.Model):
    stageDescription = models.TextField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.stageDescription


class UserAccount(models.Model):
    # username = models.CharField(max_length=100, null=True, blank=True)
    # password = models.CharField(max_length=200, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='account', unique=True)
    name = models.CharField(max_length=100, default="neznáme meno")
    surname = models.CharField(max_length=100, default="neznáme priezvisko")
    addressId = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=13, default="+421##########")
    email = models.CharField(max_length=100, default="###@email", unique=True)
    isRegistered = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.name, self.surname)


class Package(models.Model):
    receiverUserId = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    companyId = models.ForeignKey(Company, on_delete=models.CASCADE)
    dateOfOrder = models.DateTimeField(default=timezone.now)
    deliveryCompanyId = models.ForeignKey(DeliveryCompany, on_delete=models.CASCADE)
    received = models.BooleanField(null=True, blank=True)
    courierId = models.ForeignKey(Courier, on_delete=models.CASCADE, null=True, blank=True)
    typeOfDelivery = models.ForeignKey(DeliveryCode, on_delete=models.CASCADE)
    dateDelivered = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def past_stages(self):
        return self.stages.filter(datetime__lt=timezone.now())

    class Meta:
        get_latest_by = "stageCurrentId"

    def __str__(self):
        return 'rec:%s date:%s shop:%s' % (self.receiverUserId, self.dateOfOrder, self.companyId)


class Stage(models.Model):
    datetime = models.DateTimeField(default=timezone.now)
    packageId = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='stages')
    stageCurrentId = models.ForeignKey(StageCode, on_delete=models.CASCADE)
    lastSeen = models.TextField(null=True, blank=True)
    estTimeOfDelivery = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = ['stageCurrentId']

    def __str__(self):
        return '%s___stage:%s___TIME:%s' % (self.packageId, self.stageCurrentId, self.datetime)

# TODO blank=True   ak pridavame form!!!!!!!!!!!
# TODO ak databaza vypise chybu NO_SUCH_TABLE tak dat tento prikaz:python manage.py migrate --run--syncdb
