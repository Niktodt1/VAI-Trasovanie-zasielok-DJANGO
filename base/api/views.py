import json

from django.http import JsonResponse
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Package, Stage
from .serializers import PackageSerializer, PackageSerializerAndAssociated, StageSerializer, StageSerializerAndAssociated
from ..views import findAccount


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/routes',
        'GET /api/packages/',
        'GET /api/packages/:id',
        'GET /api/stages/:packageId',
        'GET /api/currentUserPackages/:id',
        'GET /api/currentStages',
        'GET /api/packageStages/:id',
        'POST /api/newPackage/:userId',
        'POST /api/newStage/:packageId',
        'POST /api/updateStage/:stageId',
        'PUT /api/confirmPackage/:id',
    ]
    return Response(routes)

@api_view(['GET'])
def getPackages(request):
    packages = Package.objects.all()
    serializer = PackageSerializerAndAssociated(packages, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getPackage(request, pk):
    package = Package.objects.get(id=pk)
    serializer = PackageSerializer(package, many=False)
    return Response(serializer.data)

    try:
        package = Package.objects.get(id=pk)
    except Package.DoesNotExist:
        return JsonResponse({'message': 'The package does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PackageSerializer(package)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        package_data = JSONParser().parse(request)
        serializer = PackageSerializer(package, data=package_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        tutorial.delete()
        return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def getUserPackages(request):
    print("API posiela usera:" + str(request.user))
    account = findAccount(request.user)

    print("a nasiel sa account:" + str(account))
    packages = Package.objects.filter(receiverUserId=account, dateDelivered__isnull=True).select_related().order_by('-created')
    past_stages = Stage.objects.filter(datetime__lt=timezone.now())
    total_packages = packages.count()
    current_time = timezone.now()
    serializer = PackageSerializerAndAssociated(packages, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getCurrentStages(request):
     past_stages = Stage.objects.filter(datetime__lt=timezone.now())
     current_time = timezone.now()
     serializer = StageSerializerAndAssociated(past_stages, many=True)
     return Response(serializer.data)


@api_view(['GET'])
def getPackageStages(request, pk):
     past_stages = Stage.objects.filter(packageId=pk, datetime__lt=timezone.now())
     current_time = timezone.now()
     serializer = StageSerializerAndAssociated(past_stages, many=True)
     return Response(serializer.data)

@api_view(['PUT'])
def confirmPackage(request, pk):
    print("CONFIRM FIRED!")
    if  request.method == 'PUT':
        package = Package.objects.get(id=pk)
        print("PUT ACKNOWLEDGED!")
        data = json.load(request)
        updated_values = data.get('payload')
        print(str(updated_values))
        print("Updating package_" + str(pk))
        package.dateDelivered = timezone.now()
        package.updated = timezone.now()
        package.save()
        serializer = PackageSerializer(package)

        return Response(serializer.data)

    