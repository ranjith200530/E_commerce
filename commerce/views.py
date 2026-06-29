from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import re
from . import models

from django.db.models import F,Sum
# Create your views here.

def logout_user(req):
    logout(req)
    return redirect("login")
def login_page(req):
    if req.user.is_authenticated:
        return redirect("home")
    
    if req.method=="POST":
        username=req.POST.get("username")
        password=req.POST.get("password")
        
        user=authenticate(
            req,
            username=username,
            password=password
        )
        print(user)
        if user:
            login(req,user)
            return redirect("home")
    return render(req,"login.html")


def register(req):
    if req.method=="POST":
        username=req.POST.get("username")
        password=req.POST.get("password1")
        password2=req.POST.get("password2")
        
        if username=="":
            return render(req,"register.html",{"error":"Please enter username"})
        if len(password)<6 or password==None:
            return render(req,"register.html",{"error":"Password must br greater than 6 characters"})
        if password!=password2:
            return render(req,"register.html",{"error":"Please enter password correct"})
        # checking whether a user with the username exits or not
        if User.objects.filter(username=username).exists():

            return render(req, "register.html", {
                "error": "User already exists"
            })

        # UPPERCASE CHECK
        if not re.search(r"[A-Z]", password):

            return render(req, "register.html", {
                "error": "Password must contain uppercase letter"
            })

        # LOWERCASE CHECK
        if not re.search(r"[a-z]", password):

            return render(req, "register.html", {
                "error": "Password must contain lowercase letter"
            })

        # NUMBER CHECK
        if not re.search(r"[0-9]", password):

            return render(req, "register.html", {
                "error": "Password must contain a number"
            })

        # SPECIAL CHARACTER CHECK
        if not re.search(r"[@#$%^&*!]", password):

            return render(req, "register.html", {
                "error": "Password must contain special character"
            })

            
        user = User.objects.create_user(
            username=username,
            password=password
        )
        login(req,user)
        return redirect("home")
    return render(req,"register.html")

def home(req):
    data=models.Products.objects.all()
    return render(req,"homepage.html",{"data":data})



def category(req,name):
    data=models.Products.objects.filter(category__name__icontains=name)
    return render(req,"category.html",{"data":data})


def product_feature(req,id):
    data=models.Products.objects.get(id=id)
    return render(req,"product_feature.html",{"product":data})


def search(req):
    search=req.GET.get("search")
    product=models.Products.objects.filter(product_name__icontains=search)
    print(product)
    return render(req,"search.html",{"product":product})



# def cart(req,id):
#     product=models.Products.objects.get(id=id)
#     models.Cart.objects.get_or_create(
#     user=req.user,
#     product=product,
#     quantity=1)
#     return redirect("cart_display")


# def cart_display(req):
#     data=models.Cart.objects.all()
#     return render(req,"cart.html",{"data":data})


# def increase_quantity(req,id):
#     newdata=models.Cart.objects.get(product_id=id)
#     newdata.quantity+=1
#     newdata.save()
#     return redirect("cart_display")
    
# def decrease_quantity(req,id):
#     newdata=models.Cart.objects.get(product_id=id)
#     if newdata.quantity<=0:
#         newdata.delete()
#     else:
#         newdata.quantity-=1
#         newdata.save()
#     return redirect("cart_display")

# def remove_item(req,id):
#     newdata=models.Cart.objects.get(product_id=id)
#     newdata.delete()
#     return redirect("cart_display")
    


# def cart_total(req):
#     # data=models.Cart.objects.aggregate("total":sum("product.price"))
#     data=models.Cart.objects.all()
#     total=models.Cart.objects.aggregate(
#     total=Sum(F("quantity") * F("product__price"))
# )
    
#     # total=0
#     # for i in data:
#     #      total += i.product.price * i.quantity
#     return render(req,"cart.html",{"data":data,"total":total["total"]})





