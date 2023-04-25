from django.http import HttpResponseRedirect
from django.conf import settings
from decimal import Decimal

class Cart(object):
	def __init__(self,request):
		self.session = request.session
		cart = self.session.get(settings.CART_SESSION_ID)
		if not cart:
			cart = self.session[settings.CART_SESSION_ID] = {}
		self.cart = cart
		self.request = request

	def save(self):
		self.session[settings.CART_SESSION_ID]=self.cart
		self.session.modified = True

	def serializarJSON(self,producto):
		total = 0
		car = self.cart[str(producto.pk)]
		d = {'total':car['total']}
		return d

	def Add(self,inventory,price,quanty,type_product):
		result = False
		if str(inventory.pk) in self.cart:
			total = int(price) * int(quanty)
			cart = self.cart[str(inventory.pk)]
			cart['quanty'] = quanty
			cart['total'] = total
			cart['price'] = price
			cart['type'] = type_product
		else:
			total = int(price) * int(quanty)
			self.cart[str(inventory.pk)] = {'pk':inventory.pk, 'code':inventory.code,'article':inventory.article,'quanty':quanty,'price':price,'total':total,'type':type_product}
			result = True
		self.save()
		print(self.cart)
		return result

	def remove(self,product):
		product_id = str(product.pk)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	def __iter__(self):
		for item in self.cart.values():
			yield item


	def __len__(self):
		return sum(int(item['quanty']) for item in self.cart.values())

	def clear(self):
		del self.session[settings.CART_SESSION_ID]
		self.session.modified = True