from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .forms import *

class ProductView(View):
 def get(self,request):
  topwears = Product.objects.filter(category='TW')
  bottomwears= Product.objects.filter(category = 'BW')
  mobile = Product.objects.filter(category='M')
  laptop =Product.objects.filter(category= 'L')
  return render(request, 'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobile':mobile,'laptop':laptop})

class ProductDetailView(View):
 def get(self,request,pk):
  product =Product.objects.get(id=pk)
  return render(request, 'app/productdetail.html',{'product':product})

def add_to_cart(request):
 return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
 return render(request, 'app/address.html')

def orders(request):
 return render(request, 'app/orders.html')

def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request,data=None):
 if data == None:
  mobile = Product.objects.filter(category='M')

 elif data == 'Redmi' or data == 'Iphone' or data == 'Motorola' or data == 'Oneplus':
   mobile = Product.objects.filter(category = 'M').filter(brand =data)

 elif data == 'above':
  mobile = Product.objects.filter(category = 'M').filter(discounted_price__gt=10000)

 elif data == 'below':
  mobile = Product.objects.filter(category = 'M').filter(discounted_price__lt=10000)

 return render(request, 'app/mobile.html',{'mobile':mobile})


def login_user(request):
  if request.method == 'POST':
     form = AuthenticationForm(request,data=request.POST)
     if form.is_valid():
       username = form.cleaned_data.get('username')
       pasword = form.cleaned_data.get('password')
       user= authenticate(username=username, pasword=pasword)
       if user:
         login(request,user)
         messages.success=(request,"Login Successfully") 
         return redirect('home')
  else:
        form = AuthenticationForm()

  return render(request, 'app/login.html', {'form': form})
 
def register_user(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomerRegistrationForm()

    return render(request, 'app/customerregistration.html', {'form': form})


def checkout(request):
 return render(request, 'app/checkout.html')
