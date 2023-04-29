from django.shortcuts import render, redirect
from Cart import Cart
import json, requests
from from_number_to_letters import Thousands_Separator
from django.http import HttpResponse
from datetime import date

def Index(request):
	if 'carrito' not in request.session:
		request.session['carrito'] = 0
	url = "https://apirapimercado.pythonanywhere.com/api/Get_All_Product/"
	payload = {}
	headers = {}
	response = requests.request("POST", url, headers=headers, data=payload)
	data = json.loads(response.text)
	list_product = {}
	for j in data['category']:
		value = []
		for i in data['products']:
			if i['category'] == j['name']:
				value.append({
						"name":i['product']
					})
		if value:
			list_product[j['name']] = value
	print(list_product)
	return render(request,'index.html',{'category':data['category'], 'products':data['products'], 'list_product': list_product})

def List_Products(request,c,s):
	try:
		c = str(c).replace('_',' ')
		s = str(s).replace('_',' ')
	except Exception as e:
		pass

	request.session['categoria'] = c
	request.session['subcategory'] = s

	url = "https://apirapimercado.pythonanywhere.com/api/Get_Product/"
	payload = json.dumps({
	  "category": c,
	  "subcategory": s
	})
	headers = {
	  'Content-Type': 'application/json'
	}
	response = requests.request("POST", url, headers=headers, data=payload)
	print(response.text)
	data = json.loads(response.text)
	return render(request,'ecommerce/product_grid.html',{'data':data,'c':c,'s':s})	

def Add_Cart(request):
	if request.is_ajax():
		data = request.GET
		url = "https://apirapimercado.pythonanywhere.com/api/Get_Product_Only/"
		payload = json.dumps({"code": data['code']})
		headers = {'Content-Type': 'application/json'}
		response = requests.request("POST", url, headers=headers, data=payload)
		product = json.loads(response.text)
		print(product)
		quanty = data['quanty']
		result = Cart(request).Add(product, quanty)
		if result:
			if int(quanty) > 0:
				request.session['carrito'] += 1
			else:
				if int(request.session['carrito']) > 0:
					request.session['carrito'] -= 1
				else:
					request.session['carrito'] = 0
		return HttpResponse(json.dumps({'result':result, 'carrito':request.session['carrito']}))


def View_Shopping_Cart(request):
	try:
		request.session['categoria'] = str(request.session['categoria']).replace(' ','_')
		request.session['subcategory'] = str(request.session['subcategory']).replace(' ','_')
	except Exception as e:
		pass
	print(request.session['categoria'])
	print(request.session['subcategory'])
	print(request.session['data_user']['name'])
	cart = Cart(request)
	subtotal = 0
	for i in cart:
		subtotal += int(i['total'])

	return render(request,'ecommerce/cart.html',{'cart':cart, 'total':Thousands_Separator(subtotal), 'cnt_cart':len(cart)})

def Invoice(request):
	try:
		if 'user' in request.session:
			cart = Cart(request)
			subtotal = 0
			data_invoice = []
			for i in cart:
				subtotal += int(i['total'])
				url = "https://apirapimercado.pythonanywhere.com/order/Create_Order/"
				data_invoice.append({
				  "email": request.session['user'],
				  "code": i['code'],
				  "product": i['product'],
				  "quanty": i['quanty'],
				  "price": i['price'],
				  "discount": i['discount']
				})
			payload = json.dumps(data_invoice)
			headers = {
			  'Content-Type': 'application/json'
			}
			response = requests.request("POST", url, headers=headers, data=payload)
			c = json.loads(response.text)['consecutive']
			data = cart
			cart.clear()
			request.session['carrito'] = 0
			return render(request,'ecommerce/invoice.html',{'data':data,'total':Thousands_Separator(subtotal),'number':c,'date':date.today(),'n_cart':request.session['carrito']})
	except Exception:
		pass
	return redirect('View_Shopping_Cart')


# USER

def Login(request):
	if request.is_ajax():
		url = "https://apirapimercado.pythonanywhere.com/user/Login/"
		payload = json.dumps({"email": request.GET['email']})
		headers = {'Content-Type': 'application/json'}
		response = requests.request("POST", url, headers=headers, data=payload)
		result = json.loads(response.text)
		if result['result']:
			request.session['data_user'] = result['data']
			request.session['user'] = request.GET['email']
		return HttpResponse(result)
	return render(request,'authentication/login.html')

def Register(request):
	if request.is_ajax():
		data = request.GET
		url = "https://apirapimercado.pythonanywhere.com/user/Create_User/"
		payload = json.dumps({
		  "name": request.GET['name'],
		  "email": request.GET['email'],
		  "phone": request.GET['phone'],
		  "psswd": request.GET['psswd'],
		})
		headers = {'Content-Type': 'application/json'}
		response = requests.request("POST", url, headers=headers, data=payload)
		result = json.loads(response.text)['result']
		if result:
			request.session['user'] = request.GET['email']
		return HttpResponse(result)
	return render(request,'authentication/register.html')


def LogOut(request):
	for i,j in list(request.session.items()):
		del request.session[i]
	return redirect('Index')



def CheckOut(request):
	return render(request,'ecommerce/checkout.html')