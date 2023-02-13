import random
import zoneinfo
from datetime import timedelta
from django.utils import timezone

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm


from .models import Package, Address, DeliveryCompany, Company, UserAccount, Courier, DeliveryCode, Stage, StageCode
from .forms import AddressForm, CompanyForm, DeliveryCompanyForm, UserAccountForm, UserForm, PackageForm
# Create your views here.

MULTIPLIER = 2

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        print(username)
        print(password)
        try:
            user = User.objects.get(username=username)
            print(user)
        except:
            messages.error(request, 'Takýto používateľ neexistuje')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Meno alebo heslo nie sú správne")
    context = {'page': page}
    return render(request, 'base/Auth/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    account_form = UserAccountForm()
    address_form = AddressForm()

    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['user'] = None
        request.POST['addressId'] = None
        request.POST['isRegistered'] = False
        form = UserCreationForm(request.POST)
        account_form = UserAccountForm(request.POST)
        address_form = AddressForm(request.POST)
        print("ACCOUNT:" + str(account_form.is_valid()))
        print(account_form.errors)
        if form.is_valid() and account_form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            account = account_form.save(commit=False)
            account.user = user
            address = address_form.save()
            account.isRegistered = True
            account.addressId = address
            account.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Pri registrácii nastala chyba')

    context = {'form': form, 'account_form': account_form, 'address_form': address_form}
    return render(request, 'base/Auth/login_register.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    packages = user.package_set.all()
    context = {'user': user, 'packages': packages}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def updateUser(request):
    if not request.user.is_authenticated:
        return redirect('home')

    user = request.user
    print("User is:" + str(user))
    accounts = UserAccount.objects.all()
    foundAccount = None
    for account in accounts:
        if account.user == user:
            print('MATCH!')
            foundAccount = account

    print("Account is:" + str(foundAccount))
    print("Address is:" + str(foundAccount.addressId))
    form = UserForm(instance=user)
    address_form = AddressForm(instance=foundAccount.addressId)
    account_form = UserAccountForm(instance=foundAccount)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        address_form = AddressForm(request.POST, instance=foundAccount.addressId)
        account_form = UserAccountForm(request.POST, instance=foundAccount)
        if form.is_valid() and address_form.is_valid() and account_form.is_valid():
            form.save()
            address_form.save()
            account_form.save()
            # TODO redirect na userProfile
            return redirect('home')

    context = {'form': form, 'address_form': address_form, 'account_form': account_form,
               'account': foundAccount, 'user': user}
    return render(request, 'base/Auth/update_user.html', context)

@login_required(login_url='login')
def changePassword(request):
    if not request.user.is_authenticated:
        return redirect('home')
    return render(request, 'base/Auth/change_password.html')

def home(request):
    account = findAccount(request.user)
    packages = Package.objects.filter(receiverUserId=account, dateDelivered__isnull=True).select_related().order_by('-created')
    past_stages = Stage.objects.filter(datetime__lt=timezone.now())

    total_packages = packages.count()
    current_time = timezone.now()
    context = {'packages': packages, 'total_packages': total_packages, 'past_stages': past_stages}
    return render(request, 'base/Home/homePage.html', context)


def newPackage(request):
    account = findAccount(request.user)
    page = 'registered'
    if str(request.user) == 'AnonymousUser':
        print("NO USER DETECTED!")
        page = 'unregistered'
    companies = Company.objects.all()
    deliveryCompanies = DeliveryCompany.objects.all()
    deliveryCodes = DeliveryCode.objects.all()
    if request.method == 'POST':
        package_form = PackageForm()
        address_form = AddressForm()
        account_form = UserAccountForm()
        if page == 'unregistered':
            print("Uzivatel nie je registrovany...")
            # vyhladame ci tu uz nebol v minulosti, podla emailu
            account = lookupAccount(request.POST['email'])
            if account is None:
                # neregistrovany pouzivatel...vytvorime mu fejkovy ucet
                # musime spravit form na account a na adresu
                account_form = UserAccountForm(request.POST)
                address_form = AddressForm(request.POST)
                account_form.user = None
                account_form.isRegistered = None
                print("Vytvorili sme mu formular bez usera a tu su chyby:" + str(account_form.errors))
                print("ACCOUNT JE: " + str(account_form.is_valid()))
                print("ADDRESS JE: " + str(address_form.is_valid()))
                if address_form.is_valid() and account_form.is_valid():
                    account = account_form.save(commit=False)
                    address = address_form.save()
                    address.save()
                    account.addressId = address
                    account.save()
                    # ucet sa neregistrovanemu nastavil

        package_form = PackageForm(request.POST)
        request.POST = request.POST.copy()
        obj_account = UserAccount.objects.get(id=account.id)
        obj_courier = getCourier(request.POST['typeOfDelivery'], request.POST['deliveryCompanyId'])
        package_form = PackageForm(request.POST)
        print("PACKAGE is:" + str(package_form.is_valid()))
        print(request.POST)
        print(package_form.errors)
        if package_form.is_valid():
            package = package_form.save(commit=False)
            package.receiverUserId = obj_account
            package.courierId = obj_courier
            package.received = False
            print(package)
            package.save()
            if not simulatePackage(package):
                messages.error(request, 'Nepodarilo a vytvoriť zásielku, jej simulácia zlyhala!')
                package.delete()
            else:
                # TODO:redirect na stránku kde vypíše úspech, alebo zobarziť nejaké okno
                return redirect('home')
        else:
            messages.error(request, 'Nepodarilo a vytvoriť zásielku')
    else:
        package_form = PackageForm()
        address_form = AddressForm()
        account_form = UserAccountForm()

    context = {'package_form': package_form, 'address_form': address_form,
               'account_form': account_form, 'page': page, 'companies': companies,
               'deliveryCompanies': deliveryCompanies, 'deliveryCodes': deliveryCodes}
    return render(request, 'base/Package/newPackagePage.html', context)


def simulatePackage(package):
    # 5 stageov....prve 4 su rovnake pre vsetky...posledny sa lisi od druhu dorucenia
    # generovanie prvych styroch

    # Stage(models.Model):
    # datetime = models.DateTimeField(default=timezone.now)
    # packageId = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='stages')
    # stageCurrentId = models.ForeignKey(StageCode, on_delete=models.CASCADE)
    # lastSeen = models.TextField(null=True, blank=True)
    # estTimeOfDelivery = models.DateTimeField(null=True, blank=True)

    # StageCode(models.Model):
    # stageDescription = models.TextField(null=True)

    # TRVANIE:
    # 1: 10-20s  2:10-20s 3:10-20 4:30-40 5: koniec
    # ZACIATKY:
    # 1: teraz  2:+(10-20s) 3:+(10-20) 4:+(10-20)  5:+(30-40)
    # TOTAL: 20*3+40 = 100 sekúnd bude odhad

    # STAGE 1
    datetime_now = timezone.now()

    duration = random.randint(10, 20) * MULTIPLIER
    delta = timedelta(seconds=duration)
    datetime_start = datetime_now
    datetime_next = datetime_start + delta
    delta = timedelta(seconds=100)
    datetime_estimate = datetime_start + delta
    last_seen = str("Sídlo " + package.companyId.companyName + ", " + package.companyId.addressId.city)
    stageCode = StageCode.objects.get(id=1)
    print("Štart objednávky:" + str(datetime_now))
    print("Stage1 od:" + str(datetime_start) + " do:" + str(datetime_next))
    print("Naposledy v:" + last_seen)
    print("Stav1:" + stageCode.stageDescription)
    newStage = Stage(datetime=datetime_start, packageId=package, stageCurrentId=stageCode, lastSeen=last_seen, estTimeOfDelivery=datetime_estimate)
    print(str(newStage))
    newStage.save()

    #STAGE 2
    datetime_start = datetime_next
    duration = random.randint(10, 20) * MULTIPLIER
    delta = timedelta(seconds=duration)
    datetime_next = datetime_start + delta
    delta = timedelta(seconds=80)
    datetime_estimate = datetime_start + delta
    last_seen = str("Sídlo " + package.companyId.companyName + ", " + package.companyId.addressId.city)
    stageCode = StageCode.objects.get(id=2)
    print("Stage2 od:" + str(datetime_start) + " do:" + str(datetime_next))
    print("Naposledy v:" + last_seen)
    print("Stav2:" + stageCode.stageDescription)
    newStage = Stage(datetime=datetime_start, packageId=package, stageCurrentId=stageCode, lastSeen=last_seen, estTimeOfDelivery=datetime_estimate)
    print(str(newStage))
    newStage.save()

    # STAGE 3
    datetime_start = datetime_next
    duration = random.randint(10, 20) * MULTIPLIER
    delta = timedelta(seconds=duration)
    datetime_next = datetime_start + delta
    delta = timedelta(seconds=60)
    datetime_estimate = datetime_start + delta
    last_seen = str("Sídlo " + package.companyId.companyName + ", " + package.companyId.addressId.city)
    stageCode = StageCode.objects.get(id=3)
    print("Stage3 od:" + str(datetime_start) + " do:" + str(datetime_next))
    print("Naposledy v:" + last_seen)
    print("Stav3:" + stageCode.stageDescription)
    newStage = Stage(datetime=datetime_start, packageId=package, stageCurrentId=stageCode, lastSeen=last_seen, estTimeOfDelivery=datetime_estimate)
    print(str(newStage))
    newStage.save()

    # STAGE 4
    datetime_start = datetime_next
    duration = random.randint(30, 40) * MULTIPLIER
    delta = timedelta(seconds=duration)
    datetime_next = datetime_start + delta
    delta = timedelta(seconds=40)
    datetime_estimate = datetime_start + delta
    # TODO: MAPA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    last_seen = str("Not implemented yet, sorry")
    stageCode = StageCode.objects.get(id=4)
    print("Stage4 od:" + str(datetime_start) + " do:" + str(datetime_next))
    print("Naposledy v:" + last_seen)
    print("Stav4:" + stageCode.stageDescription)
    newStage = Stage(datetime=datetime_start, packageId=package, stageCurrentId=stageCode, lastSeen=last_seen, estTimeOfDelivery=datetime_estimate)
    print(str(newStage))
    newStage.save()

    # STAGE 5
    datetime_start = datetime_next
    # pozrieme typ doručenia
    delivery = package.typeOfDelivery
    print("Spôsob diručenia:" + str(delivery))
    if str(delivery) == "Kuríérom" or str(delivery) == "Poštovým kuriérom":
        stageCode = StageCode.objects.filter(stageDescription="Zásielka už onedlho príde")
        last_seen = str("Neďaleko vašej adresy!")
    elif str(delivery) == "Do boxu":
        stageCode = StageCode.objects.filter(stageDescription="Zásielka bola doručená do boxu")
        last_seen = str("V najbližšom balíko-boxe!")
    elif str(delivery) == "Na poštu":
        stageCode = StageCode.objects.filter(stageDescription="Zásielka bola doručená na poštu")
        last_seen = str("Na Vami zvolenej pošte!")
    elif str(delivery) == "Zásielkovňa":
        stageCode = StageCode.objects.filter(stageDescription="Zásielka bola doručená do zásielkovne")
        last_seen = str("Na Vami zvolenej pobočke!")
    else:
        stageCode = StageCode.objects.filter(stageDescription="Zásielka už onedlho príde")
        last_seen = str("Neďaleko Vás!")

    print("Stage5 od:" + str(datetime_start))
    print("Naposledy v:" + last_seen)
    print("Stav5:" + stageCode[0].stageDescription)
    newStage = Stage(datetime=datetime_start, packageId=package, stageCurrentId=stageCode[0], lastSeen=last_seen, estTimeOfDelivery=datetime_estimate)
    print(str(newStage))
    newStage.save()
    return True

def editPackage(request):
    return render(request, 'base/Package/edit.html')


@login_required(login_url='login')
def history(request):
    account = findAccount(request.user)
    packages = Package.objects.filter(receiverUserId=account, dateDelivered__isnull=False).select_related().order_by(
        '-dateDelivered')
    past_stages = Stage.objects.filter(datetime__lt=timezone.now())

    total_packages = packages.count()

    context = {'packages': packages, 'total_packages': total_packages, 'past_stages': past_stages}
    return render(request, 'base/History/historyPage.html', context)


def deliveryCompanies(request):
    deliveryCompanies = DeliveryCompany.objects.all().select_related('addressId')
    companies = Company.objects.all().select_related('addressId')
    context = {
        'deliveryCompanies': deliveryCompanies,
        'companies': companies,
    }
    return render(request, 'base/DeliveryCompanies/deliveryCompaniesPage.html', context)


@login_required(login_url='login')
def createCompany(request):
    if not request.user.is_staff:
        return HttpResponse('Na toto nemáš povolenie!!!')

    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        company_form = CompanyForm(request.POST)
        print("Spol je:" + str(company_form.is_valid()))
        print("Adresa je:" + str(address_form.is_valid()))
        if address_form.is_valid():
            address = address_form.save()
            address.save()
            request.POST = request.POST.copy()
            obj_address = Address.objects.get(id=address.pk)
            request.POST['addressId'] = obj_address
            company_form = CompanyForm(request.POST)
            print("Spol je:" + str(company_form.is_valid()))
            print(company_form.errors)
            if company_form.is_valid():
                company = company_form.save(commit=False)
                company.addressId = obj_address
                company.save()
                # TODO:redirect na stránku kde vypíše úspech, alebo zobarziť nejaké okno
                return redirect('deliveryCompanies')
    else:
        address_form = AddressForm()
        company_form = CompanyForm()
    context = {'address_form': address_form, 'company_form': company_form}
    return render(request, 'base/DeliveryCompanies/company_form.html', context)


@login_required(login_url='login')
def editCompany(request, pk):
    if not request.user.is_staff:
        return HttpResponse('Na toto nemáš povolenie!!!')

    # TODO: okolo 1:24:00  sa tento redirect ukazuje
    company = Company.objects.get(id=pk)
    # address = Address.objects.get(id=company.addressId.id)
    address_form = AddressForm(instance=company.addressId)
    company_form = CompanyForm(instance=company)


    if request.method == 'POST':
        address_form = AddressForm(request.POST, instance=company.addressId)
        company_form = CompanyForm(request.POST, instance=company)
        if address_form.is_valid() and company_form.is_valid():
            address_form.save()
            company_form.save()
            return redirect('deliveryCompanies')
    context = {'company_form': company_form, 'address_form': address_form}
    return render(request, 'base/DeliveryCompanies/company_form.html', context)


@login_required(login_url='login')
def deleteCompany(request, pk):
    if not request.user.is_staff:
        return HttpResponse('Na toto nemáš povolenie!!!')
    company = Company.objects.get(id=pk)
    if request.method == 'POST':
        company.delete()
        return redirect('deliveryCompanies')
    context = {'obj': company}
    return render(request, 'base/delete.html', context)

def companyDetail(request, pk):
    company = Company.objects.get(id=pk)
    context = {'company': company}
    return render(request, 'base/DeliveryCompanies/company_detail.html', context)


@login_required(login_url='login')
def createDeliveryCompany(request):
    if not request.user.is_staff:
        return HttpResponse('Na toto nemáš povolenie!!!')

    temp_address = Address(city="temp", zipCode="temp", street="temp", streetNumber="temp")
    temp_address.save()
    print("Prvy POST:" + str(request.POST))
    request.POST = request.POST.copy()
    request.POST['addressId'] = temp_address.id
    deliveryCompany_form = DeliveryCompanyForm(request.POST)
    if request.method == 'POST':
        if deliveryCompany_form.is_valid():
            address = Address.objects.create(city=request.POST['city'], zipCode=request.POST['zipCode'],
                                             street=request.POST['street'], streetNumber=request.POST['streetNumber'])
            company = deliveryCompany_form.save(commit=False)
            address.save()
            company.addressId = address
            company.save()
            temp_address.delete()
            # TODO:redirect na stránku kde vypíše úspech, alebo zobarziť nejaké okno
            return redirect('deliveryCompanies')

    context = {'deliveryCompany_form': deliveryCompany_form}
    temp_address.delete()
    return render(request, 'base/DeliveryCompanies/deliveryCompany_form.html', context)


@login_required(login_url='login')
def editDeliveryCompany(request, pk):
    if not request.user.is_staff:
        return HttpResponse('Na toto nemáš povolenie!!!')

    page='edit'
    deliveryCompany = DeliveryCompany.objects.get(id=pk)
    deliveryCompany_form = DeliveryCompanyForm(instance=deliveryCompany)
    address_form = AddressForm(instance=deliveryCompany.addressId)

    if request.method == 'POST':
        deliveryCompany_form = DeliveryCompanyForm(request.POST, instance=deliveryCompany)
        address_form = AddressForm(request.POST, instance=deliveryCompany.addressId)

        if address_form.is_valid() and deliveryCompany_form.is_valid():
            print("both valid!")
            address_form.save()
            deliveryCompany_form.save()
            return redirect('deliveryCompanies')

    context = {'deliveryCompany_form': deliveryCompany_form, 'address_form': address_form, 'deliveryCompany': deliveryCompany, 'page': page}
    return render(request, 'base/DeliveryCompanies/deliveryCompany_form.html', context)


@login_required(login_url='login')
def deleteDeliveryCompany(request, pk):
    if not request.user.is_staff:
        return HttpResponse('Na toto nemáš povolenie!!!')
    deliveryCompany = DeliveryCompany.objects.get(id=pk)
    if request.method == 'POST':
        deliveryCompany.delete()
        return redirect('deliveryCompanies')
    return render(request, 'base/delete.html', {'obj': deliveryCompany})

def deliveryCompanyDetail(request, pk):
    deliveryCompany = DeliveryCompany.objects.get(id=pk)
    context = {'deliveryCompany': deliveryCompany}
    return render(request, 'base/DeliveryCompanies/deliveryCompany_detail.html', context)


def contact(request):
    return render(request, 'base/Contact/contactPage.html')

def findAccount(user):
    print("LOOKING FOR USER:" + str(user))
    accounts = UserAccount.objects.all()
    foundAccount = None
    for account in accounts:
#         print("LOOKING AT:" + str(account) + " " + str(account.user))
        if account.user == user:
#             print('MATCH!')
            foundAccount = account
    return foundAccount

def getCourier(typeOfDelivery, company):
    if typeOfDelivery == 'Do boxu' or typeOfDelivery == 'Zásielkovňa' or typeOfDelivery == 'Na poštu':
        print("NO COURIERS NEEDED!")
        return None
    print("LOOKING FOR:" + typeOfDelivery + " FOR:" + str(company))
    deliCompanies = DeliveryCompany.objects.all()
    for deliCompany in deliCompanies:
        if deliCompany.deliveryCompanyCode == company:
            company = deliCompany

    if company is None:
        return None
    couriers = Courier.objects.filter(deliveryCompanyId=company)
    couriers_count = len(couriers)
    if couriers_count <= 0:
        return None
    print("Found: " + str(couriers_count) + " couriers!")
    index = random.randint(1, couriers_count)
    return couriers[index-1]


def lookupAddress(address):
    addresses = Address.objects.filter(city=address.streetNumber, street=address.street, streetNumber=address.streetNumber)
    addresses_count = len(addresses)
    if addresses_count == 1:
        print("FOUND MATCHING ADDRESS!!!")
        return addresses[0]
    else:
        return None


def lookupAccount(email):
    accounts = UserAccount.objects.filter(email=email)
    accounts_count = len(accounts)
    if accounts_count == 1:
        print("FOUND MATCHING ACCOUNT BY EMAIL!!!")
        return accounts[0]
    else:
        return None


def ajaxTesting(request):
    packages = Package.objects.all()
    context = {'packages': packages}
    return render(request, 'base/ajaxTesting.html', context)