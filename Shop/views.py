from django.shortcuts import render,redirect
from django.views import View
from . models import  product,customer,Cart,OrderPlaced
from . forms import CustomerRegistrationForm,customerprofile
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse


# Create your views here.
class productView(View):
  def get(self,request):
     pants=product.objects.filter(cetagory='P')
     shirt=product.objects.filter(cetagory='sh')
     jercy=product.objects.filter(cetagory='j')
     saree=product.objects.filter(cetagory='s')
     lehenga=product.objects.filter(cetagory='k')
 
     return render(request, 'Shop/home.html',{'pant':pants,'shirt':shirt,'jercy':jercy,'sare':saree,'lahenga':lehenga})

class productDetialView(View):
 def get(self,request,pk):
   product_detail=product.objects.get(pk=pk)
   return render(request, 'Shop/productdetail.html',{'produc_d':product_detail})

def add_to_cart(request):
 user=request.user
 product_id=request.GET.get('prod_id')
 Product=product.objects.get(id=product_id)
 Cart(user=user,product=Product).save()
 return redirect('/cart')

def buy_now(request):
 return render(request, 'Shop/buynow.html')

class customerprofileView(View):
 def get (self,request):
  form=customerprofile()
  return render(request, 'Shop/profile.html',{'form':form,'active':'btn-primary'})
 
 def post(self,request):
   form=customerprofile(request.POST)
   if form.is_valid():
    usr=request.user
    name=form.cleaned_data['name']
    division=form.cleaned_data['division']
    district=form.cleaned_data['district']
    thana=form.cleaned_data['thana']
    vilroad=form.cleaned_data['vllorroad']
    zipcode=form.cleaned_data['zipcode']

    reg=customer(user=usr,name=name,division=division,district=district,thana=thana,vllorroad=vilroad,zipcode=zipcode)

    reg.save()
    messages.success(request,'Succesfully Done your Profile')
   return render(request, 'Shop/profile.html',{'form':form,'active':'btn-primary'})



def address(request):
 add=customer.objects.filter(user=request.user)
 
 return render(request, 'Shop/address.html',{'add':add,'active':'btn-primary'})

def orders(request):
  op=OrderPlaced.objects.filter(user=request.user)
  return render(request, 'Shop/orders.html',{'op':op})

def change_password(request):
 return render(request, 'Shop/changepassword.html')

def lehenga(request,data=None):
 if data==None:
   lehengas=product.objects.filter(cetagory='k')
 elif data=='Arong' or data=='Sara':
   lehengas=product.objects.filter(cetagory='k').filter(brand=data)
 return render(request, 'Shop/lehenga.html',{'lehanga':lehengas})

def login(request):
     return render(request, 'Shop/login.html')

class CustomerRegistrationView(View):
 def get(self, request):
  form = CustomerRegistrationForm()
  return render(request, 'Shop/customerregistration.html', {'form': form})
 def post(self, request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   form.save()
   messages.success(request,'Congratuolation Succesfully Registration Done!!!')
  return render(request, 'Shop/customerregistration.html',{'form': form})
  

def checkout(request):
  user=request.user
  add=customer.objects.filter(user=user)
  cart_item=Cart.objects.filter(user=user)
  amount=0.0
  shiping_amount=100.00
  total_amount=0

  cart_product=[p for p in Cart.objects.all() if p.user==user]
  if cart_product:
      for p in cart_product:
        tempamount=(p.quantity*p.product.discount_price)
        amount=tempamount+amount
        totalamount=amount+shiping_amount
  return render(request, 'Shop/checkout.html',{'add':add,'cart':cart_item,'total_amount':totalamount})

def Show_cart(request):
  if request.user.is_authenticated:
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0.0
    shiping_amount=100.00
    total_amount=0

    cart_product=[p for p in Cart.objects.all() if p.user==user]
    if cart_product:
      for p in cart_product:
        tempamount=(p.quantity*p.product.discount_price)
        amount=tempamount+amount
        totalamount=amount+shiping_amount
      return render (request,'Shop/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount})
    
    else:
      return render(request,'Shop/emtycart.html')
#PLUS CART
def plus_cart(request):
    if request.method == 'GET':
      prod_id = request.GET['prod_id']
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.quantity +=1
      c.save()
      amount = 0
      shipping_amount = 100
      cart_product = [p for p in Cart.objects.all() if p.user==request.user]
      for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount  
            totalamount = amount + shipping_amount
      data = {
         'quantity': c.quantity,
         'amount': amount,
         'totalamount': totalamount
      }
      return JsonResponse(data)
    

#minus cart
def minus_cart(request):
    if request.method == 'GET':
      prod_id = request.GET['prod_id']
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.quantity -=1
      c.save()
      amount = 0
      shipping_amount = 100
      cart_product = [p for p in Cart.objects.all() if p.user==request.user]
      for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount  
            totalamount = amount + shipping_amount
      data = {
         'quantity': c.quantity,
         'amount': amount,
         'totalamount': totalamount
      }
      return JsonResponse(data)
    

#remove cart
def remove_cart(request):
    if request.method == 'GET':
      prod_id = request.GET['prod_id']
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.delete()
      amount = 0
      shipping_amount = 100
      cart_product = [p for p in Cart.objects.all() if p.user==request.user]
      for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount  
            
      data = {
         'amount': amount,
         'totalamount': amount + shipping_amount
      }
      return JsonResponse(data)
    
#payment_done

def payment_done(request):
  user=request.user
  custid=request.GET.get('custid')
  customers=customer.objects.get(id=custid)
  cart=Cart.objects.filter(user=user)
  for c in cart:
    OrderPlaced(user=user,customer=customers,product=c.product,quantity=c.quantity).save()
    c.delete()
    
  return redirect('orders')