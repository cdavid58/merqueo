from django.conf.urls import url
from .views import *

urlpatterns=[
	url(r'^$',Index,name="Index"),
	url(r'^List_Products/(\w+)/(\w+)/$',List_Products,name="List_Products"),
	url(r'^Add_Cart/$',Add_Cart,name="Add_Cart"),
	url(r'^View_Shopping_Cart/$',View_Shopping_Cart,name="View_Shopping_Cart"),
	url(r'^Invoice/$',Invoice,name="Invoice"),
	url(r'^Login/$',Login,name="Login"),
	url(r'^Register/$',Register,name="Register"),
	url(r'^CheckOut/$',CheckOut,name="CheckOut"),
	url(r'^LogOut/$',LogOut,name="LogOut"),
]