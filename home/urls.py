from django.conf.urls import url
from .views import *

urlpatterns=[
	url(r'^$',Index,name="Index"),
	url(r'^List_Products/(\w+)/(\w+)/$',List_Products,name="List_Products"),
]