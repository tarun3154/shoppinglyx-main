from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .forms import *



login_required(login_url='login')
def address(request):
    add= Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add})


login_required(login_url='login')
def orders(request):
    op =OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})


def change_password(request):
    return render(request, 'app/changepassword.html')

@method_decorator(login_required, name='dispatch')
class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobile = Product.objects.filter(category='M')
        laptop = Product.objects.filter(category='L')
        return render(request, 'app/home.html', {'topwears': topwears, 'bottomwears': bottomwears, 'mobile': mobile, 'laptop': laptop})


@method_decorator(login_required, name='dispatch')
class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:
            item_already_in_cart= Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product': product,'item_already_in_cart':item_already_in_cart})

@method_decorator(login_required, name='dispatch')
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


login_required(login_url='login')
def add_to_cart(request):
    user=request.user
    product_id= request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')


login_required(login_url='login')
def payment_done(request):
    user=request.user
    custid=request.GET.get("custid")
    customer= Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect('orders')
    


login_required(login_url='login')
def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart= Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=70.0
        total_amount= 0.0
        cart_product= [p for p in Cart.objects.all() if p.user==user]

        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount+= tempamount
                total_amount= amount + shipping_amount
        return render(request,'app/addtocart.html',{'carts':cart,'amount':amount,'totalamount':total_amount})
    else:
        return render(request,'app/emptycart.html')
    
def plus_cart(request):
    if request.method == 'GET':
        user=request.user
        prod_id= request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product= [p for p in Cart.objects.all() if p.user== user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount+= tempamount
            total_amount= amount + shipping_amount
            data={
                'quantity':c.quantity,
                'amount':'amount',
                'totalamount':total_amount
            }
            return JsonResponse(data)

           


def minus_cart(request):
    if request.method == 'GET':
        user=request.user
        prod_id= request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product= [p for p in Cart.objects.all() if p.user== user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount+= tempamount
            total_amount= amount + shipping_amount
            data={
                'quantity':c.quantity,
                'amount':'amount',
                'totalamount':total_amount
            }
            return JsonResponse(data)

           




def remove_item(request, item_id):
    try:
        cart_item = Cart.objects.get(id=item_id)
        cart_item.delete()
        messages.success(request, "Item removed from cart successfully.")
    except Cart.DoesNotExist:
        messages.error(request, "Item not found in cart.")

    return redirect('/cart')



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
    user=request.user
    add= Customer.objects.filter(user=user)
    cart_items= Cart.objects.filter(user=user)
    amount= 0.0
    shipping_amount= 70.0
    totalamount= 0.0
    cart_product= [p for p  in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount +=tempamount
            totalamount =amount +shipping_amount
    return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items})


