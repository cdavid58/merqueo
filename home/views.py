from django.shortcuts import render
import json, requests


def Index(request):
	if 'carrito' not in request.session:
		request.session['carrito'] = 0
	return render(request,'index.html')

def List_Products(request,c,s):
	try:
		c = str(c).replace('_',' ')
	except Exception as e:
		pass

	print(c)

	url = "http://localhost:9090/api/Get_Product/"
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
	return render(request,'ecommerce/product_grid.html',{'data':data})	