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

	def Add(self,product,quanty):
		result = False
		if int(quanty) <= 0:
			self.remove(product)
		elif str(product['code']) in self.cart and int(quanty) > 0:
			total = int(product['price']) * int(quanty)
			cart = self.cart[str(product['code'])]
			cart['quanty'] = quanty
			cart['total'] = total
			cart['price'] = product['price']
		elif int(quanty) > 0:
			total = int(product['price']) * int(quanty)
			self.cart[str(product['code'])] = {'code':product['code'],'product':product['product'],'quanty':quanty,'price':product['price'],'discount':product['discount'],'total':total,'img':product['img']}
			result = True
		self.save()
		print(self.cart)
		return result

	def remove(self,product):
		product_id = str(product['code'])
		if product_id in self.cart:
			del self.cart[product_id]
			print('removido')
			self.save()

	def __iter__(self):
		for item in self.cart.values():
			yield item


	def __len__(self):
		return sum(int(item['quanty']) for item in self.cart.values())

	def clear(self):
		del self.session[settings.CART_SESSION_ID]
		self.session.modified = True