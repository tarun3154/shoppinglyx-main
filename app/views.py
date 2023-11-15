from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import EmailMessage

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .forms import *



@login_required(login_url='login')
def address(request):
    add= Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add})


@login_required(login_url='login')
def orders(request):
    return render(request, 'app/orders.html')


@login_required(login_url='login')
def change_password(request):
    return render(request, 'app/changepassword.html')


# @login_required(login_url='login')
class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobile = Product.objects.filter(category='M')
        laptop = Product.objects.filter(category='L')
        return render(request, 'app/home.html', {'topwears': topwears, 'bottomwears': bottomwears, 'mobile': mobile, 'laptop': laptop})


class ProductDetailView(View):
    @login_required(login_url='login')
    def get(self, request, pk):
        user=request.user
        product = Product.objects.get(id=pk)
        print(product)
        return render(request, 'app/productdetail.html', {'product': product,'user':user})


@login_required(login_url='login')
def add_to_cart(request):
    user=request.user
    product_id= request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product.id).save()
    return render(request, 'app/addtocart.html')

def removeitem(request,pk):
    item=Cart.objects.get(id=pk)
    item.delete()
    redirect('cart')



@login_required(login_url='login')
def buy_now(request):
    return render(request, 'app/buynow.html')


@login_required(login_url='login')
def mobile(request, data=None):
    if data == None:
        mobile = Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'Iphone' or data == 'Motorola' or data == 'Oneplus':
        mobile = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'above':
        mobile = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    elif data == 'below':
        mobile = Product.objects.filter(category='M').filter(discounted_price__lt=10000)

    return render(request, 'app/mobile.html', {'mobile': mobile})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')  # Adjust the URL name if necessary
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'app/login.html', {'form': form})


def Userlogout(request):
    logout(request)
    return redirect('login')


def register_user(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        messages.success(request, "Registration successful")
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomerRegistrationForm()

    return render(request, 'app/customerregistration.html', {'form': form})


@login_required(login_url='login')
def checkout(request):
    return render(request, 'app/checkout.html')



class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg= Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Profile Successfully Updated')
        
        return render(request, 'app/profile.html', {'form': form ,'user':usr})
