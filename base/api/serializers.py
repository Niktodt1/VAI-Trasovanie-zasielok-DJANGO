from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from ..models import Package, UserAccount, Company, DeliveryCompany, Courier, DeliveryCode, Stage, StageCode, Address, User

class PackageSerializer(ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class AccountSerializer(ModelSerializer):
    addressId = AddressSerializer()
    user = UserSerializer()
    class Meta:
        model = UserAccount
        fields = '__all__'

class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class DeliveryCompanySerializer(ModelSerializer):
    class Meta:
        model = DeliveryCompany
        fields = '__all__'

class CourierSerializer(ModelSerializer):
    class Meta:
        model = Courier
        fields = '__all__'

class DeliveryCodeSerializer(ModelSerializer):
    class Meta:
        model = DeliveryCode
        fields = '__all__'

class StageSerializer(ModelSerializer):
    class Meta:
        model = Stage
        fields = '__all__'

class StageCodeSerializer(ModelSerializer):
    class Meta:
        model = StageCode
        fields = '__all__'


class PackageSerializerAndAssociated(ModelSerializer):
    # receiverUserId = serializers.PrimaryKeyRelatedField(queryset=UserAccount.objects.all())
    # companyId = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())

    receiverUserId = AccountSerializer()
    companyId = CompanySerializer()
    deliveryCompanyId = DeliveryCompanySerializer()
    courierId = CourierSerializer()
    typeOfDelivery = DeliveryCodeSerializer()

    def update(self, instance, validated_data):
        instance.id = validated_data.get("id", instance.id)
        instance.receiverUserId = validated_data.get("receiverUserId", instance.receiverUserId)
        instance.companyId = validated_data.get("companyId", instance.companyId)
        instance.dateOfOrder = validated_data.get("dateOfOrder", instance.dateOfOrder)
        instance.deliveryCompanyId = validated_data.get("deliveryCompanyId", instance.deliveryCompanyId)
        instance.received = validated_data.get("received", instance.received)
        instance.courierId = validated_data.get("courierId", instance.courierId)
        instance.typeOfDelivery = validated_data.get("typeOfDelivery", instance.typeOfDelivery)
        instance.dateDelivered = validated_data.get("dateDelivered", instance.dateDelivered)
        instance.updated = validated_data.get("updated", instance.updated)
        instance.created = validated_data.get("created", instance.created)
        instance.save()
        return instance


    class Meta:
        model = Package
        fields = '__all__'


class StageSerializerAndAssociated(ModelSerializer):
    stageCurrentId = StageCodeSerializer()

    class Meta:
        model = Stage
        fields = '__all__'