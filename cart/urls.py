from django.contrib import admin
from django.urls import path
from . import views 
# from commerce import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
   
   path('cart/<int:id>/', views.cart, name="cart"),
   path('cartdisplay/',views.cart_display,name="cart_display"),
   path('increase/<int:id>/',views.increase_quantity,name="increase_quantity"),
    path('decrease/<int:id>/',views.decrease_quantity,name="decrease_quantity"),
    path('remove/<int:id>/',views.remove_item,name="remove"),
    path('total/',views.cart_total,name='total'),
    path('order/',views.order_form,name='orders'),
     path('checkout/',views.checkout_review,name='checkout_form'),
    #  path("check/", views.place_order, name="checkout"),
    path("order-success/<int:order_id>/", views.order_success, name="order_success"),
    path('adminpage/',views.admin_page,name="admin_page"),
    path('add_category/',views.add_categeory,name="add_category"),
    path('read/',views.read,name="read"),
    path('delete/<int:id>/',views.delete,name="delete"),
    path('edit/<int:id>',views.edit,name="edit"),
   
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )