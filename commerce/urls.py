from django.contrib import admin
from django.urls import path
from . import views 
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
   path('',views.login_page,name="login"),
   path('register/',views.register,name="register"),
   path('home/',views.home,name="home"),
   path('logout/',views.logout_user,name="logout"),
   path('category/<str:name>/', views.category, name="category"),
   path('prodcut/<int:id>/', views.product_feature, name="product"),
   path('search/', views.search, name="search"),
#    path('cart/<int:id>/', views.cart, name="cart"),
#    path('cartdisplay/',views.cart_display,name="cart_display"),
#    path('increase/<int:id>/',views.increase_quantity,name="increase_quantity"),
#     path('decrease/<int:id>/',views.decrease_quantity,name="decrease_quantity"),
#     path('remove/<int:id>/',views.remove_item,name="remove"),
#     path('total/',views.cart_total,name='total'),
   
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )