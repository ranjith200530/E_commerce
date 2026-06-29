from django.shortcuts import render,redirect
from commerce import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import re
from django.contrib import messages


from django.db.models import F,Sum

# Create your views here.
# def cart(req,id):
#     product=models.Products.objects.get(id=id)
#     if models.Cart.objects.filter(product=product).exists():
        
#         models.Cart.objects.get_or_create(
#         user=req.user,
#         product=product,
#         quantity=1)
#     else:
#         data=models.Cart.objects.get(product_id=product)
#         data.quantity+=1
#         data.save()
#     return redirect("cart_display")

def cart(req, id):
    product = models.Products.objects.get(id=id)

    cart_item, created = models.Cart.objects.get_or_create(
        user=req.user,
        product=product,
        defaults={"quantity": 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart_display")


def cart_display(req):
    data = models.Cart.objects.filter(user=req.user)
    return render(req,"cart.html",{"data":data})


def increase_quantity(req,id):
    newdata=models.Cart.objects.get(product_id=id)
    newdata.quantity+=1
    newdata.save()
    return redirect("cart_display")
    
def decrease_quantity(req,id):
    newdata=models.Cart.objects.get(product_id=id)
    if newdata.quantity<=0:
        newdata.delete()
    else:
        newdata.quantity-=1
        newdata.save()
    return redirect("cart_display")

def remove_item(req,id):
    newdata=models.Cart.objects.get(product_id=id)
    newdata.delete()
    return redirect("cart_display")
    


def cart_total(req):
    # data=models.Cart.objects.aggregate("total":sum("product.price"))
    data=models.Cart.objects.filter(user=req.user)
    total=models.Cart.objects.filter(user=req.user).aggregate(
    total=Sum(F("quantity") * F("product__price"))
)
    
    # total=0
    # for i in data:
    #      total += i.product.price * i.quantity
    return render(req,"cart.html",{"data":data,"total":total["total"]})



# def order_form(req):
#     if req.method=="POST":
#         name=req.POST.get("name")
#         phone=req.POST.get("phone")
#         city=req.POST.get("city")
#         pincode=req.POST.get("pincode")
#         address=req.POST.get("address")
        
#         models.order.objects.create(name=name,phone=phone,city=city, pincode=pincode,address=address)
        
#     return render(req,'order.html')
        
def order_form(request):
    cart_items = models.Cart.objects.filter(user=request.user)

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        city = request.POST.get("city")
        pincode = request.POST.get("pincode")
        address = request.POST.get("address")

        # 1. Create Order
        order_obj = models.order.objects.create(
            name=name,
            phone=phone,
            city=city,
            pincode=pincode,
            address=address
        )

        # 2. Move Cart → OrderItems
        for item in cart_items:
            models.OrderItem.objects.create(
                order=order_obj,
                product=item.product,
                quantity=item.quantity,
                
                
            )

        # 3. Clear cart after order placed
        # cart_items.delete()

        return redirect("order_success", order_id=order_obj.id)

    return render(request, "order.html")


def checkout_review(request):
    cart_items = models.Cart.objects.filter(user=request.user)

    items = []
    total = 0

    for item in cart_items:
        subtotal = item.product.price * item.quantity
        total += subtotal

        items.append({
            "image":item.product.image,
            "product": item.product,
            "quantity": item.quantity,
            "subtotal": subtotal
        })

    return render(request, "checkout_form.html", {
        "items": items,
        "total": total,
        # "image": item.product.image.url ,
    })
    


# def place_order(request):
#     if request.method == "POST":

#         # 1. Create Order
#         order_obj = models.order.objects.create(
#             name=request.POST['name'],
#             phone=request.POST['phone'],
#             city=request.POST['city'],
#             address=request.POST['address'],
#             pincode=request.POST['pincode']
#         )

#         # 2. Get cart items of logged-in user
#         cart_items = models.Cart.objects.filter(user=request.user)

#         # 3. Move cart → order items
#         for item in cart_items:
#             models.OrderItem.objects.create(
#                 order=order_obj,
#                 product=item.product,
#                 quantity=item.quantity
#             )

#         # 4. Clear cart after order
#         cart_items.delete()

#         return redirect("order_success", order_id=order_obj.id)
#     return redirect("orders")
    
def order_success(request, order_id):
    order_obj = models.order.objects.get(id=order_id)
    # items = order_obj.items.all()
   
    items = models.OrderItem.objects.filter(order_id=order_id)

    return render(request, "sucess.html", {
        "order": order_obj,
        "items": items,
       
    })
    
    
    
def admin_page(req):
     if req.user.is_superuser:
         data=models.Category.objects.all()
         return render(req,"adminpage.html",{"data":data})
     return redirect("home")


def read(req):
    data=models.Category.objects.all()
    return render(req,"adminpage.html",{"data":data})

def edit(req,id):
    data=models.Category.objects.get(id=id)
    if req.method=="POST":
        name=req.POST.get("name")
        data.name=name
        data.save()
        return redirect("admin_page")
    return render(req,"edit.html",{"data":data})

def delete(req,id):
    data=models.Category.objects.get(id=id)
    if data.products_set.exists():
        messages.error(
            req,
            "Category cannot be deleted because products exist."
        )
    data.delete()
    return redirect("admin_page")
    
def add_categeory(req):
    if req.method=="POST":
        cat_name=req.POST.get("name")
        models.Category.objects.create(name=cat_name)
        return redirect("admin_page")
    return render(req,"add_category.html")
    
    
    